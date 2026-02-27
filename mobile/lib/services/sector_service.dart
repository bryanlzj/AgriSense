import 'dart:convert';
import 'package:fyp_prototype/utils/api_constants.dart';
import 'package:fyp_prototype/utils/token_storage.dart';
import 'package:fyp_prototype/utils/http_client.dart';
import 'package:fyp_prototype/models/farm_sector.dart';

/// Service for managing farm sectors via the API.
class SectorService {
  /// Fetch all sectors for the current user.
  static Future<List<Sector>> fetchSectors({
    int skip = 0,
    int limit = 50,
    String? crop,
  }) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final queryParams = <String, String>{
      'skip': skip.toString(),
      'limit': limit.toString(),
    };
    if (crop != null) queryParams['crop'] = crop;

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.sectors}')
        .replace(queryParameters: queryParams);

    final response = await appHttpClient.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      // Backend returns a direct array
      if (data is List) {
        return data
            .map((s) => Sector.fromJson(s as Map<String, dynamic>))
            .toList();
      }
      return [];
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch sectors');
    }
  }

  /// Get a single sector by ID.
  static Future<Sector> getSector(int sectorId) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri =
        Uri.parse('${ApiConstants.baseUrl}${ApiConstants.sectors}$sectorId');

    final response = await appHttpClient.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return Sector.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 404) {
      throw Exception('Sector not found');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch sector');
    }
  }

  /// Create a new sector.
  static Future<Sector> createSector(Sector sector) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.sectors}');

    final response = await appHttpClient.post(
      uri,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode(sector.toJson()),
    );

    if (response.statusCode == 201) {
      final data = json.decode(response.body);
      return Sector.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to create sector');
    }
  }

  /// Update an existing sector.
  static Future<Sector> updateSector(int sectorId, Sector sector) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri =
        Uri.parse('${ApiConstants.baseUrl}${ApiConstants.sectors}$sectorId');

    final response = await appHttpClient.put(
      uri,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: json.encode(sector.toJson()),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return Sector.fromJson(data);
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 404) {
      throw Exception('Sector not found');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to update sector');
    }
  }

  /// Delete a sector.
  static Future<void> deleteSector(int sectorId) async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri =
        Uri.parse('${ApiConstants.baseUrl}${ApiConstants.sectors}$sectorId');

    final response = await appHttpClient.delete(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 204 || response.statusCode == 200) {
      return;
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else if (response.statusCode == 404) {
      throw Exception('Sector not found');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to delete sector');
    }
  }

  /// Get sector statistics.
  static Future<Map<String, dynamic>> getSectorStats() async {
    final token = await TokenStorage.getToken();
    if (token == null) {
      throw Exception('Not authenticated');
    }

    final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.sectorStats}');

    final response = await appHttpClient.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      return json.decode(response.body) as Map<String, dynamic>;
    } else if (response.statusCode == 401) {
      throw Exception('Session expired. Please login again.');
    } else {
      final data = json.decode(response.body);
      throw Exception(data['detail'] ?? 'Failed to fetch sector stats');
    }
  }
}
