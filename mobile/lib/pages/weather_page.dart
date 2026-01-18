import 'package:flutter/material.dart';
import 'package:fyp_prototype/models/farm_sector.dart';
import 'package:fyp_prototype/services/mock_sector_service.dart';
import 'package:google_fonts/google_fonts.dart';

class WeatherPage extends StatefulWidget {
  const WeatherPage({super.key});

  @override
  State<WeatherPage> createState() => _WeatherPageState();
}

class _WeatherPageState extends State<WeatherPage> {
  List<Sector> _sectors = [];
  Sector? _selectedSector;

  @override
  void initState() {
    super.initState();
    _loadSectors();
  }

  Future<void> _loadSectors() async {
    final sectors = await MockSectorService.fetchSectors();
    setState(() {
      _sectors = sectors;
      if (sectors.isNotEmpty) {
        _selectedSector = sectors.first; // default select first sector
      }
    });
  }

  void _onSectorSelected(Sector newSector) {
    setState(() {
      _selectedSector = newSector;
      // TODO: refresh weather data for the selected sector
    });
  }

  Widget _buildSectorDropdown() {
    if (_selectedSector == null) {
      return const Center(child: Text('No sector available'));
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: Colors.grey.withValues(alpha: 0.3)),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 5,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          // 📍 Location Icon
          Image.asset('assets/images/pin.png', width: 30, height: 30),
          const SizedBox(width: 12),

          // Column with sector info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // First row: Sector name - Crop
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        _selectedSector!.name,
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(
                      _selectedSector!.crop,
                      style: const TextStyle(
                        fontWeight: FontWeight.w500,
                        fontSize: 14,
                      ),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                // Second row: Location - Area
                Row( 
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        _selectedSector!.location,
                        style: const TextStyle(
                          fontSize: 13,
                          color: Colors.grey,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    const SizedBox(width: 8),
                    Text(
                      _selectedSector!.area,
                      style: const TextStyle(fontSize: 13, color: Colors.grey),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Dropdown arrow
          PopupMenuButton<Sector>(
            icon: const Icon(Icons.keyboard_arrow_down_rounded),
            onSelected: _onSectorSelected,
            itemBuilder: (context) {
              return _sectors.map((sector) {
                return PopupMenuItem<Sector>(
                  value: sector,
                  child: Text(sector.name),
                );
              }).toList();
            },
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 200,
        flexibleSpace: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Color(0xFF53AD64), // top color
                Color(0xFF3C8AEA), // bottom color
              ],
            ),
          ),
        ),
        title: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 15.0),
          child: Column(
            children: [
              Text(
                'Weather Details',
                style: GoogleFonts.scheherazadeNew(
                  fontSize: 28,
                  color: Colors.white,
                ),
              ),
            ],
          ),
        ),
      ),
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            _buildSectorDropdown(),
            const SizedBox(height: 20),
            // Weather content for _selectedSector goes below
          ],
        ),
      ),
    );
  }
}
