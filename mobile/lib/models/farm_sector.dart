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
