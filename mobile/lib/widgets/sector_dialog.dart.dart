import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
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
  late TextEditingController areaValueController;
  String _areaUnit = 'acres';
  String _selectedCrop = 'rice';
  DateTime? _plantedDate;
  String? _nameError;

  static const List<Map<String, String>> _cropTypes = [
    {'value': 'rice', 'label': 'Rice'},
    {'value': 'vegetables', 'label': 'Vegetables'},
    {'value': 'corn', 'label': 'Corn'},
    {'value': 'oil_palm', 'label': 'Oil Palm'},
    {'value': 'rubber', 'label': 'Rubber'},
  ];

  static const List<String> _areaUnits = ['acres', 'hectares'];

  @override
  void initState() {
    super.initState();
    final s = widget.initialSector;
    nameController = TextEditingController(text: s?.name ?? '');
    locationController = TextEditingController(text: s?.location ?? '');
    areaValueController = TextEditingController(
      text: s?.areaValue?.toStringAsFixed(1) ?? '',
    );
    _areaUnit = s?.areaUnit ?? 'acres';

    // Handle crop: if existing value is not in the list, default to first option
    final existingCrop = s?.crop.toLowerCase() ?? 'rice';
    if (_cropTypes.any((c) => c['value'] == existingCrop)) {
      _selectedCrop = existingCrop;
    } else if (existingCrop.isNotEmpty) {
      _selectedCrop = existingCrop;
    } else {
      _selectedCrop = 'rice';
    }

    if (s?.planted != null && s!.planted.isNotEmpty) {
      _plantedDate = DateTime.tryParse(s.planted);
    }
  }

  @override
  void dispose() {
    nameController.dispose();
    locationController.dispose();
    areaValueController.dispose();
    super.dispose();
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _plantedDate ?? DateTime.now(),
      firstDate: DateTime(2000),
      lastDate: DateTime.now().add(const Duration(days: 365)),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.light(primary: Color(0xFF53AD64)),
          ),
          child: child!,
        );
      },
    );
    if (picked != null) {
      setState(() => _plantedDate = picked);
    }
  }

  void _save() {
    if (nameController.text.trim().isEmpty) {
      setState(() => _nameError = 'Sector name is required');
      return;
    }
    setState(() => _nameError = null);

    final sector = Sector(
      name: nameController.text.trim(),
      location: locationController.text.trim(),
      areaValue: double.tryParse(areaValueController.text),
      areaUnit: _areaUnit,
      crop: _selectedCrop,
      planted: _plantedDate != null ? DateFormat('yyyy-MM-dd').format(_plantedDate!) : '',
    );
    widget.onSave(sector);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    final isEditing = widget.initialSector != null && widget.initialSector!.id != null;

    // Build crop dropdown items, include existing value if not in standard list
    final cropItems = <DropdownMenuItem<String>>[];
    for (final crop in _cropTypes) {
      cropItems.add(DropdownMenuItem(value: crop['value'], child: Text(crop['label']!)));
    }
    if (!_cropTypes.any((c) => c['value'] == _selectedCrop)) {
      cropItems.insert(0, DropdownMenuItem(value: _selectedCrop, child: Text(_selectedCrop)));
    }

    return Dialog(
      insetPadding: const EdgeInsets.symmetric(horizontal: 20),
      backgroundColor: Colors.white,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Name
              TextField(
                controller: nameController,
                style: GoogleFonts.inter(fontWeight: FontWeight.bold, fontSize: 16),
                decoration: InputDecoration(
                  hintText: 'Sector Name *',
                  hintStyle: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Color(0xFF676767)),
                  border: InputBorder.none,
                  errorText: _nameError,
                ),
                onChanged: (_) {
                  if (_nameError != null) setState(() => _nameError = null);
                },
              ),
              const Divider(),
              const SizedBox(height: 8),

              // Plot Description
              _buildLabel('Plot Description'),
              const SizedBox(height: 4),
              TextField(
                controller: locationController,
                style: const TextStyle(fontSize: 13),
                decoration: const InputDecoration(
                  hintText: 'e.g. North field, Block A',
                  hintStyle: TextStyle(fontSize: 13, color: Color(0xFF9E9E9E)),
                  isDense: true,
                  contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                  border: OutlineInputBorder(),
                  enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                  focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF53AD64))),
                ),
              ),
              const SizedBox(height: 12),

              // Crop Dropdown
              _buildLabel('Crop Type'),
              const SizedBox(height: 4),
              DropdownButtonFormField<String>(
                value: _selectedCrop,
                isDense: true,
                decoration: const InputDecoration(
                  isDense: true,
                  contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                  border: OutlineInputBorder(),
                  enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                  focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF53AD64))),
                ),
                items: cropItems,
                onChanged: (value) {
                  if (value != null) setState(() => _selectedCrop = value);
                },
              ),
              const SizedBox(height: 12),

              // Area
              _buildLabel('Area'),
              const SizedBox(height: 4),
              Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: TextField(
                      controller: areaValueController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      style: const TextStyle(fontSize: 13),
                      decoration: const InputDecoration(
                        hintText: '0.0',
                        isDense: true,
                        contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                        border: OutlineInputBorder(),
                        enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                        focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF53AD64))),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    flex: 2,
                    child: DropdownButtonFormField<String>(
                      value: _areaUnit,
                      isDense: true,
                      decoration: const InputDecoration(
                        isDense: true,
                        contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                        border: OutlineInputBorder(),
                        enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                        focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF53AD64))),
                      ),
                      items: _areaUnits.map((u) => DropdownMenuItem(value: u, child: Text(u))).toList(),
                      onChanged: (value) {
                        if (value != null) setState(() => _areaUnit = value);
                      },
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),

              // Planted Date
              _buildLabel('Planted Date'),
              const SizedBox(height: 4),
              InkWell(
                onTap: _pickDate,
                child: InputDecorator(
                  decoration: const InputDecoration(
                    isDense: true,
                    contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 10),
                    border: OutlineInputBorder(),
                    enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFFE0E0E0))),
                    suffixIcon: Icon(Icons.calendar_today, size: 18, color: Color(0xFF53AD64)),
                  ),
                  child: Text(
                    _plantedDate != null ? DateFormat('yyyy-MM-dd').format(_plantedDate!) : 'Select date',
                    style: TextStyle(
                      fontSize: 13,
                      color: _plantedDate != null ? Colors.black87 : const Color(0xFF9E9E9E),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Action buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  if (isEditing)
                    TextButton(
                      onPressed: () {
                        widget.onDelete?.call();
                        Navigator.pop(context);
                      },
                      child: const Text('Delete', style: TextStyle(color: Colors.red)),
                    )
                  else
                    const SizedBox(),
                  Row(
                    children: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: const Text('Cancel', style: TextStyle(color: Color(0xFF53AD64))),
                      ),
                      TextButton(
                        onPressed: _save,
                        child: const Text('Save', style: TextStyle(color: Color(0xFF53AD64), fontWeight: FontWeight.bold)),
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

  Widget _buildLabel(String text) {
    return Text(
      text,
      style: GoogleFonts.inter(fontSize: 12, fontWeight: FontWeight.w600, color: const Color(0xFF676767)),
    );
  }
}
