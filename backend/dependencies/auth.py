"""
Authentication Dependencies

This module provides FastAPI dependencies for authentication.

Learning Notes:
- Dependencies are reusable functions that run before endpoint handlers
- Used to extract and validate authentication tokens
- Automatically handle errors and return appropriate HTTP responses
- Can be injected into any endpoint that requires authentication
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.utils.security import decode_access_token


# HTTP Bearer token scheme (Authorization: Bearer <token>)
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency to get the current authenticated user.
    
    This function:
    1. Extracts JWT token from Authorization header
    2. Validates and decodes the token
    3. Retrieves user from database
    4. Returns user object or raises 401 error
    
    Args:
        credentials: HTTP Bearer credentials (automatically extracted by FastAPI)
        db: Database session (automatically injected by FastAPI)
        
    Returns:
        User object if authentication successful
        
    Raises:
        HTTPException 401: If token is invalid, expired, or user not found
        
    Example Usage:
        @app.get("/api/protected")
        def protected_endpoint(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello {current_user.username}!"}
            
    Learning Notes:
    - This is a FastAPI dependency (reusable function)
    - Depends() tells FastAPI to inject this function
    - HTTPBearer() automatically extracts "Authorization: Bearer <token>"
    - If token is missing, FastAPI returns 401 automatically
    - If token is invalid, we raise HTTPException 401
    - If user not found, we raise HTTPException 401
    - The User object is passed to the endpoint handler
    """
    
    # Extract token from credentials
    token = credentials.credentials
    
    # Decode and validate token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract username from token payload
    username: Optional[str] = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Optional authentication dependency.
    
    Returns user if token is provided and valid, None otherwise.
    Does NOT raise error if token is missing or invalid.
    
    Useful for endpoints that work differently for authenticated vs anonymous users.
    
    Args:
        credentials: Optional HTTP Bearer credentials
        db: Database session
        
    Returns:
        User object if authenticated, None otherwise
        
    Example Usage:
        @app.get("/api/public")
        def public_endpoint(current_user: Optional[User] = Depends(get_current_user_optional)):
            if current_user:
                return {"message": f"Hello {current_user.username}!"}
            else:
                return {"message": "Hello guest!"}
    """
    
    # No token provided
    if credentials is None:
        return None
    
    # Extract and decode token
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        return None
    
    # Extract username
    username: Optional[str] = payload.get("sub")
    if username is None:
        return None
    
    # Get user from database
    user = db.query(User).filter(User.username == username).first()
    return user


# ============================================================================
# LEARNING NOTES: FastAPI Dependencies
# ============================================================================

"""
1. What are FastAPI Dependencies?
   - Reusable functions that run before endpoint handlers
   - Used for authentication, database connections, validation, etc.
   - Automatically injected by FastAPI
   - Can depend on other dependencies (dependency chain)
   - Handle errors and return appropriate responses

2. How Dependencies Work:
   Step 1: Client sends request to endpoint
   Step 2: FastAPI runs all dependencies first
   Step 3: Dependencies return values or raise errors
   Step 4: If all dependencies succeed, endpoint handler runs
   Step 5: Endpoint handler receives dependency results as parameters
   
   Example:
   @app.get("/api/profile")
   def get_profile(current_user: User = Depends(get_current_user)):
       # current_user is the result of get_current_user() dependency
       return {"username": current_user.username}

3. HTTPBearer Security Scheme:
   - Automatically extracts "Authorization: Bearer <token>" header
   - Returns HTTPAuthorizationCredentials object
   - credentials.credentials contains the token string
   - Raises 401 if header is missing (unless auto_error=False)
   
   Example header:
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

4. Dependency Injection Chain:
   get_current_user depends on:
   - security (HTTPBearer) → extracts token from header
   - get_db → provides database session
   
   FastAPI automatically:
   1. Calls HTTPBearer() to extract token
   2. Calls get_db() to get database session
   3. Passes both to get_current_user()
   4. Passes User object to endpoint handler

5. Error Handling:
   Dependencies can raise HTTPException:
   - 401 Unauthorized: Invalid/expired token, user not found
   - 403 Forbidden: User doesn't have permission
   - 404 Not Found: Resource not found
   - 422 Unprocessable Entity: Validation error
   
   FastAPI automatically converts these to proper HTTP responses

6. Required vs Optional Authentication:
   Required (get_current_user):
   - Raises 401 if token missing or invalid
   - Use for protected endpoints
   
   Optional (get_current_user_optional):
   - Returns None if token missing or invalid
   - Use for public endpoints with optional features

7. Testing Protected Endpoints:
   # Get token
   response = client.post("/api/auth/login", json={
       "username": "ahmad",
       "password": "password123"
   })
   token = response.json()["access_token"]
   
   # Call protected endpoint
   response = client.get("/api/profile", headers={
       "Authorization": f"Bearer {token}"
   })

8. Common Patterns:
   # Require authentication
   @app.get("/api/profile")
   def get_profile(current_user: User = Depends(get_current_user)):
       return {"username": current_user.username}
   
   # Optional authentication
   @app.get("/api/posts")
   def get_posts(current_user: Optional[User] = Depends(get_current_user_optional)):
       if current_user:
           # Show personalized posts
           return get_user_posts(current_user.id)
       else:
           # Show public posts
           return get_public_posts()
   
   # Multiple dependencies
   @app.post("/api/admin/users")
   def create_user(
       current_user: User = Depends(get_current_user),
       is_admin: bool = Depends(require_admin),
       db: Session = Depends(get_db)
   ):
       # Only admins can create users
       return create_new_user(db)

9. Dependency Caching:
   FastAPI caches dependency results within a single request:
   - If multiple endpoints use get_current_user, it only runs once
   - Database session is reused across dependencies
   - Improves performance

10. Best Practices:
    ✅ DO:
    - Use dependencies for authentication
    - Use dependencies for database sessions
    - Use dependencies for validation
    - Keep dependencies simple and focused
    - Raise HTTPException for errors
    
    ❌ DON'T:
    - Put business logic in dependencies
    - Make dependencies too complex
    - Return None from required dependencies
    - Catch exceptions without re-raising

Example Usage in Your Code:
    # Protected endpoint (requires authentication)
    @router.get("/api/sensors/current")
    def get_current_sensors(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        # current_user is guaranteed to be a valid User object
        # If token is invalid, FastAPI returns 401 automatically
        sensors = db.query(SensorReading).filter(
            SensorReading.user_id == current_user.id
        ).first()
        return sensors
    
    # Public endpoint (optional authentication)
    @router.get("/api/weather/current")
    def get_current_weather(
        current_user: Optional[User] = Depends(get_current_user_optional)
    ):
        # current_user might be None (anonymous user)
        if current_user:
            # Use user's location
            location = current_user.location
        else:
            # Use default location
            location = "Kuala Lumpur"
        
        return get_weather(location)
"""
