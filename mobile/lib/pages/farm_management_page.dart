import 'package:flutter/material.dart';
import 'package:fyp_prototype/services/mock_sector_service.dart';
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
  final List<Sector> _sectors = [];

  @override
  void initState() {
    super.initState();
    _loadMockSectors();
  }

  Future<void> _loadMockSectors() async {
    final sectors = await MockSectorService.fetchSectors();
    setState(() {
      _sectors.clear();
      _sectors.addAll(sectors);
    });
  }
  Future<void> _deleteSector(int index) async {
    await MockSectorService.deleteSector(index);
    _loadMockSectors(); // refresh after deletion
  }

  void _addOrEditSector(Sector sector, [int? index]) async {
    if (index != null) {
      await MockSectorService.updateSector(index, sector);
    } else {
      await MockSectorService.addSector(sector);
    }
    _loadMockSectors(); // refresh after change
  }


  void _showSectorDialog({Sector? sector, int? index}) {
    showDialog(
      context: context,
      builder: (_) => SectorDialog(
        initialSector: sector,
        onSave: (newSector) {
          _addOrEditSector(newSector, index);
          
        },
        onDelete: index != null
            ? () {
                _deleteSector(index);
                
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
              child: _sectors.isEmpty
                  ? const Center(child: Text('No sectors added yet'))
                  : ListView.builder(
                      itemCount: _sectors.length,
                      itemBuilder: (context, index) {
                        return FarmSectorCard(
                          sector: _sectors[index],
                          onEdit: () => _showSectorDialog(
                            sector: _sectors[index],
                            index: index,
                          ),
                        );
                      },
                    ),
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
}
