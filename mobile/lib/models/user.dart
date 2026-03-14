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
