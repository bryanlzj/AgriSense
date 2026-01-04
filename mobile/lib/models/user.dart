/// User model
class User {
  final int id;
  final String username;
  final String fullName;
  final DateTime createdAt;

  User({
    required this.id,
    required this.username,
    required this.fullName,
    required this.createdAt,
  });

  /// Create User from JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      username: json['username'],
      fullName: json['full_name'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  /// Convert User to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'full_name': fullName,
      'created_at': createdAt.toIso8601String(),
    };
  }
}
