"""
JWT Token Utilities

This module provides functions for creating and validating JWT tokens.

Learning Notes:
- JWT = JSON Web Token (industry standard for authentication)
- Tokens are stateless (no database lookup needed)
- Tokens contain user data (claims) + expiration time
- Tokens are signed with secret key (prevents tampering)
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from config import settings


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary of claims to encode in token (e.g., {"sub": "username"})
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
        
    Example:
        >>> token = create_access_token({"sub": "ahmad"})
        >>> print(token)
        eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhaG1hZCIsImV4cCI6MTY...
        
    Learning Notes:
    - "sub" (subject) claim typically contains username or user ID
    - "exp" (expiration) claim is automatically added
    - Token is signed with SECRET_KEY from config
    - Token format: header.payload.signature (base64 encoded)
    - Token is NOT encrypted (anyone can read it)
    - Token IS signed (cannot be modified without secret key)
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default: 7 days (PRD v2)
        expire = datetime.utcnow() + timedelta(days=settings.access_token_expire_days)
    
    # Add expiration claim
    to_encode.update({"exp": expire})
    
    # Encode token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary of claims if valid, None if invalid
        
    Example:
        >>> token = create_access_token({"sub": "ahmad"})
        >>> payload = decode_access_token(token)
        >>> print(payload)
        {"sub": "ahmad", "exp": 1234567890}
        
    Learning Notes:
    - Validates signature (ensures token wasn't tampered with)
    - Validates expiration (ensures token isn't expired)
    - Returns None if token is invalid or expired
    - Does NOT check if user exists in database (stateless)
    """
    try:
        # Decode and validate token
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        # Token is invalid, expired, or tampered with
        return None


def get_token_expiration_time(expires_delta: Optional[timedelta] = None) -> datetime:
    """
    Calculate token expiration time.
    
    Args:
        expires_delta: Optional custom expiration time
        
    Returns:
        Datetime object representing expiration time
        
    Example:
        >>> exp_time = get_token_expiration_time()
        >>> print(exp_time)
        2025-02-15 10:30:00
    """
    if expires_delta:
        return datetime.utcnow() + expires_delta
    else:
        return datetime.utcnow() + timedelta(days=settings.access_token_expire_days)


# ============================================================================
# LEARNING NOTES: JWT Authentication
# ============================================================================

"""
1. What is JWT?
   - JSON Web Token (RFC 7519)
   - Self-contained authentication token
   - Contains user data + expiration + signature
   - Stateless (no database lookup needed)
   - Industry standard for mobile apps and SPAs

2. JWT Structure:
   Format: header.payload.signature
   
   Header (base64 encoded):
   {
     "alg": "HS256",  # Algorithm
     "typ": "JWT"     # Type
   }
   
   Payload (base64 encoded):
   {
     "sub": "ahmad",           # Subject (username)
     "exp": 1234567890,        # Expiration timestamp
     "iat": 1234567890,        # Issued at timestamp
     "custom_claim": "value"   # Any custom data
   }
   
   Signature (HMAC-SHA256):
   HMACSHA256(
     base64UrlEncode(header) + "." + base64UrlEncode(payload),
     secret_key
   )

3. How JWT Works:
   Login Flow:
   1. User submits username + password
   2. Backend verifies credentials
   3. Backend creates JWT with user data
   4. Backend returns JWT to client
   5. Client stores JWT (localStorage, secure storage)
   
   Authenticated Request Flow:
   1. Client sends JWT in Authorization header
   2. Backend decodes and validates JWT
   3. Backend extracts user data from JWT
   4. Backend processes request
   5. No database lookup needed!

4. JWT vs Session Cookies:
   JWT (Stateless):
   ✅ No server-side storage needed
   ✅ Scales horizontally (any server can validate)
   ✅ Works across domains
   ✅ Perfect for mobile apps
   ❌ Cannot revoke tokens (until expiration)
   ❌ Larger payload size
   
   Session Cookies (Stateful):
   ✅ Can revoke sessions immediately
   ✅ Smaller payload size
   ❌ Requires server-side storage (Redis, DB)
   ❌ Harder to scale horizontally
   ❌ Doesn't work well with mobile apps

5. Security Considerations:
   ✅ DO:
   - Use HTTPS (prevents token interception)
   - Set reasonable expiration time (30 days for this project)
   - Use strong secret key (32+ random characters)
   - Validate signature on every request
   - Check expiration time
   
   ❌ DON'T:
   - Store sensitive data in JWT (it's readable!)
   - Use JWT for sensitive operations (use short-lived tokens)
   - Share secret key
   - Use weak algorithms (MD5, SHA1)
   - Store JWT in localStorage (XSS risk - use secure storage on mobile)

6. Simplified JWT for Student Project:
   Standard Production JWT:
   - Short-lived access tokens (15 minutes)
   - Long-lived refresh tokens (7 days)
   - Token rotation on refresh
   - Token blacklist for logout
   
   Our Simplified JWT:
   - Long-lived access tokens (30 days)
   - No refresh tokens
   - No token blacklist
   - Simpler implementation
   - Good enough for demo/learning

7. Common JWT Claims:
   Standard Claims (optional but recommended):
   - "sub" (subject): User identifier (username or user ID)
   - "exp" (expiration): Expiration timestamp
   - "iat" (issued at): Token creation timestamp
   - "iss" (issuer): Who created the token
   - "aud" (audience): Who should accept the token
   
   Custom Claims (your choice):
   - "user_id": Database user ID
   - "role": User role (admin, farmer)
   - "email": User email
   - Any other non-sensitive data

8. Authorization Header Format:
   Standard format:
   Authorization: Bearer <token>
   
   Example:
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhaG1hZCIsImV4cCI6MTY...

9. Error Handling:
   Common JWT errors:
   - ExpiredSignatureError: Token has expired
   - JWTDecodeError: Token is malformed
   - InvalidSignatureError: Token signature is invalid
   - InvalidTokenError: Generic token error
   
   All handled by returning None in decode_access_token()

10. Testing JWT:
    You can decode JWT tokens at https://jwt.io
    - Paste your token
    - See header and payload
    - Verify signature (paste secret key)
    - Check expiration time

Example Usage in Your Code:
    # Login endpoint
    from backend.utils.security import create_access_token
    from backend.utils.password import verify_password
    
    # Verify password
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    
    # Create token
    access_token = create_access_token({"sub": user.username})
    
    # Return token
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 30 * 24 * 60 * 60  # 30 days in seconds
    }
    
    # Protected endpoint
    from backend.utils.security import decode_access_token
    
    # Extract token from header
    token = request.headers.get("Authorization").replace("Bearer ", "")
    
    # Decode token
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(401, "Invalid or expired token")
    
    # Get username from token
    username = payload.get("sub")
    
    # Get user from database
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(401, "User not found")
    
    # User is authenticated!
    return {"message": f"Hello {user.username}!"}
"""
