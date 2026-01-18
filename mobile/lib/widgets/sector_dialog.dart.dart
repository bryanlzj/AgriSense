import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/farm_sector.dart';

class SectorDialog extends StatefulWidget {
  final Sector? initialSector;
  final void Function(Sector) onSave;
  final void Function()? onDelete;

  const SectorDialog({
    super.key,
    this.initialSector,
    required this.onSave,
    this.onDelete,
  });

  @override
  State<SectorDialog> createState() => _SectorDialogState();
}

class _SectorDialogState extends State<SectorDialog> {
  late TextEditingController nameController;
  late TextEditingController locationController;
  late TextEditingController areaController;
  late TextEditingController cropController;
  late TextEditingController plantedController;

  @override
  void initState() {
    super.initState();
    final s = widget.initialSector;
    nameController = TextEditingController(text: s?.name ?? '');
    locationController = TextEditingController(text: s?.location ?? '');
    areaController = TextEditingController(text: s?.area ?? '');
    cropController = TextEditingController(text: s?.crop ?? '');
    plantedController = TextEditingController(text: s?.planted ?? '');
  }

  @override
  void dispose() {
    nameController.dispose();
    locationController.dispose();
    areaController.dispose();
    cropController.dispose();
    plantedController.dispose();
    super.dispose();
  }

  Widget _buildDialogFieldRow({
    required String icon,
    required String label,
    required String hintText,
    required TextEditingController controller,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Image.asset(icon, height: 20, width: 20),
          const SizedBox(width: 10),
          Text(
            label,
            style: GoogleFonts.inter(
              fontSize: 12,
              fontWeight: FontWeight.bold,
              color: const Color(0xFF676767),
            ),
          ),
          Expanded(
            child: SizedBox(
              height: 30,
              child: TextField(
                controller: controller,
                style: const TextStyle(fontSize: 12, color: Color(0xFF676767)),
                decoration: InputDecoration(
                  hintText: hintText,
                  contentPadding: const EdgeInsets.symmetric(horizontal: 5),
                  focusedBorder: OutlineInputBorder(
                    borderSide: BorderSide.none,
                  ),
                  border: OutlineInputBorder(borderSide: BorderSide.none),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      insetPadding: const EdgeInsets.symmetric(horizontal: 20),
      backgroundColor: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: Container(
        height: 300,
        decoration: BoxDecoration(
          border: Border.all(
            color: Colors.black.withValues(alpha: 0.1),
            width: 1.5,
          ),
          borderRadius: BorderRadius.circular(15),
        ),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 15),
          child: Column(
            children: [
              // Title Row
              TextField(
                controller: nameController,
                style: GoogleFonts.inter(fontWeight: FontWeight.bold),
                decoration: const InputDecoration(
                  hintText: 'Sector Name',
                  hintStyle: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF676767),
                  ),
                  //border: OutlineInputBorder(),
                  border: InputBorder.none,
                ),
              ),
              //const SizedBox(height: 5),
              Expanded(
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      _buildDialogFieldRow(
                        icon: 'assets/images/pin.png',
                        label: 'Location:',
                        hintText: 'Enter location',
                        controller: locationController,
                      ),
                      _buildDialogFieldRow(
                        icon: 'assets/images/area.png',
                        label: 'Area:',
                        hintText: 'Enter area',
                        controller: areaController,
                      ),
                      _buildDialogFieldRow(
                        icon: 'assets/images/crop.png',
                        label: 'Crop:',
                        hintText: 'Enter crop',
                        controller: cropController,
                      ),
                      _buildDialogFieldRow(
                        icon: 'assets/images/calender.png',
                        label: 'Planted:',
                        hintText: 'Enter date',
                        controller: plantedController,
                      ),
                    ],
                  ),
                ),
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  TextButton(
                    onPressed: () {
                      widget.onDelete?.call();
                      Navigator.pop(context);
                    },
                    child: const Text(
                      'Delete',
                      style: TextStyle(color: Color(0xFF53AD64)),
                    ),
                  ),
                  Row(
                    children: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text(
                          'Cancel',
                          style: TextStyle(color: Color(0xFF53AD64)),
                        ),
                      ),
                      TextButton(
                        onPressed: () {
                          final sector = Sector(
                            name: nameController.text.isEmpty
                                ? 'Unnamed Sector'
                                : nameController.text,
                            location: locationController.text.isEmpty
                                ? 'Unknown'
                                : locationController.text,
                            area: areaController.text.isEmpty
                                ? 'Unknown'
                                : areaController.text,
                            crop: cropController.text.isEmpty
                                ? 'Unknown'
                                : cropController.text,
                            planted: plantedController.text.isEmpty
                                ? 'Unknown'
                                : plantedController.text,
                          );
                          widget.onSave(sector);
                          Navigator.pop(context);
                        },
                        child: Text(
                          'Save',
                          style: TextStyle(color: Color(0xFF53AD64)),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
