"""
Password Hashing Utilities

This module provides functions for securely hashing and verifying passwords.

Learning Notes:
- NEVER store plain text passwords in database
- Use bcrypt for password hashing (industry standard)
- Hashing is one-way (cannot reverse)
- Each hash is unique even for same password (salt)
"""

from passlib.context import CryptContext

# Create password context with bcrypt
# bcrypt automatically handles salting and multiple rounds
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    Args:
        password: Plain text password from user
        
    Returns:
        Hashed password string (safe to store in database)
        
    Example:
        >>> hashed = get_password_hash("mypassword123")
        >>> print(hashed)
        $2b$12$KIXxLVq7V5Z8H3yF5vZ8H3yF5vZ8H3yF5vZ8H3yF5vZ8H3yF5vZ8
        
    Learning Notes:
    - The hash includes the salt (random data)
    - Same password produces different hashes each time
    - Hash is ~60 characters long
    - Format: $2b$[cost]$[salt][hash]
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password: Password entered by user (plain text)
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        >>> hashed = get_password_hash("mypassword123")
        >>> verify_password("mypassword123", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
        
    Learning Notes:
    - This is how you check passwords during login
    - Bcrypt extracts the salt from the hash
    - Hashes the plain password with same salt
    - Compares the two hashes
    - Timing-safe comparison (prevents timing attacks)
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================================
# LEARNING NOTES: Password Security
# ============================================================================

"""
1. Why Hash Passwords?
   - If database is stolen, passwords are still safe
   - Even admins can't see user passwords
   - Industry standard security practice
   - Required by security compliance (GDPR, etc.)

2. What is Bcrypt?
   - Password hashing algorithm
   - Designed to be slow (prevents brute force)
   - Automatically handles salting
   - Adaptive (can increase cost factor over time)

3. What is a Salt?
   - Random data added to password before hashing
   - Prevents rainbow table attacks
   - Each password gets unique salt
   - Salt is stored with hash (not secret)

4. How Bcrypt Works:
   Step 1: Generate random salt
   Step 2: Combine password + salt
   Step 3: Hash multiple times (cost factor = 12 rounds = 4096 iterations)
   Step 4: Store salt + hash together
   
   Format: $2b$12$[22 char salt][31 char hash]
   Example: $2b$12$KIXxLVq7V5Z8H3yF5vZ8H3yF5vZ8H3yF5vZ8H3yF5vZ8H3yF5vZ8

5. Cost Factor (12):
   - Number of rounds = 2^12 = 4096 iterations
   - Higher = more secure but slower
   - 12 is good balance (takes ~0.3 seconds)
   - Can increase over time as computers get faster

6. Common Mistakes to Avoid:
   ❌ Storing plain text passwords
   ❌ Using MD5 or SHA1 (too fast, not secure)
   ❌ Not using salt
   ❌ Using same salt for all passwords
   ❌ Storing salt separately from hash
   
   ✅ Use bcrypt, scrypt, or argon2
   ✅ Let library handle salting
   ✅ Use recommended cost factor
   ✅ Never log or display passwords

7. Login Flow:
   Registration:
   1. User submits password: "mypassword123"
   2. Hash it: get_password_hash("mypassword123")
   3. Store hash in database: "$2b$12$..."
   
   Login:
   1. User submits password: "mypassword123"
   2. Get hash from database: "$2b$12$..."
   3. Verify: verify_password("mypassword123", "$2b$12$...")
   4. Returns True if match, False if wrong password

8. Security Benefits:
   - Database breach: Passwords still safe
   - Timing attacks: Prevented by constant-time comparison
   - Rainbow tables: Prevented by unique salts
   - Brute force: Slowed by cost factor
   - Dictionary attacks: Slowed by cost factor

Example Usage in Your Code:
    # Registration
    from backend.utils.password import get_password_hash
    
    hashed = get_password_hash(user_password)
    user = User(username="ahmad", hashed_password=hashed)
    db.add(user)
    db.commit()
    
    # Login
    from backend.utils.password import verify_password
    
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        # Password correct, create JWT token
        return {"access_token": token}
    else:
        # Wrong password
        raise HTTPException(401, "Invalid credentials")
"""
