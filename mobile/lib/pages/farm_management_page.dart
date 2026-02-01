import 'package:flutter/material.dart';
import 'package:fyp_prototype/services/sector_service.dart';
import 'package:fyp_prototype/widgets/sector_dialog.dart.dart';
import 'package:google_fonts/google_fonts.dart';
import '../widgets/custom_app_bar.dart';
import '../widgets/farm_sector_card.dart';
import '../models/farm_sector.dart';

class FarmManagementPage extends StatefulWidget {
  const FarmManagementPage({super.key});

  @override
  State<FarmManagementPage> createState() => _FarmManagementPageState();
}

class _FarmManagementPageState extends State<FarmManagementPage> {
  List<Sector> _sectors = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadSectors();
  }

  Future<void> _loadSectors() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final sectors = await SectorService.fetchSectors();
      setState(() {
        _sectors = sectors;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString().replaceFirst('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  Future<void> _deleteSector(Sector sector) async {
    if (sector.id == null) return;

    try {
      await SectorService.deleteSector(sector.id!);
      _loadSectors(); // refresh after deletion
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to delete sector: ${e.toString().replaceFirst('Exception: ', '')}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _addOrEditSector(Sector sector, [Sector? existingSector]) async {
    try {
      if (existingSector != null && existingSector.id != null) {
        // Update existing sector
        await SectorService.updateSector(existingSector.id!, sector);
      } else {
        // Create new sector
        await SectorService.createSector(sector);
      }
      _loadSectors(); // refresh after change
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to save sector: ${e.toString().replaceFirst('Exception: ', '')}'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  void _showSectorDialog({Sector? sector}) {
    showDialog(
      context: context,
      builder: (_) => SectorDialog(
        initialSector: sector,
        onSave: (newSector) {
          _addOrEditSector(newSector, sector);
        },
        onDelete: sector != null && sector.id != null
            ? () {
                _deleteSector(sector);
              }
            : null,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(
        title: 'Farm Management',
        subtitle: 'Manage your farm sectors and crops',
      ),
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'My Farm Sectors',
              style: GoogleFonts.scheherazadeNew(
                fontSize: 20,
                fontWeight: FontWeight.w500,
              ),
            ),
            const SizedBox(height: 15),
            Expanded(
              child: _buildContent(),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: const Color(0xFF53AD64),
        foregroundColor: Colors.white,
        onPressed: () => _showSectorDialog(),
        icon: const Icon(Icons.add),
        label: const Text('Add Sector'),
      ),
    );
  }

  Widget _buildContent() {
    if (_isLoading) {
      return const Center(
        child: CircularProgressIndicator(color: Color(0xFF53AD64)),
      );
    }

    if (_error != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.error_outline, color: Colors.red, size: 48),
            const SizedBox(height: 16),
            Text(
              _error!,
              style: GoogleFonts.inter(color: Colors.red),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loadSectors,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF53AD64),
              ),
              child: const Text('Retry', style: TextStyle(color: Colors.white)),
            ),
          ],
        ),
      );
    }

    if (_sectors.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.grass, color: Colors.grey[400], size: 64),
            const SizedBox(height: 16),
            Text(
              'No sectors added yet',
              style: GoogleFonts.inter(
                fontSize: 16,
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Tap the button below to add your first sector',
              style: GoogleFonts.inter(
                fontSize: 14,
                color: Colors.grey[400],
              ),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _loadSectors,
      color: const Color(0xFF53AD64),
      child: ListView.builder(
        itemCount: _sectors.length,
        itemBuilder: (context, index) {
          return FarmSectorCard(
            sector: _sectors[index],
            onEdit: () => _showSectorDialog(sector: _sectors[index]),
          );
        },
      ),
    );
  }
}
