import json
import logging
from django.http import JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class CORSDebugMiddleware(MiddlewareMixin):
    """
    Detailed CORS debugging middleware to identify exactly what's happening
    """
    
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