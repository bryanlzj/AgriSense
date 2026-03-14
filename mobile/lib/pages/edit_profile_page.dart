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
