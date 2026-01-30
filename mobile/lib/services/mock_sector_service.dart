// lib/services/mock_sector_service.dart
import 'dart:async';
import '../models/farm_sector.dart';

class MockSectorService {
  static final List<Sector> _mockSectors = [
    Sector(
      name: 'Sector 1',
      location: 'North Field',
      area: '2 acres',
      crop: 'Corn',
      planted: '2025-03-12',
    ),
    Sector(
      name: 'Sector 2',
      location: 'South Field',
      area: '1.5 acres',
      crop: 'Wheat',
      planted: '2025-04-01',
    ),
  ];

  static Future<List<Sector>> fetchSectors() async {
    await Future.delayed(const Duration(milliseconds: 500)); // simulate delay
    return List.from(_mockSectors);
  }

  static Future<void> addSector(Sector sector) async {
    await Future.delayed(const Duration(milliseconds: 300));
    _mockSectors.add(sector);
  }

  static Future<void> updateSector(int index, Sector sector) async {
    await Future.delayed(const Duration(milliseconds: 300));
    _mockSectors[index] = sector;
  }

  static Future<void> deleteSector(int index) async {
    await Future.delayed(const Duration(milliseconds: 300));
    _mockSectors.removeAt(index);
  }
}
