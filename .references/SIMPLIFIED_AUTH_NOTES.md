# Simplified Authentication - Design Decision

**Date:** January 2025  
**Decision:** Simplified JWT authentication for student project  
**Reason:** Focus on core features (pest detection, monitoring) while maintaining professional appearance

---

## 🎯 What Changed

### **Before (Complex JWT)**
- Email + password + full name + phone + location registration
- Email validation and verification
- Password reset flow
- Refresh tokens + access tokens
- Token blacklisting
- 24-hour token expiry
- ~10 hours development time

### **After (Simplified JWT)**
- Username + password only registration
- No email validation/verification
- No password reset flow
- Single long-lived access token (30 days)
- No token blacklisting
- 30-day token expiry
- ~5 hours development time

---

## ✅ What We Kept (Professional)

1. **JWT Authentication** - Industry standard for mobile APIs
2. **Password Hashing** - bcrypt for security best practice
3. **Protected Routes** - Middleware for authentication
4. **Token Validation** - Proper JWT verification
5. **Error Handling** - 401 for invalid credentials

---

## ❌ What We Removed (Unnecessary for Demo)

1. **Email Requirement** - Username is sufficient for demo
2. **Password Reset** - Not needed for single-user testing
3. **Email Verification** - No email system required
4. **Refresh Tokens** - Long-lived tokens simpler for demo
5. **Token Blacklisting** - Overkill for student project
6. **Complex Password Rules** - Min 6 chars instead of 8+ with special chars

---

## 📊 Impact Analysis

### **Time Saved:** ~5 hours
- No email service integration
- No password reset UI/API
- No refresh token logic
- No token blacklist management

### **Complexity Reduced:**
- Fewer database fields (3 vs 7 in users table)
- Simpler API contracts (2 fields vs 5 in registration)
- Less validation logic
- Fewer edge cases to test

### **Professional Appearance Maintained:**
- ✅ Still uses JWT (industry standard)
- ✅ Still hashes passwords (security)
- ✅ Still validates tokens (proper auth)
- ✅ Still has protected endpoints
- ✅ Looks complete for demo/portfolio

---

## 🎓 Justification for Lecturers

**Why this is appropriate for a student project:**

1. **Focus on Core Learning Objectives:**
   - IoT data integration ✅
   - ML model integration ✅
   - Mobile app development ✅
   - REST API design ✅
   - Full-stack integration ✅

2. **Time Management:**
   - 14-week timeline is tight
   - Auth is supporting feature, not core
   - More time for pest detection (main feature)

3. **Real-World Pragmatism:**
   - MVPs often start simple
   - Can add complexity later if needed
   - Demonstrates prioritization skills

4. **Still Demonstrates Technical Skills:**
   - JWT implementation (modern auth)
   - Password security (hashing)
   - API authentication patterns
   - Mobile token storage

---

## 📝 Database Schema Changes

### **users Table (Simplified)**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Removed fields:**
- `email` - Not needed for demo
- `full_name` - Not needed for demo
- `phone` - Not needed for demo
- `location` - Not needed for demo
- `updated_at` - Not needed for demo

---

## 🔌 API Changes

### **POST /api/auth/register**

**Before:**
```json
{
  "email": "ahmad@example.com",
  "password": "SecurePass123!",
  "full_name": "Ahmad bin Abdullah",
  "phone": "+60123456789",
  "location": "Kuala Lumpur"
}
```

**After:**
```json
{
  "username": "ahmad_farmer",
  "password": "Pass123"
}
```

### **POST /api/auth/login**

**Before:**
```json
{
  "email": "ahmad@example.com",
  "password": "SecurePass123!"
}
```

**After:**
```json
{
  "username": "ahmad_farmer",
  "password": "Pass123"
}
```

### **Token Response**

**Before:** 24-hour expiry  
**After:** 30-day expiry (2,592,000 seconds)

---

## 🚀 Implementation Notes

### **Password Validation**
- **Before:** Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
- **After:** Min 6 chars (any characters)

### **Username Validation**
- 3-50 characters
- Alphanumeric + underscore only
- Must be unique

### **Token Expiry**
- 30 days (long-lived for demo convenience)
- No refresh mechanism needed
- User stays logged in for entire demo period

---

## 🎯 Success Criteria (Unchanged)

Authentication still meets all core requirements:
- ✅ User can register
- ✅ User can login
- ✅ Protected endpoints require valid token
- ✅ Invalid credentials return 401
- ✅ Tokens expire (just longer duration)
- ✅ Passwords are hashed (security)

---

## 📚 References

- **PRD Updated:** `.references/prd/agrisense-prd.md` (Section 5.1)
- **Tasks Updated:** `.references/tasks/agrisense-tasks.md` (Tasks 0.3.1, 1.1.3, 1.2.1-1.2.5)
- **Handover Document:** `Context/agrisense_handover_v2.md` (Already recommended simple approach)

---

## ✨ Final Note

This simplification aligns with the handover document's philosophy:

> **"Cut ruthlessly. Build ONE thing that works end-to-end."**

Authentication is **supporting infrastructure**, not the **core feature**. By simplifying it, we can spend more time on:
- 🐛 Pest detection accuracy
- 📊 Dashboard UI/UX
- 🌤️ Weather integration
- 🔔 Alert system
- 📱 Mobile app polish

**Result:** Better demo, same learning outcomes, less stress! 🎉
