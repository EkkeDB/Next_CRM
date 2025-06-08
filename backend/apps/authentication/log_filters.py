import logging
import time
from collections import defaultdict

class AuthenticationLogFilter(logging.Filter):
    """
    Custom logging filter to suppress repeated authentication failures
    """
    
    def __init__(self):
        super().__init__()
        self._error_cache = defaultdict(list)
        self._suppressed_counts = defaultdict(int)
        self._max_repeats = 3
        self._time_window = 60  # 60 seconds
        self._last_suppression_log = {}
    
    def filter(self, record):
        """
        Filter log records to suppress repeated authentication failures
        """
        # Only filter authentication-related warnings
        if (record.levelno == logging.WARNING and 
            hasattr(record, 'msg') and 
            isinstance(record.msg, str)):
            
            message = record.msg
            
            # Check for authentication-related messages
            auth_patterns = [
                'Unauthorized: /api/auth',
                'POST /api/auth/token/refresh HTTP/1.1" 401',
                'Authentication required'
            ]
            
            is_auth_error = any(pattern in message for pattern in auth_patterns)
            
            if is_auth_error:
                return self._should_log_auth_error(message)
        
        # Allow all other log messages
        return True
    
    def _should_log_auth_error(self, message):
        """Check if this authentication error should be logged"""
        current_time = time.time()
        
        # Create a key based on the message pattern
        key = self._normalize_message(message)
        
        # Clean old entries
        self._error_cache[key] = [
            timestamp for timestamp in self._error_cache[key] 
            if current_time - timestamp < self._time_window
        ]
        
        # Add current error
        self._error_cache[key].append(current_time)
        
        # Check if we should suppress
        if len(self._error_cache[key]) > self._max_repeats:
            self._suppressed_counts[key] += 1
            
            # Log suppression message once per minute
            last_suppression = self._last_suppression_log.get(key, 0)
            if current_time - last_suppression > 60:
                self._last_suppression_log[key] = current_time
                # Create a custom log record for suppression message
                logger = logging.getLogger('apps.authentication.log_filters')
                logger.warning(
                    f"🔁 Repeated authentication failure detected. "
                    f"Suppressing similar logs temporarily. "
                    f"Total occurrences in last {self._time_window}s: {len(self._error_cache[key])}"
                )
            
            return False
        
        return True
    
    def _normalize_message(self, message):
        """Normalize message to create a consistent key for similar errors"""
        # Extract the core error pattern
        if 'Unauthorized: /api/auth' in message:
            return 'unauthorized_api_auth'
        elif 'POST /api/auth/token/refresh HTTP/1.1" 401' in message:
            return 'token_refresh_401'
        elif 'Authentication required' in message:
            return 'authentication_required'
        else:
            # Fallback - use first 50 chars
            return message[:50]