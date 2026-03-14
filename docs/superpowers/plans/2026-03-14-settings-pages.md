# Settings Pages + Farm Management Fix — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build out 5 incomplete settings features: Edit Profile (with email), Import Dataset (CSV sensor data), Farm Management UX fix, Help & Support, and About AgriSense.

**Architecture:** Backend-first for features needing API changes (Edit Profile, Import Dataset), then mobile-only features. Each task is self-contained and commits independently. Backend uses FastAPI + SQLAlchemy + Alembic. Mobile uses Flutter + Provider.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy, Alembic, Flutter/Dart, Provider, file_picker, url_launcher

**Spec:** `docs/superpowers/specs/2026-03-14-settings-pages-design.md`

---

## Chunk 1: Edit Profile (Backend)

### Task 1: Add email column to User model + migration

**Files:**
- Modify: `backend/models/user.py`
- Modify: `backend/schemas/auth.py`
- Create: `backend/alembic/versions/<auto>_add_email_to_users.py` (via alembic)

- [ ] **Step 1: Add email column to User model**

In `backend/models/user.py`, add after `full_name` column (after line 65):

```python
email = Column(
    String(255),
    nullable=True,
    unique=True,
    index=True,
    comment="User email address (required for new signups, optional for existing users)"
)
```

Also update `to_dict()` method to include email — add `"email": self.email,` after the `"full_name"` line.

- [ ] **Step 2: Add email to auth schemas**

In `backend/schemas/auth.py`:

Add email to `UserRegister` (after `full_name` field, around line 60). **Note:** email is `Optional` to avoid breaking existing clients — the mobile sign-up page will make it required via UI validation:
```python
email: Optional[str] = Field(
    None,
    max_length=255,
    description="User email address (required for new signups)"
)

@field_validator('email')
@classmethod
def validate_email(cls, v: Optional[str]) -> Optional[str]:
    """Basic email format validation."""
    if v is None or v.strip() == '':
        return None
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, v):
        raise ValueError('Invalid email format')
    return v.lower()
```

Add email to `UserResponse` (after `full_name` field, around line 161):
```python
email: Optional[str] = Field(None, description="User email address")
```

Update `UserResponse` example to include `"email": "ahmad@example.com"`.

- [ ] **Step 3: Generate and apply Alembic migration**

Run:
```bash
cd backend
alembic revision --autogenerate -m "Add email column to users table"
```

Review the generated migration file, then apply:
```bash
alembic upgrade head
```

- [ ] **Step 4: Commit**

```bash
git add backend/models/user.py backend/schemas/auth.py backend/alembic/versions/
git commit -m "feat: add email column to User model with migration"
```

---

### Task 2: Add profile update and password change endpoints

**Files:**
- Modify: `backend/schemas/auth.py`
- Modify: `backend/routers/auth.py`

- [ ] **Step 1: Add UserUpdate and PasswordChange schemas**

In `backend/schemas/auth.py`, add before `UserResponse` class:

```python
class UserUpdate(BaseModel):
    """Schema for updating user profile. All fields optional."""
    full_name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=255)
    farm_location_name: Optional[str] = Field(None, max_length=100)
    farm_location_lat: Optional[float] = Field(None, ge=-90, le=90)
    farm_location_lng: Optional[float] = Field(None, ge=-180, le=180)
    crop_type: Optional[str] = Field(None)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == '':
            return None
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('crop_type')
    @classmethod
    def validate_crop_type_update(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        valid_types = ["rice", "vegetables", "corn", "oil_palm", "rubber"]
        if v.lower() not in valid_types:
            raise ValueError(f'Crop type must be one of: {", ".join(valid_types)}')
        return v.lower()


class PasswordChange(BaseModel):
    """Schema for changing password."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=6, description="New password (min 6 chars)")
```

- [ ] **Step 2: Add PUT /auth/me endpoint**

In `backend/routers/auth.py`, add the import for `UserUpdate` in the imports line:
```python
from schemas.auth import UserRegister, UserLogin, Token, UserResponse, UserUpdate, PasswordChange
```

Add after the `get_me` endpoint:

```python
@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
)
async def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the current user's profile fields."""
    # Check email uniqueness if email is being updated
    if user_data.email is not None:
        existing = db.query(User).filter(
            User.email == user_data.email,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already in use by another account"
            )

    # Update only provided fields
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user
```

- [ ] **Step 3: Add POST /auth/change-password endpoint**

Add after the `update_me` endpoint in `backend/routers/auth.py`:

```python
@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change password",
)
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change the current user's password."""
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}
```

- [ ] **Step 4: Test endpoints manually**

Run: `cd backend && python run.py`

Test with curl or Swagger UI at `http://localhost:8000/docs`:
- PUT /api/v1/auth/me with a valid token
- POST /api/v1/auth/change-password with correct/incorrect current password

- [ ] **Step 5: Commit**

```bash
git add backend/schemas/auth.py backend/routers/auth.py
git commit -m "feat: add profile update and password change endpoints"
```

---

### Task 3: Update registration to include email

**Files:**
- Modify: `backend/routers/auth.py`

- [ ] **Step 1: Update register endpoint to pass email**

In `backend/routers/auth.py`, in the `register` function, add email uniqueness check after the username check (after line 64):

```python
# Check if email already exists
if user_data.email:
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
```

And add `email=user_data.email` to the `User()` constructor (after `full_name` line):

```python
email=user_data.email,
```

- [ ] **Step 2: Commit**

```bash
git add backend/routers/auth.py
git commit -m "feat: include email in user registration flow"
```

---

## Chunk 2: Edit Profile (Mobile)

### Task 4: Update mobile User model and AuthService

**Files:**
- Modify: `mobile/lib/models/user.dart`
- Modify: `mobile/lib/services/auth_service.dart`
- Modify: `mobile/lib/utils/api_constants.dart`

- [ ] **Step 1: Add email to User model**

In `mobile/lib/models/user.dart`, add `email` field:

```dart
/// User model matching backend UserResponse schema.
class User {
  final int id;
  final String username;
  final String? fullName;
  final String? email;
  final String farmLocationName;
  final double farmLocationLat;
  final double farmLocationLng;
  final String cropType;
  final bool isActive;
  final DateTime createdAt;

  User({
    required this.id,
    required this.username,
    this.fullName,
    this.email,
    required this.farmLocationName,
    required this.farmLocationLat,
    required this.farmLocationLng,
    required this.cropType,
    required this.isActive,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      username: json['username'] as String,
      fullName: json['full_name'] as String?,
      email: json['email'] as String?,
      farmLocationName: json['farm_location_name'] as String,
      farmLocationLat: (json['farm_location_lat'] as num).toDouble(),
      farmLocationLng: (json['farm_location_lng'] as num).toDouble(),
      cropType: json['crop_type'] as String,
      isActive: json['is_active'] as bool,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'full_name': fullName,
      'email': email,
      'farm_location_name': farmLocationName,
      'farm_location_lat': farmLocationLat,
      'farm_location_lng': farmLocationLng,
      'crop_type': cropType,
      'is_active': isActive,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
```

- [ ] **Step 2: Add API constants**

In `mobile/lib/utils/api_constants.dart`, add after the `me` constant:

```dart
static const String profileUpdate = '$apiPrefix/auth/me';
static const String changePassword = '$apiPrefix/auth/change-password';
```

- [ ] **Step 3: Add updateProfile and changePassword to AuthService**

In `mobile/lib/services/auth_service.dart`, add these methods:

```dart
/// Update the current user's profile.
static Future<User> updateProfile({
  required String token,
  String? fullName,
  String? email,
  String? farmLocationName,
  double? farmLocationLat,
  double? farmLocationLng,
  String? cropType,
}) async {
  final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.profileUpdate}');

  final body = <String, dynamic>{};
  if (fullName != null) body['full_name'] = fullName;
  if (email != null) body['email'] = email;
  if (farmLocationName != null) body['farm_location_name'] = farmLocationName;
  if (farmLocationLat != null) body['farm_location_lat'] = farmLocationLat;
  if (farmLocationLng != null) body['farm_location_lng'] = farmLocationLng;
  if (cropType != null) body['crop_type'] = cropType;

  final response = await appHttpClient.put(
    url,
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
    body: json.encode(body),
  );

  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    return User.fromJson(data);
  } else if (response.statusCode == 401) {
    throw Exception('Session expired. Please login again.');
  } else if (response.statusCode == 409) {
    throw Exception('Email already in use by another account');
  } else {
    final data = json.decode(response.body);
    throw Exception(data['detail'] ?? 'Failed to update profile');
  }
}

/// Change the current user's password.
static Future<void> changePassword({
  required String token,
  required String currentPassword,
  required String newPassword,
}) async {
  final url = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.changePassword}');

  final response = await appHttpClient.post(
    url,
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
    body: json.encode({
      'current_password': currentPassword,
      'new_password': newPassword,
    }),
  );

  if (response.statusCode == 200) {
    return;
  } else if (response.statusCode == 400) {
    throw Exception('Current password is incorrect');
  } else if (response.statusCode == 401) {
    throw Exception('Session expired. Please login again.');
  } else {
    final data = json.decode(response.body);
    throw Exception(data['detail'] ?? 'Failed to change password');
  }
}
```

- [ ] **Step 4: Add updateProfile and changePassword to AuthProvider**

In `mobile/lib/providers/auth_provider.dart`, add before the `logout()` method:

```dart
/// Update user profile.
Future<bool> updateProfile({
  String? fullName,
  String? email,
  String? farmLocationName,
  double? farmLocationLat,
  double? farmLocationLng,
  String? cropType,
}) async {
  if (_token == null) return false;

  _isLoading = true;
  _errorMessage = null;
  notifyListeners();

  try {
    final updatedUser = await AuthService.updateProfile(
      token: _token!,
      fullName: fullName,
      email: email,
      farmLocationName: farmLocationName,
      farmLocationLat: farmLocationLat,
      farmLocationLng: farmLocationLng,
      cropType: cropType,
    );
    _user = updatedUser;
    _isLoading = false;
    notifyListeners();
    return true;
  } catch (e) {
    _errorMessage = e.toString().replaceFirst('Exception: ', '');
    _isLoading = false;
    notifyListeners();
    return false;
  }
}

/// Change user password.
Future<bool> changePassword({
  required String currentPassword,
  required String newPassword,
}) async {
  if (_token == null) return false;

  _isLoading = true;
  _errorMessage = null;
  notifyListeners();

  try {
    await AuthService.changePassword(
      token: _token!,
      currentPassword: currentPassword,
      newPassword: newPassword,
    );
    _isLoading = false;
    notifyListeners();
    return true;
  } catch (e) {
    _errorMessage = e.toString().replaceFirst('Exception: ', '');
    _isLoading = false;
    notifyListeners();
    return false;
  }
}
```

- [ ] **Step 5: Commit**

```bash
git add mobile/lib/models/user.dart mobile/lib/services/auth_service.dart mobile/lib/utils/api_constants.dart mobile/lib/providers/auth_provider.dart
git commit -m "feat: add profile update and password change to mobile auth layer"
```

---

### Task 5: Create Edit Profile page

**Files:**
- Create: `mobile/lib/pages/edit_profile_page.dart`
- Modify: `mobile/lib/main.dart`
- Modify: `mobile/lib/pages/settings_page.dart`

- [ ] **Step 1: Create EditProfilePage**

Create `mobile/lib/pages/edit_profile_page.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fyp_prototype/providers/auth_provider.dart';
import 'package:fyp_prototype/widgets/custom_app_bar.dart';
import 'package:google_fonts/google_fonts.dart';

class EditProfilePage extends StatefulWidget {
  const EditProfilePage({super.key});

  @override
  State<EditProfilePage> createState() => _EditProfilePageState();
}

class _EditProfilePageState extends State<EditProfilePage> {
  final _profileFormKey = GlobalKey<FormState>();
  final _passwordFormKey = GlobalKey<FormState>();

  late TextEditingController _fullNameController;
  late TextEditingController _emailController;
  late TextEditingController _farmLocationController;
  late TextEditingController _latController;
  late TextEditingController _lngController;
  String _selectedCropType = 'rice';

  final _currentPasswordController = TextEditingController();
  final _newPasswordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  bool _isSavingProfile = false;
  bool _isChangingPassword = false;

  static const Map<String, Map<String, double>> _malaysianLocations = {
    'Perlis': {'lat': 6.4449, 'lng': 100.2048},
    'Kedah': {'lat': 6.1184, 'lng': 100.3685},
    'Penang': {'lat': 5.4164, 'lng': 100.3327},
    'Perak': {'lat': 4.5921, 'lng': 101.0901},
    'Selangor': {'lat': 3.0738, 'lng': 101.5183},
    'Negeri Sembilan': {'lat': 2.7258, 'lng': 101.9424},
    'Melaka': {'lat': 2.1896, 'lng': 102.2501},
    'Johor': {'lat': 1.4854, 'lng': 103.7618},
    'Pahang': {'lat': 3.8126, 'lng': 103.3256},
    'Terengganu': {'lat': 5.3117, 'lng': 103.1324},
    'Kelantan': {'lat': 6.1254, 'lng': 102.2381},
    'Sabah': {'lat': 5.9788, 'lng': 116.0753},
    'Sarawak': {'lat': 1.5533, 'lng': 110.3592},
    'Kuala Lumpur': {'lat': 3.1390, 'lng': 101.6869},
  };

  final List<Map<String, String>> _cropTypes = [
    {'value': 'rice', 'label': 'Rice'},
    {'value': 'vegetables', 'label': 'Vegetables'},
    {'value': 'corn', 'label': 'Corn'},
    {'value': 'oil_palm', 'label': 'Oil Palm'},
    {'value': 'rubber', 'label': 'Rubber'},
  ];

  @override
  void initState() {
    super.initState();
    final user = context.read<AuthProvider>().user;
    _fullNameController = TextEditingController(text: user?.fullName ?? '');
    _emailController = TextEditingController(text: user?.email ?? '');
    _farmLocationController = TextEditingController(text: user?.farmLocationName ?? 'Kuala Lumpur');
    _latController = TextEditingController(text: user?.farmLocationLat.toString() ?? '');
    _lngController = TextEditingController(text: user?.farmLocationLng.toString() ?? '');
    _selectedCropType = user?.cropType ?? 'rice';
  }

  @override
  void dispose() {
    _fullNameController.dispose();
    _emailController.dispose();
    _farmLocationController.dispose();
    _latController.dispose();
    _lngController.dispose();
    _currentPasswordController.dispose();
    _newPasswordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _saveProfile() async {
    if (!_profileFormKey.currentState!.validate()) return;

    setState(() => _isSavingProfile = true);

    final authProvider = context.read<AuthProvider>();
    final coords = _malaysianLocations[_farmLocationController.text];

    final success = await authProvider.updateProfile(
      fullName: _fullNameController.text.trim(),
      email: _emailController.text.trim().isNotEmpty ? _emailController.text.trim() : null,
      farmLocationName: _farmLocationController.text,
      farmLocationLat: coords?['lat'] ?? double.tryParse(_latController.text),
      farmLocationLng: coords?['lng'] ?? double.tryParse(_lngController.text),
      cropType: _selectedCropType,
    );

    setState(() => _isSavingProfile = false);

    if (!mounted) return;

    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Profile updated successfully'), backgroundColor: Color(0xFF4BAE4F)),
      );
      Navigator.pop(context);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(authProvider.errorMessage ?? 'Failed to update profile'), backgroundColor: Colors.red),
      );
      authProvider.clearError();
    }
  }

  Future<void> _changePassword() async {
    if (!_passwordFormKey.currentState!.validate()) return;

    setState(() => _isChangingPassword = true);

    final authProvider = context.read<AuthProvider>();
    final success = await authProvider.changePassword(
      currentPassword: _currentPasswordController.text,
      newPassword: _newPasswordController.text,
    );

    setState(() => _isChangingPassword = false);

    if (!mounted) return;

    if (success) {
      _currentPasswordController.clear();
      _newPasswordController.clear();
      _confirmPasswordController.clear();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Password changed successfully'), backgroundColor: Color(0xFF4BAE4F)),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(authProvider.errorMessage ?? 'Failed to change password'), backgroundColor: Colors.red),
      );
      authProvider.clearError();
    }
  }

  InputDecoration _inputDecoration(String label) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: Color(0xFF828282), fontSize: 14),
      contentPadding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: const BorderSide(color: Color(0xFFE0E0E0)),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: const BorderSide(color: Color(0xFF53AD64)),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: const BorderSide(color: Colors.red),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Edit Profile', subtitle: 'Update your personal information'),
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Profile section
            Text('Personal Information', style: GoogleFonts.scheherazadeNew(fontSize: 20, fontWeight: FontWeight.w500)),
            const SizedBox(height: 15),
            Form(
              key: _profileFormKey,
              child: Column(
                children: [
                  TextFormField(
                    controller: _fullNameController,
                    decoration: _inputDecoration('Full Name'),
                  ),
                  const SizedBox(height: 12),
                  TextFormField(
                    controller: _emailController,
                    decoration: _inputDecoration('Email'),
                    keyboardType: TextInputType.emailAddress,
                  ),
                  const SizedBox(height: 12),
                  // Farm Location Dropdown
                  DropdownButtonFormField<String>(
                    value: _malaysianLocations.containsKey(_farmLocationController.text)
                        ? _farmLocationController.text
                        : 'Kuala Lumpur',
                    decoration: _inputDecoration('Farm Location'),
                    items: _malaysianLocations.keys.map((name) {
                      return DropdownMenuItem<String>(value: name, child: Text(name));
                    }).toList(),
                    onChanged: (value) {
                      if (value != null) {
                        setState(() {
                          _farmLocationController.text = value;
                          final coords = _malaysianLocations[value]!;
                          _latController.text = coords['lat']!.toString();
                          _lngController.text = coords['lng']!.toString();
                        });
                      }
                    },
                  ),
                  const SizedBox(height: 12),
                  // Crop Type Dropdown
                  DropdownButtonFormField<String>(
                    value: _cropTypes.any((c) => c['value'] == _selectedCropType) ? _selectedCropType : 'rice',
                    decoration: _inputDecoration('Crop Type'),
                    items: _cropTypes.map((crop) {
                      return DropdownMenuItem<String>(value: crop['value'], child: Text(crop['label']!));
                    }).toList(),
                    onChanged: (value) {
                      if (value != null) {
                        setState(() => _selectedCropType = value);
                      }
                    },
                  ),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _isSavingProfile ? null : _saveProfile,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF4BAE4F),
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                      child: _isSavingProfile
                          ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                          : const Text('Save Changes', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 30),
            const Divider(),
            const SizedBox(height: 20),

            // Password section
            Text('Change Password', style: GoogleFonts.scheherazadeNew(fontSize: 20, fontWeight: FontWeight.w500)),
            const SizedBox(height: 15),
            Form(
              key: _passwordFormKey,
              child: Column(
                children: [
                  TextFormField(
                    controller: _currentPasswordController,
                    decoration: _inputDecoration('Current Password'),
                    obscureText: true,
                    validator: (val) {
                      if (val == null || val.isEmpty) return 'Please enter your current password';
                      return null;
                    },
                  ),
                  const SizedBox(height: 12),
                  TextFormField(
                    controller: _newPasswordController,
                    decoration: _inputDecoration('New Password'),
                    obscureText: true,
                    validator: (val) {
                      if (val == null || val.isEmpty) return 'Please enter a new password';
                      if (val.length < 6) return 'Password must be at least 6 characters';
                      return null;
                    },
                  ),
                  const SizedBox(height: 12),
                  TextFormField(
                    controller: _confirmPasswordController,
                    decoration: _inputDecoration('Confirm New Password'),
                    obscureText: true,
                    validator: (val) {
                      if (val == null || val.isEmpty) return 'Please confirm your new password';
                      if (val != _newPasswordController.text) return 'Passwords do not match';
                      return null;
                    },
                  ),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: double.infinity,
                    child: OutlinedButton(
                      onPressed: _isChangingPassword ? null : _changePassword,
                      style: OutlinedButton.styleFrom(
                        foregroundColor: const Color(0xFF4BAE4F),
                        side: const BorderSide(color: Color(0xFF4BAE4F)),
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                      ),
                      child: _isChangingPassword
                          ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFF4BAE4F)))
                          : const Text('Change Password', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }
}
```

- [ ] **Step 2: Add route and wire up settings button**

In `mobile/lib/main.dart`, add import at top:
```dart
import 'package:fyp_prototype/pages/edit_profile_page.dart';
```

Add route in the routes map:
```dart
'/editProfile': (context) => EditProfilePage(),
```

In `mobile/lib/pages/settings_page.dart`, replace the Edit Profile button's `onPressed`:
```dart
onPressed: () {
  Navigator.pushNamed(context, '/editProfile');
},
```

- [ ] **Step 3: Add email field to sign-up page**

In `mobile/lib/pages/sign_up_page.dart`:

Add a controller in the state class:
```dart
final TextEditingController emailController = TextEditingController();
```

Dispose it in `dispose()`:
```dart
emailController.dispose();
```

Add email field after the username field (after the username `CustomFormField`, around line 188):
```dart
// Email
CustomFormField(
  controller: emailController,
  hintText: 'Enter your email address',
  validator: (val) {
    if (val == null || val.isEmpty) {
      return 'Please enter your email';
    }
    final emailRegex = RegExp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');
    if (!emailRegex.hasMatch(val)) {
      return 'Please enter a valid email address';
    }
    return null;
  },
),
```

In the `_handleSignUp` method, update the `authProvider.register` call to pass email. This requires updating the `AuthProvider.register` method and `AuthService.register` method to accept an `email` parameter.

In `mobile/lib/services/auth_service.dart`, add `String? email` parameter to `register()` and include in body:
```dart
if (email != null) {
  body['email'] = email;
}
```

In `mobile/lib/providers/auth_provider.dart`, add `String? email` parameter to `register()` and pass it through.

In the sign-up page's `_handleSignUp`, add:
```dart
email: emailController.text.trim(),
```

- [ ] **Step 4: Commit**

```bash
git add mobile/lib/pages/edit_profile_page.dart mobile/lib/main.dart mobile/lib/pages/settings_page.dart mobile/lib/pages/sign_up_page.dart mobile/lib/services/auth_service.dart mobile/lib/providers/auth_provider.dart
git commit -m "feat: add Edit Profile page with email support and sign-up email field"
```

---

## Chunk 3: Import Dataset (Backend + Mobile)

### Task 6: Add CSV import endpoint to backend

**Files:**
- Modify: `backend/routers/sensor.py`

- [ ] **Step 1: Add import endpoint**

Add to imports at top of `backend/routers/sensor.py`:
```python
from fastapi import UploadFile, File
import csv
import io
```

Add this endpoint **before** any `/{sensor_data_id}` parametric routes (to avoid route matching conflicts):

```python
@router.post("/import", status_code=200)
async def import_sensor_data(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Import sensor data from a CSV file.

    Accepted columns: temperature, relative_humidity (alias: humidity),
    soil_moisture, rain (alias: rainfall), wind_speed, solar_radiation,
    soil_temperature, weather_code, timestamp.

    Required per row: temperature, relative_humidity, soil_moisture.
    Missing optional columns default to 0.0 or NULL.
    Max 10,000 rows per import.
    """
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    content = await file.read()
    # Handle UTF-8 BOM
    text = content.decode('utf-8-sig')

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV file is empty or has no headers")

    # Column aliases
    aliases = {
        'humidity': 'relative_humidity',
        'rainfall': 'rain',
    }

    # Normalize headers
    normalized_fields = []
    for f in reader.fieldnames:
        clean = f.strip().lower()
        normalized_fields.append(aliases.get(clean, clean))

    expected_columns = [
        'temperature', 'relative_humidity', 'soil_moisture',
        'rain', 'wind_speed', 'solar_radiation',
        'soil_temperature', 'weather_code', 'timestamp'
    ]
    required_columns = ['temperature', 'relative_humidity', 'soil_moisture']

    columns_matched = [c for c in expected_columns if c in normalized_fields]
    columns_missing = [c for c in expected_columns if c not in normalized_fields]

    rows_imported = 0
    rows_skipped = 0
    errors = []

    for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
        if rows_imported + rows_skipped >= 10000:
            errors.append({"row": row_num, "message": "Row limit (10,000) reached"})
            break

        # Normalize row keys
        normalized_row = {}
        for key, value in row.items():
            clean_key = key.strip().lower()
            normalized_row[aliases.get(clean_key, clean_key)] = value.strip() if value else None

        # Check required fields
        missing_required = []
        for req in required_columns:
            if req not in normalized_row or not normalized_row[req]:
                missing_required.append(req)

        if missing_required:
            rows_skipped += 1
            errors.append({"row": row_num, "message": f"Missing required fields: {', '.join(missing_required)}"})
            continue

        try:
            # Parse timestamp
            ts = None
            if 'timestamp' in normalized_row and normalized_row['timestamp']:
                ts_str = normalized_row['timestamp']
                for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y']:
                    try:
                        ts = datetime.strptime(ts_str, fmt)
                        break
                    except ValueError:
                        continue
                if ts is None:
                    rows_skipped += 1
                    errors.append({"row": row_num, "message": f"Invalid timestamp format: {ts_str}"})
                    continue

            def safe_float(val, default=None):
                if val is None or val == '':
                    return default
                return float(val)

            def safe_int(val, default=None):
                if val is None or val == '':
                    return default
                return int(float(val))

            reading = SensorReading(
                user_id=current_user.id,
                temperature=safe_float(normalized_row.get('temperature')),
                relative_humidity=safe_float(normalized_row.get('relative_humidity')),
                soil_moisture=safe_float(normalized_row.get('soil_moisture')),
                rain=safe_float(normalized_row.get('rain'), 0.0),
                wind_speed=safe_float(normalized_row.get('wind_speed'), 0.0),
                solar_radiation=safe_float(normalized_row.get('solar_radiation')),
                soil_temperature=safe_float(normalized_row.get('soil_temperature')),
                weather_code=safe_int(normalized_row.get('weather_code')),
            )
            if ts:
                reading.timestamp = ts

            db.add(reading)
            rows_imported += 1
        except (ValueError, TypeError) as e:
            rows_skipped += 1
            errors.append({"row": row_num, "message": str(e)})

    db.commit()

    return {
        "rows_imported": rows_imported,
        "rows_skipped": rows_skipped,
        "columns_matched": columns_matched,
        "columns_missing": columns_missing,
        "errors": errors[:50],  # Limit error list
    }
```

- [ ] **Step 2: Test with curl**

Run: `cd backend && python run.py`

Create a test CSV and try importing via Swagger UI or curl.

- [ ] **Step 3: Commit**

```bash
git add backend/routers/sensor.py
git commit -m "feat: add CSV import endpoint for sensor data"
```

---

### Task 7: Build Import Dataset mobile page

**Files:**
- Modify: `mobile/pubspec.yaml`
- Modify: `mobile/lib/utils/api_constants.dart`
- Modify: `mobile/lib/pages/import_dataset_page.dart`

- [ ] **Step 1: Add file_picker dependency**

In `mobile/pubspec.yaml`, add under dependencies (after `intl: ^0.19.0`):
```yaml
  file_picker: ^8.0.0
```

Run: `cd mobile && flutter pub get`

- [ ] **Step 2: Add API constant**

In `mobile/lib/utils/api_constants.dart`, add:
```dart
static const String sensorImport = '$apiPrefix/sensor/import';
```

- [ ] **Step 3: Rewrite Import Dataset page**

Rewrite `mobile/lib/pages/import_dataset_page.dart`:

```dart
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:fyp_prototype/utils/api_constants.dart';
import 'package:fyp_prototype/utils/token_storage.dart';
import 'package:fyp_prototype/utils/http_client.dart';
import 'package:fyp_prototype/widgets/custom_app_bar.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;

class ImportDatasetPage extends StatefulWidget {
  const ImportDatasetPage({super.key});

  @override
  State<ImportDatasetPage> createState() => _ImportDatasetPageState();
}

class _ImportDatasetPageState extends State<ImportDatasetPage> {
  String? _filePath;
  String? _fileName;
  List<List<String>> _previewRows = [];
  List<String> _headers = [];
  bool _isImporting = false;
  Map<String, dynamic>? _importResult;

  static const List<String> _expectedColumns = [
    'temperature', 'relative_humidity', 'soil_moisture',
    'rain', 'wind_speed', 'solar_radiation',
    'soil_temperature', 'weather_code', 'timestamp',
  ];

  static const List<String> _requiredColumns = [
    'temperature', 'relative_humidity', 'soil_moisture',
  ];

  static const Map<String, String> _aliases = {
    'humidity': 'relative_humidity',
    'rainfall': 'rain',
  };

  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['csv'],
    );

    if (result == null || result.files.single.path == null) return;

    final file = File(result.files.single.path!);
    final lines = await file.readAsLines();

    if (lines.isEmpty) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('CSV file is empty'), backgroundColor: Colors.red),
        );
      }
      return;
    }

    final headers = lines[0].split(',').map((h) => h.trim()).toList();
    final preview = <List<String>>[];
    for (var i = 1; i < lines.length && i <= 5; i++) {
      preview.add(lines[i].split(',').map((v) => v.trim()).toList());
    }

    setState(() {
      _filePath = result.files.single.path;
      _fileName = result.files.single.name;
      _headers = headers;
      _previewRows = preview;
      _importResult = null;
    });
  }

  List<String> get _normalizedHeaders {
    return _headers.map((h) {
      final lower = h.toLowerCase().trim();
      return _aliases[lower] ?? lower;
    }).toList();
  }

  Future<void> _importData() async {
    if (_filePath == null) return;

    setState(() => _isImporting = true);

    try {
      final token = await TokenStorage.getToken();
      if (token == null) throw Exception('Not authenticated');

      final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.sensorImport}');
      final request = http.MultipartRequest('POST', uri);
      request.headers['Authorization'] = 'Bearer $token';
      request.files.add(await http.MultipartFile.fromPath('file', _filePath!));

      final streamed = await appHttpClient.send(request);
      final response = await http.Response.fromStream(streamed);

      if (response.statusCode == 200) {
        setState(() {
          _importResult = json.decode(response.body);
        });
      } else {
        final data = json.decode(response.body);
        throw Exception(data['detail'] ?? 'Import failed');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Import failed: ${e.toString().replaceFirst("Exception: ", "")}'), backgroundColor: Colors.red),
        );
      }
    } finally {
      setState(() => _isImporting = false);
    }
  }

  void _reset() {
    setState(() {
      _filePath = null;
      _fileName = null;
      _headers = [];
      _previewRows = [];
      _importResult = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Import Dataset', subtitle: 'Upload sensor data from CSV'),
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // File picker
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: _isImporting ? null : _pickFile,
                icon: const Icon(Icons.upload_file),
                label: Text(_fileName ?? 'Select CSV File'),
                style: OutlinedButton.styleFrom(
                  foregroundColor: const Color(0xFF53AD64),
                  side: const BorderSide(color: Color(0xFF53AD64)),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
              ),
            ),

            if (_headers.isNotEmpty) ...[
              const SizedBox(height: 20),

              // Column match summary
              Text('Column Matching', style: GoogleFonts.scheherazadeNew(fontSize: 18, fontWeight: FontWeight.w500)),
              const SizedBox(height: 10),
              ..._expectedColumns.map((col) {
                final matched = _normalizedHeaders.contains(col);
                final isRequired = _requiredColumns.contains(col);
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 2),
                  child: Row(
                    children: [
                      Icon(
                        matched ? Icons.check_circle : Icons.remove_circle_outline,
                        color: matched ? const Color(0xFF4BAE4F) : Colors.grey,
                        size: 18,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        col + (isRequired ? ' *' : ''),
                        style: TextStyle(
                          fontSize: 13,
                          color: matched ? Colors.black87 : Colors.grey,
                          fontWeight: isRequired ? FontWeight.w600 : FontWeight.normal,
                        ),
                      ),
                    ],
                  ),
                );
              }),
              const SizedBox(height: 4),
              Text('* Required fields', style: TextStyle(fontSize: 11, color: Colors.grey[600])),

              const SizedBox(height: 20),

              // Preview table
              Text('Preview (first 5 rows)', style: GoogleFonts.scheherazadeNew(fontSize: 18, fontWeight: FontWeight.w500)),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                  headingRowColor: WidgetStateProperty.all(const Color(0xFFF5F5F5)),
                  columnSpacing: 16,
                  columns: _headers.map((h) => DataColumn(label: Text(h, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)))).toList(),
                  rows: _previewRows.map((row) {
                    return DataRow(
                      cells: List.generate(
                        _headers.length,
                        (i) => DataCell(Text(i < row.length ? row[i] : '', style: const TextStyle(fontSize: 11))),
                      ),
                    );
                  }).toList(),
                ),
              ),

              const SizedBox(height: 20),

              // Import button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isImporting ? null : _importData,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF4BAE4F),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  ),
                  child: _isImporting
                      ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Text('Import Data', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                ),
              ),
            ],

            // Import result
            if (_importResult != null) ...[
              const SizedBox(height: 20),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFFF0F9F0),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFF4BAE4F).withValues(alpha: 0.3)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Import Complete', style: GoogleFonts.inter(fontSize: 16, fontWeight: FontWeight.bold, color: const Color(0xFF2E7D32))),
                    const SizedBox(height: 10),
                    Text('Rows imported: ${_importResult!['rows_imported']}', style: const TextStyle(color: Color(0xFF2E7D32))),
                    if ((_importResult!['rows_skipped'] as int) > 0)
                      Text('Rows skipped: ${_importResult!['rows_skipped']}', style: const TextStyle(color: Colors.orange)),
                    if ((_importResult!['errors'] as List).isNotEmpty) ...[
                      const SizedBox(height: 10),
                      ExpansionTile(
                        title: Text('Errors (${(_importResult!['errors'] as List).length})', style: const TextStyle(fontSize: 13, color: Colors.red)),
                        tilePadding: EdgeInsets.zero,
                        children: (_importResult!['errors'] as List).map<Widget>((e) {
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 2),
                            child: Text('Row ${e['row']}: ${e['message']}', style: const TextStyle(fontSize: 11, color: Colors.red)),
                          );
                        }).toList(),
                      ),
                    ],
                    const SizedBox(height: 10),
                    TextButton(
                      onPressed: _reset,
                      child: const Text('Import Another File', style: TextStyle(color: Color(0xFF53AD64))),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

- [ ] **Step 4: Commit**

```bash
git add mobile/pubspec.yaml mobile/lib/utils/api_constants.dart mobile/lib/pages/import_dataset_page.dart
git commit -m "feat: add CSV import functionality for sensor data"
```

---

## Chunk 4: Farm Management Fix

### Task 8: Fix Sector model and dialog

**Files:**
- Modify: `mobile/lib/models/farm_sector.dart`
- Modify: `mobile/lib/widgets/sector_dialog.dart.dart`
- Modify: `mobile/lib/widgets/farm_sector_card.dart`

- [ ] **Step 1: Update Sector model to use areaValue + areaUnit**

Rewrite `mobile/lib/models/farm_sector.dart`:

```dart
/// Represents a farm sector/plot in the AgriSense system.
class Sector {
  final int? id;
  final int? userId;
  String name;
  String location;
  double? areaValue;
  String areaUnit;
  String crop;
  String planted; // Date string in format 'yyyy-MM-dd'
  final DateTime? createdAt;
  final DateTime? updatedAt;

  Sector({
    this.id,
    this.userId,
    required this.name,
    required this.location,
    this.areaValue,
    this.areaUnit = 'acres',
    required this.crop,
    required this.planted,
    this.createdAt,
    this.updatedAt,
  });

  /// Formatted area display string.
  String get areaDisplay {
    if (areaValue == null) return 'Not set';
    return '${areaValue!.toStringAsFixed(1)} $areaUnit';
  }

  /// Create a Sector from JSON response.
  factory Sector.fromJson(Map<String, dynamic> json) {
    String plantedDate = '';
    if (json['planted_date'] != null) {
      final dateStr = json['planted_date'] as String;
      if (dateStr.contains('T')) {
        plantedDate = dateStr.split('T')[0];
      } else {
        plantedDate = dateStr;
      }
    }

    // Parse area: prefer area_value/area_unit, fall back to parsing area string
    double? areaValue = (json['area_value'] as num?)?.toDouble();
    String areaUnit = json['area_unit'] as String? ?? 'acres';

    if (areaValue == null && json['area'] != null) {
      final areaStr = json['area'] as String;
      final match = RegExp(r'([\d.]+)\s*(\w+)?').firstMatch(areaStr);
      if (match != null) {
        areaValue = double.tryParse(match.group(1) ?? '');
        if (match.group(2) != null) areaUnit = match.group(2)!;
      }
    }

    return Sector(
      id: json['id'] as int?,
      userId: json['user_id'] as int?,
      name: json['name'] as String? ?? '',
      location: json['location'] as String? ?? '',
      areaValue: areaValue,
      areaUnit: areaUnit,
      crop: json['crop'] as String? ?? '',
      planted: plantedDate,
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'] as String)
          : null,
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'] as String)
          : null,
    );
  }

  /// Convert Sector to JSON for API requests.
  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{
      'name': name,
      'location': location.isNotEmpty ? location : null,
      'area': areaValue != null ? '${areaValue!.toStringAsFixed(1)} $areaUnit' : null,
      'area_value': areaValue,
      'area_unit': areaUnit,
      'crop': crop.isNotEmpty ? crop : null,
    };

    if (planted.isNotEmpty) {
      if (!planted.contains('T')) {
        json['planted_date'] = '${planted}T00:00:00';
      } else {
        json['planted_date'] = planted;
      }
    }

    return json;
  }

  Sector copyWith({
    int? id,
    int? userId,
    String? name,
    String? location,
    double? areaValue,
    String? areaUnit,
    String? crop,
    String? planted,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Sector(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      name: name ?? this.name,
      location: location ?? this.location,
      areaValue: areaValue ?? this.areaValue,
      areaUnit: areaUnit ?? this.areaUnit,
      crop: crop ?? this.crop,
      planted: planted ?? this.planted,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
```

- [ ] **Step 2: Rewrite Sector Dialog with proper inputs**

Rewrite `mobile/lib/widgets/sector_dialog.dart.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import '../models/farm_sector.dart';

class SectorDialog extends StatefulWidget {
  final Sector? initialSector;
  final void Function(Sector) onSave;
  final void Function()? onDelete;

  const SectorDialog({
    super.key,
    this.initialSector,
    required this.onSave,
    this.onDelete,
  });

  @override
  State<SectorDialog> createState() => _SectorDialogState();
}

class _SectorDialogState extends State<SectorDialog> {
  late TextEditingController nameController;
  late TextEditingController locationController;
  late TextEditingController areaValueController;
  String _areaUnit = 'acres';
  String _selectedCrop = 'rice';
  DateTime? _plantedDate;
  String? _nameError;

  static const List<Map<String, String>> _cropTypes = [
    {'value': 'rice', 'label': 'Rice'},
    {'value': 'vegetables', 'label': 'Vegetables'},
    {'value': 'corn', 'label': 'Corn'},
    {'value': 'oil_palm', 'label': 'Oil Palm'},
    {'value': 'rubber', 'label': 'Rubber'},
  ];

  static const List<String> _areaUnits = ['acres', 'hectares'];

  @override
  void initState() {
    super.initState();
    final s = widget.initialSector;
    nameController = TextEditingController(text: s?.name ?? '');
    locationController = TextEditingController(text: s?.location ?? '');
    areaValueController = TextEditingController(
      text: s?.areaValue?.toStringAsFixed(1) ?? '',
    );
    _areaUnit = s?.areaUnit ?? 'acres';

    // Handle crop: if existing value is not in the list, default to first option
    final existingCrop = s?.crop?.toLowerCase() ?? 'rice';
    if (_cropTypes.any((c) => c['value'] == existingCrop)) {
      _selectedCrop = existingCrop;
    } else if (existingCrop.isNotEmpty) {
      // Add as temporary option
      _selectedCrop = existingCrop;
    } else {
      _selectedCrop = 'rice';
    }

    if (s?.planted != null && s!.planted.isNotEmpty) {
      _plantedDate = DateTime.tryParse(s.planted);
    }
  }

  @override
  void dispose() {
    nameController.dispose();
    locationController.dispose();
    areaValueController.dispose();
    super.dispose();
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _plantedDate ?? DateTime.now(),
      firstDate: DateTime(2000),
      lastDate: DateTime.now().add(const Duration(days: 365)),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.light(primary: Color(0xFF53AD64)),
          ),
          child: child!,
        );
      },
    );
    if (picked != null) {
      setState(() => _plantedDate = picked);
    }
  }

  void _save() {
    if (nameController.text.trim().isEmpty) {
      setState(() => _nameError = 'Sector name is required');
      return;
    }
    setState(() => _nameError = null);

    final sector = Sector(
      name: nameController.text.trim(),
      location: locationController.text.trim(),
      areaValue: double.tryParse(areaValueController.text),
      areaUnit: _areaUnit,
      crop: _selectedCrop,
      planted: _plantedDate != null ? DateFormat('yyyy-MM-dd').format(_plantedDate!) : '',
    );
    widget.onSave(sector);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final isEditing = widget.initialSector != null && widget.initialSector!.id != null;

    // Build crop dropdown items, include existing value if not in standard list
    final cropItems = <DropdownMenuItem<String>>[];
    for (final crop in _cropTypes) {
      cropItems.add(DropdownMenuItem(value: crop['value'], child: Text(crop['label']!)));
    }
    if (!_cropTypes.any((c) => c['value'] == _selectedCrop)) {
      cropItems.insert(0, DropdownMenuItem(value: _selectedCrop, child: Text(_selectedCrop)));
    }

    return Dialog(
      insetPadding: const EdgeInsets.symmetric(horizontal: 20),
      backgroundColor: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Name
              TextField(
                controller: nameController,
                style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16),
                decoration: InputDecoration(
                  hintText: 'Sector Name *',
                  hintStyle: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Color(0xFF676767)),
                  border: InputBorder.none,
                  errorText: _nameError,
                ),
                onChanged: (_) {
                  if (_nameError != null) setState(() => _nameError = null);
                },
              ),
              const Divider(),
              const SizedBox(height: 8),

              // Plot Description
              _buildLabel('Plot Description'),
              const SizedBox(height: 4),
              TextField(
                controller: locationController,
                style: const TextStyle(fontSize: 13),
                decoration: const InputDecoration(
                  hintText: 'e.g. North field, Block A',
                  hintStyle: TextStyle(fontSize: 13, color: Color(0xFF9E9E9E)),
                  isDense: true,
                  contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                  border: OutlineInputBorder(),
                  enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                  focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF53AD64))),
                ),
              ),
              const SizedBox(height: 12),

              // Crop Dropdown
              _buildLabel('Crop Type'),
              const SizedBox(height: 4),
              DropdownButtonFormField<String>(
                value: _selectedCrop,
                isDense: true,
                decoration: const InputDecoration(
                  isDense: true,
                  contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                  border: OutlineInputBorder(),
                  enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                  focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF53AD64))),
                ),
                items: cropItems,
                onChanged: (value) {
                  if (value != null) setState(() => _selectedCrop = value);
                },
              ),
              const SizedBox(height: 12),

              // Area
              _buildLabel('Area'),
              const SizedBox(height: 4),
              Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: TextField(
                      controller: areaValueController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      style: const TextStyle(fontSize: 13),
                      decoration: const InputDecoration(
                        hintText: '0.0',
                        isDense: true,
                        contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                        border: OutlineInputBorder(),
                        enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                        focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF53AD64))),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    flex: 2,
                    child: DropdownButtonFormField<String>(
                      value: _areaUnit,
                      isDense: true,
                      decoration: const InputDecoration(
                        isDense: true,
                        contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                        border: OutlineInputBorder(),
                        enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                        focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF53AD64))),
                      ),
                      items: _areaUnits.map((u) => DropdownMenuItem(value: u, child: Text(u))).toList(),
                      onChanged: (value) {
                        if (value != null) setState(() => _areaUnit = value);
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // Planted Date
              _buildLabel('Planted Date'),
              const SizedBox(height: 4),
              InkWell(
                onTap: _pickDate,
                child: InputDecorator(
                  decoration: const InputDecoration(
                    isDense: true,
                    contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                    border: OutlineInputBorder(),
                    enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                    suffixIcon: Icon(Icons.calendar_today, size: 18, color: Color(0xFF53AD64)),
                  ),
                  child: Text(
                    _plantedDate != null ? DateFormat('yyyy-MM-dd').format(_plantedDate!) : 'Select date',
                    style: TextStyle(
                      fontSize: 13,
                      color: _plantedDate != null ? Colors.black87 : const Color(0xFF9E9E9E),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Action buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  if (isEditing)
                    TextButton(
                      onPressed: () {
                        widget.onDelete?.call();
                        Navigator.pop(context);
                      },
                      child: const Text('Delete', style: TextStyle(color: Colors.red)),
                    )
                  else
                    const SizedBox(),
                  Row(
                    children: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('Cancel', style: TextStyle(color: Color(0xFF53AD64))),
                      ),
                      TextButton(
                        onPressed: _save,
                        child: const Text('Save', style: TextStyle(color: Color(0xFF53AD64), fontWeight: FontWeight.bold)),
                      ),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLabel(String text) {
    return Text(
      text,
      style: GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w600, color: const Color(0xFF676767)),
    );
  }
}
```

- [ ] **Step 3: Update Farm Sector Card**

In `mobile/lib/widgets/farm_sector_card.dart`, change line 79-82 to use the new area display:

Replace:
```dart
buildInfoRow('assets/images/area.png', 'Area', sector.area),
```
With:
```dart
buildInfoRow('assets/images/area.png', 'Area', sector.areaDisplay),
```

- [ ] **Step 4: Run and test**

Run: `cd mobile && flutter run`
Test: Create a new sector, edit an existing one, verify dropdown/date picker work.

- [ ] **Step 5: Commit**

```bash
git add mobile/lib/models/farm_sector.dart mobile/lib/widgets/sector_dialog.dart.dart mobile/lib/widgets/farm_sector_card.dart
git commit -m "feat: improve Farm Management UX with dropdowns, date picker, and area fields"
```

---

## Chunk 5: Help & Support + About AgriSense

### Task 9: Build Help & Support page

**Files:**
- Modify: `mobile/pubspec.yaml`
- Modify: `mobile/lib/pages/help_support_page.dart`

- [ ] **Step 1: Add url_launcher dependency**

In `mobile/pubspec.yaml`, add under dependencies:
```yaml
  url_launcher: ^6.2.0
```

Run: `cd mobile && flutter pub get`

- [ ] **Step 2: Rewrite Help & Support page**

Rewrite `mobile/lib/pages/help_support_page.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:fyp_prototype/widgets/custom_app_bar.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:url_launcher/url_launcher.dart';

class HelpSupportPage extends StatelessWidget {
  const HelpSupportPage({super.key});

  static const List<Map<String, String>> _faqs = [
    {
      'question': 'What is AgriSense?',
      'answer': 'AgriSense is an IoT-driven agricultural monitoring system that helps farmers track environmental conditions, detect pests using AI, and make data-driven decisions for their crops.',
    },
    {
      'question': 'How does pest detection work?',
      'answer': 'Upload a photo of your crop and our AI model will analyze it to identify pests. The system returns the pest type, confidence score, and recommended actions to take.',
    },
    {
      'question': 'How do I set up farm sectors?',
      'answer': 'Go to Settings > Farm Management. Tap "Add Sector" to create a new sector with crop type, area, and planting date. You can edit or delete sectors at any time.',
    },
    {
      'question': 'What environmental data is tracked?',
      'answer': 'AgriSense monitors temperature, relative humidity, soil moisture, rainfall, wind speed, and solar radiation. Data is updated regularly and displayed on your dashboard.',
    },
    {
      'question': 'How do I import historical data?',
      'answer': 'Go to Settings > Import Dataset. Select a CSV file with your sensor data. The system will validate the columns and import matching data into your account.',
    },
    {
      'question': 'How does weather forecasting work?',
      'answer': 'AgriSense uses the Open-Meteo API to provide a 5-day weather forecast for your farm location. Forecasts are updated every 10 minutes and include temperature, rainfall, and humidity predictions.',
    },
  ];

  Future<void> _launchUrl(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  Future<void> _launchEmail(String email) async {
    final uri = Uri(scheme: 'mailto', path: email);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Help & Support', subtitle: 'FAQs and contact support'),
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Frequently Asked Questions', style: GoogleFonts.scheherazadeNew(fontSize: 20, fontWeight: FontWeight.w500)),
            const SizedBox(height: 10),
            ..._faqs.map((faq) => ExpansionTile(
              tilePadding: const EdgeInsets.symmetric(horizontal: 0),
              title: Text(faq['question']!, style: GoogleFonts.inter(fontSize: 14, fontWeight: FontWeight.w600)),
              childrenPadding: const EdgeInsets.only(bottom: 12),
              children: [
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 0),
                  child: Text(faq['answer']!, style: GoogleFonts.inter(fontSize: 13, color: Colors.grey[700], height: 1.5)),
                ),
              ],
            )),

            const SizedBox(height: 30),
            const Divider(),
            const SizedBox(height: 20),

            Text('Contact Support', style: GoogleFonts.scheherazadeNew(fontSize: 20, fontWeight: FontWeight.w500)),
            const SizedBox(height: 15),
            ListTile(
              contentPadding: EdgeInsets.zero,
              leading: const Icon(Icons.email_outlined, color: Color(0xFF53AD64)),
              title: const Text('Email Support', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
              subtitle: const Text('support@agrisense.app', style: TextStyle(fontSize: 13, color: Color(0xFF53AD64))),
              onTap: () => _launchEmail('support@agrisense.app'),
            ),
            ListTile(
              contentPadding: EdgeInsets.zero,
              leading: const Icon(Icons.code, color: Color(0xFF53AD64)),
              title: const Text('GitHub Repository', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
              subtitle: const Text('Report issues or contribute', style: TextStyle(fontSize: 13, color: Colors.grey)),
              onTap: () => _launchUrl('https://github.com/bryanlzj/AgriSense'),
            ),
          ],
        ),
      ),
    );
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add mobile/pubspec.yaml mobile/lib/pages/help_support_page.dart
git commit -m "feat: build Help & Support page with FAQ and contact info"
```

---

### Task 10: Build About AgriSense page

**Files:**
- Modify: `mobile/lib/pages/about_agrisense_page.dart`

- [ ] **Step 1: Rewrite About page**

Rewrite `mobile/lib/pages/about_agrisense_page.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:fyp_prototype/widgets/custom_app_bar.dart';
import 'package:google_fonts/google_fonts.dart';

class AboutAgrisensePage extends StatelessWidget {
  const AboutAgrisensePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'About AgriSense', subtitle: 'App information'),
      backgroundColor: Colors.white,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 30),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.asset('assets/images/logo.png', width: 100, height: 100),
              const SizedBox(height: 20),
              Text(
                'AgriSense',
                style: GoogleFonts.scheherazadeNew(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                  color: const Color(0xFF2E7D32),
                ),
              ),
              const SizedBox(height: 6),
              Text(
                'Version 1.0.0',
                style: GoogleFonts.inter(fontSize: 14, color: Colors.grey[600]),
              ),
              const SizedBox(height: 24),
              Text(
                'AgriSense is an IoT-driven agricultural monitoring system that helps farmers track environmental conditions, detect pests, and make data-driven decisions for their crops.',
                textAlign: TextAlign.center,
                style: GoogleFonts.inter(fontSize: 14, color: Colors.grey[700], height: 1.6),
              ),
              const SizedBox(height: 30),
              const Divider(),
              const SizedBox(height: 20),
              Text(
                'Built with Flutter & FastAPI',
                style: GoogleFonts.inter(fontSize: 12, color: Colors.grey[500]),
              ),
              const SizedBox(height: 6),
              Text(
                '\u00a9 2026 AgriSense Team',
                style: GoogleFonts.inter(fontSize: 12, color: Colors.grey[400]),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add mobile/lib/pages/about_agrisense_page.dart
git commit -m "feat: build About AgriSense page with app info"
```

---

## Final Verification

### Task 11: End-to-end verification

- [ ] **Step 1: Run backend**

```bash
cd backend && python run.py
```

Verify: Swagger UI at `/docs` shows new endpoints (PUT /auth/me, POST /auth/change-password, POST /sensor/import).

- [ ] **Step 2: Run mobile app**

```bash
cd mobile && flutter run
```

Verify each settings feature:
1. Edit Profile — can update name, email, farm location, crop type; can change password
2. Import Dataset — can pick CSV, see preview, import successfully
3. Farm Management — dropdown for crop, date picker for planted, numeric area with unit
4. Help & Support — FAQ accordion expands, email/GitHub links work
5. About AgriSense — shows version and description

- [ ] **Step 3: Commit any fixes**

If any issues found, fix and commit with descriptive message.
