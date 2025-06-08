import json
import logging
import time
from collections import defaultdict
from django.http import JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import jwt
from datetime import datetime

logger = logging.getLogger(__name__)

class CORSDebugMiddleware(MiddlewareMixin):
    """
    Detailed CORS debugging middleware to identify exactly what's happening
    Includes rate limiting to prevent log flooding from repeated errors
    """
    
    # Class-level cache for tracking repeated errors
    _error_cache = defaultdict(list)
    _suppressed_logs = defaultdict(int)
    _max_repeats = 3
    _time_window = 60  # 60 seconds
    
    def process_request(self, request):
        """Log all incoming request details"""
        debug_info = {
            'method': request.method,
            'path': request.path,
            'origin': request.META.get('HTTP_ORIGIN', 'No Origin'),
            'host': request.META.get('HTTP_HOST', 'No Host'),
            'user_agent': request.META.get('HTTP_USER_AGENT', 'No User Agent'),
            'referer': request.META.get('HTTP_REFERER', 'No Referer'),
            'content_type': request.META.get('CONTENT_TYPE', 'No Content Type'),
            'is_secure': request.is_secure(),
            'scheme': request.scheme,
            'cors_headers': {},
            'auth_headers': {},
        }
        
        # Log CORS-related headers
        cors_headers = [
            'HTTP_ORIGIN', 'HTTP_ACCESS_CONTROL_REQUEST_METHOD', 
            'HTTP_ACCESS_CONTROL_REQUEST_HEADERS'
        ]
        for header in cors_headers:
            if header in request.META:
                debug_info['cors_headers'][header] = request.META[header]
        
        # Log authentication headers
        auth_headers = ['HTTP_AUTHORIZATION', 'HTTP_COOKIE']
        for header in auth_headers:
            if header in request.META:
                # Don't log full cookie/auth values for security
                debug_info['auth_headers'][header] = 'Present' if request.META[header] else 'Empty'
        
        # Log cookies separately
        cookies = {}
        for cookie_name in ['access_token', 'refresh_token', 'csrftoken']:
            if cookie_name in request.COOKIES:
                cookies[cookie_name] = 'Present'
        debug_info['cookies'] = cookies
        
        # Debug: Log raw cookie header for troubleshooting
        raw_cookies = request.META.get('HTTP_COOKIE', '')
        if raw_cookies:
            debug_info['raw_cookie_header'] = raw_cookies[:200] + '...' if len(raw_cookies) > 200 else raw_cookies
        
        # Debug: Log all parsed cookies
        debug_info['all_parsed_cookies'] = list(request.COOKIES.keys())
        
        # Only log if not suppressed
        should_log = self._should_log_request(request.path, request.method)
        if should_log:
            logger.info(f"🔍 CORS DEBUG REQUEST: {json.dumps(debug_info, indent=2)}")
        
        # Store debug info for later use
        request._cors_debug_info = debug_info
        
    def process_response(self, request, response):
        """Log all outgoing response details"""
        debug_info = getattr(request, '_cors_debug_info', {})
        
        response_info = {
            'status_code': response.status_code,
            'content_type': response.get('Content-Type', 'Not set'),
            'response_headers': {},
            'cors_headers_added': {},
        }
        
        # Log all CORS-related response headers
        cors_response_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers',
            'Access-Control-Allow-Credentials',
            'Access-Control-Max-Age',
            'Access-Control-Expose-Headers',
        ]
        
        for header in cors_response_headers:
            if header in response:
                response_info['cors_headers_added'][header] = response[header]
        
        # Log other important headers
        other_headers = ['Location', 'WWW-Authenticate', 'Set-Cookie']
        for header in other_headers:
            if header in response:
                response_info['response_headers'][header] = 'Present' if response[header] else 'Empty'
        
        combined_info = {
            'request': debug_info,
            'response': response_info,
            'analysis': self._analyze_cors_issue(debug_info, response_info)
        }
        
        # Check if this is a repeated error and should be logged
        should_log = self._should_log_response(request.path, response.status_code, combined_info, request)
        if should_log:
            logger.info(f"📤 CORS DEBUG RESPONSE: {json.dumps(combined_info, indent=2)}")
        
        return response
    
    def _analyze_cors_issue(self, request_info, response_info):
        """Analyze potential CORS issues"""
        issues = []
        recommendations = []
        
        # Check if origin is present
        if request_info.get('origin') == 'No Origin':
            issues.append("No Origin header in request")
            recommendations.append("Request might not be a cross-origin request")
        
        # Check if CORS headers are present in response
        cors_headers = response_info.get('cors_headers_added', {})
        if not cors_headers.get('Access-Control-Allow-Origin'):
            issues.append("No Access-Control-Allow-Origin header in response")
            recommendations.append("CORS middleware might not be working")
        
        # Check for redirect responses
        if 300 <= response_info['status_code'] < 400:
            issues.append(f"Redirect response ({response_info['status_code']})")
            recommendations.append("Redirects can cause CORS issues - check URL paths")
        
        # Check authentication
        if response_info['status_code'] == 401:
            issues.append("Authentication required")
            recommendations.append("This is normal for protected endpoints without tokens")
        
        # Check if it's a preflight request
        if request_info.get('method') == 'OPTIONS':
            if not cors_headers.get('Access-Control-Allow-Methods'):
                issues.append("Missing Access-Control-Allow-Methods in OPTIONS response")
                recommendations.append("Preflight request not handled properly")
        
        return {
            'issues': issues,
            'recommendations': recommendations,
            'cors_status': 'OK' if not issues or (len(issues) == 1 and 'Authentication required' in issues) else 'PROBLEM'
        }
    
    def _should_log_request(self, path, method):
        """Check if this request should be logged based on rate limiting"""
        current_time = time.time()
        key = f"{method}:{path}"
        
        # Clean old entries
        self._error_cache[key] = [
            timestamp for timestamp in self._error_cache[key] 
            if current_time - timestamp < self._time_window
        ]
        
        # Add current request
        self._error_cache[key].append(current_time)
        
        # Check if we should suppress
        if len(self._error_cache[key]) > self._max_repeats:
            self._suppressed_logs[key] += 1
            return False
        
        return True
    
    def _should_log_response(self, path, status_code, response_info, request=None):
        """Check if this response should be logged and analyze JWT if it's an auth error"""
        current_time = time.time()
        key = f"{status_code}:{path}"
        
        # Clean old entries
        self._error_cache[key] = [
            timestamp for timestamp in self._error_cache[key] 
            if current_time - timestamp < self._time_window
        ]
        
        # Add current response
        self._error_cache[key].append(current_time)
        
        # If this is the first auth error in this window, add detailed JWT analysis
        if status_code == 401 and len(self._error_cache[key]) == 1:
            jwt_analysis = self._analyze_jwt_token(response_info, request)
            response_info['jwt_analysis'] = jwt_analysis
            logger.info(f"🔐 JWT TOKEN ANALYSIS: {json.dumps(jwt_analysis, indent=2)}")
        
        # Check if we should suppress repeated errors
        if len(self._error_cache[key]) > self._max_repeats:
            self._suppressed_logs[key] += 1
            if self._suppressed_logs[key] == 1:  # First time suppressing
                logger.warning(f"🔁 Repeated authentication failure detected for {path} (status {status_code}). "
                             f"Logging suppressed temporarily. Total occurrences: {len(self._error_cache[key])}")
            return False
        
        return True
    
    def _analyze_jwt_token(self, response_info, request=None):
        """Analyze JWT tokens in cookies for detailed debugging"""
        request_info = response_info.get('request', {})
        cookies = request_info.get('cookies', {})
        
        analysis = {
            'cookies_present': list(cookies.keys()),
            'refresh_token_status': 'not_found',
            'access_token_status': 'not_found',
            'token_details': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # If we have the actual request object, analyze the actual tokens
        if request:
            # Check for refresh token
            refresh_token = request.COOKIES.get('refresh_token') or request.COOKIES.get('refresh')
            if refresh_token:
                analysis['refresh_token_status'] = self._analyze_token_content(refresh_token, 'refresh')
                analysis['token_details']['refresh_token'] = 'Token found and analyzed'
            
            # Check for access token
            access_token = request.COOKIES.get('access_token') or request.COOKIES.get('access')
            if access_token:
                analysis['access_token_status'] = self._analyze_token_content(access_token, 'access')
                analysis['token_details']['access_token'] = 'Token found and analyzed'
            
            # Check Authorization header as fallback
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                bearer_token = auth_header[7:]
                analysis['bearer_token_status'] = self._analyze_token_content(bearer_token, 'bearer')
                analysis['token_details']['bearer_token'] = 'Token found in Authorization header'
        else:
            # Fallback to basic cookie presence check
            if 'refresh_token' in cookies:
                analysis['refresh_token_status'] = 'present_but_not_analyzed'
                analysis['token_details']['refresh_token'] = 'Cookie present but content not analyzed'
            
            if 'access_token' in cookies:
                analysis['access_token_status'] = 'present_but_not_analyzed'
                analysis['token_details']['access_token'] = 'Cookie present but content not analyzed'
        
        # Add recommendations based on what we found
        if not cookies and not request:
            analysis['issue'] = 'No authentication cookies found'
            analysis['recommendation'] = 'Frontend may not be sending cookies with credentials: "include"'
        elif 'refresh_token' not in cookies and not analysis.get('bearer_token_status'):
            analysis['issue'] = 'Refresh token cookie missing'
            analysis['recommendation'] = 'Check if refresh token was set correctly during login'
        else:
            analysis['issue'] = 'Refresh token present but authentication failed'
            analysis['recommendation'] = 'Token may be expired, malformed, or invalid. Check token validation logic.'
        
        return analysis
    
    def _analyze_token_content(self, token, token_type):
        """Analyze the actual JWT token content safely"""
        try:
            # Decode without verification to inspect claims
            decoded = jwt.decode(token, options={"verify_signature": False})
            
            # Check expiration
            exp = decoded.get('exp')
            now = time.time()
            
            if exp:
                exp_datetime = datetime.fromtimestamp(exp)
                if exp < now:
                    return f'{token_type}_expired'
                else:
                    time_remaining = exp - now
                    return f'{token_type}_valid_expires_in_{int(time_remaining)}s'
            else:
                return f'{token_type}_no_expiration'
                
        except jwt.DecodeError:
            return f'{token_type}_malformed'
        except Exception as e:
            return f'{token_type}_decode_error_{str(e)[:50]}'