"""
Rate limiter implementation for FastAPI endpoints.
"""

import time
from typing import Dict, Optional
from fastapi import Request, HTTPException, status
from collections import defaultdict
import threading


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter.
    Note: This is for demonstration purposes. 
    In production, use Redis or similar for distributed rate limiting.
    """
    
    def __init__(self):
        self._requests: Dict[str, list] = defaultdict(list)
        self._lock = threading.Lock()
    
    def is_allowed(
        self, 
        identifier: str, 
        max_requests: int = 5, 
        window_seconds: int = 60
    ) -> bool:
        """
        Check if the request is allowed based on rate limits.
        
        Args:
            identifier: Unique identifier (e.g., IP address, user ID)
            max_requests: Maximum number of requests allowed in the window
            window_seconds: Time window in seconds
            
        Returns:
            True if request is allowed, False otherwise
        """
        current_time = time.time()
        
        with self._lock:
            # Get the request times for this identifier
            request_times = self._requests[identifier]
            
            # Remove old requests outside the window
            cutoff_time = current_time - window_seconds
            request_times[:] = [req_time for req_time in request_times if req_time > cutoff_time]
            
            # Check if we're within the limit
            if len(request_times) >= max_requests:
                return False
            
            # Add current request
            request_times.append(current_time)
            return True
    
    def get_remaining(
        self, 
        identifier: str, 
        max_requests: int = 5, 
        window_seconds: int = 60
    ) -> int:
        """Get remaining requests in the current window."""
        current_time = time.time()
        
        with self._lock:
            request_times = self._requests[identifier]
            cutoff_time = current_time - window_seconds
            
            # Count valid requests in current window
            valid_requests = sum(1 for req_time in request_times if req_time > cutoff_time)
            return max(0, max_requests - valid_requests)


# Global rate limiter instance
rate_limiter = InMemoryRateLimiter()


def get_client_identifier(request: Request) -> str:
    """
    Get unique identifier for rate limiting.
    Uses X-Forwarded-For header if available, otherwise falls back to remote IP.
    """
    # Check for forwarded IP (useful behind proxies)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Take the first IP in the chain
        return forwarded_for.split(",")[0].strip()
    
    # Fall back to direct client IP
    client_host = getattr(request.client, "host", "unknown")
    return client_host


def rate_limit(max_requests: int = 5, window_seconds: int = 60):
    """
    Rate limiting decorator for FastAPI endpoints.
    
    Args:
        max_requests: Maximum number of requests allowed in the window
        window_seconds: Time window in seconds
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Extract request from args/kwargs
            request: Optional[Request] = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                # Look in kwargs
                request = kwargs.get("request")
            
            if not request:
                # If we can't find request, allow the call (safety fallback)
                return func(*args, **kwargs)
            
            # Get client identifier
            identifier = get_client_identifier(request)
            
            # Check rate limit
            if not rate_limiter.is_allowed(identifier, max_requests, window_seconds):
                remaining_time = window_seconds
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Try again in {remaining_time} seconds.",
                    headers={"X-RateLimit-Limit": str(max_requests)}
                )
            
            # Add rate limit headers
            remaining = rate_limiter.get_remaining(identifier, max_requests, window_seconds)
            
            # Call the original function
            response = func(*args, **kwargs)
            
            # Add headers if response supports it
            if hasattr(response, "headers"):
                response.headers["X-RateLimit-Limit"] = str(max_requests)
                response.headers["X-RateLimit-Remaining"] = str(remaining)
                response.headers["X-RateLimit-Reset"] = str(int(time.time() + window_seconds))
            
            return response
        
        return wrapper
    return decorator


def create_rate_limit_dependency(max_requests: int = 5, window_seconds: int = 60):
    """
    Create a FastAPI dependency for rate limiting.
    
    Usage:
        rate_limit_dep = create_rate_limit_dependency(max_requests=10, window_seconds=60)
        
        @router.post("/endpoint")
        def my_endpoint(request: Request, _: None = Depends(rate_limit_dep)):
            pass
    """
    def rate_limit_dependency(request: Request):
        identifier = get_client_identifier(request)
        
        if not rate_limiter.is_allowed(identifier, max_requests, window_seconds):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds.",
                headers={
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Window": str(window_seconds)
                }
            )
        
        return None
    
    return rate_limit_dependency


# Common rate limit dependencies
auth_rate_limit = create_rate_limit_dependency(max_requests=5, window_seconds=300)  # 5 per 5 minutes for auth
vote_rate_limit = create_rate_limit_dependency(max_requests=20, window_seconds=60)  # 20 per minute for voting
general_rate_limit = create_rate_limit_dependency(max_requests=100, window_seconds=60)  # 100 per minute general