/// Represents a farm sector/plot in the AgriSense system.
class Sector {
  final int? id;
  final int? userId;
  String name;
  String location;
  String area;
  String crop;
  String planted; // Date string in format 'yyyy-MM-dd'
  final DateTime? createdAt;
  final DateTime? updatedAt;

  Sector({
    this.id,
    this.userId,
    required this.name,
    required this.location,
    required this.area,
    required this.crop,
    required this.planted,
    this.createdAt,
    this.updatedAt,
  });

  /// Create a Sector from JSON response
  factory Sector.fromJson(Map<String, dynamic> json) {
    // Handle planted_date which could be a full datetime or just a date
    String plantedDate = '';
    if (json['planted_date'] != null) {
      final dateStr = json['planted_date'] as String;
      // Extract just the date part (yyyy-MM-dd) if it's a full datetime
      if (dateStr.contains('T')) {
        plantedDate = dateStr.split('T')[0];
      } else {
        plantedDate = dateStr;
      }
    }

    return Sector(
      id: json['id'] as int?,
      userId: json['user_id'] as int?,
      name: json['name'] as String? ?? '',
      location: json['location'] as String? ?? '',
      area: json['area'] as String? ?? '',
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

  /// Convert Sector to JSON for API requests
  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{
      'name': name,
      'location': location.isNotEmpty ? location : null,
      'area': area.isNotEmpty ? area : null,
      'crop': crop.isNotEmpty ? crop : null,
    };

    // Convert planted date to ISO format if provided
    if (planted.isNotEmpty) {
      // If it's just a date (yyyy-MM-dd), append time
      if (!planted.contains('T')) {
        json['planted_date'] = '${planted}T00:00:00';
      } else {
        json['planted_date'] = planted;
      }
    }

    return json;
  }

  /// Create a copy of this sector with updated fields
  Sector copyWith({
    int? id,
    int? userId,
    String? name,
    String? location,
    String? area,
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
      area: area ?? this.area,
      crop: crop ?? this.crop,
      planted: planted ?? this.planted,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
