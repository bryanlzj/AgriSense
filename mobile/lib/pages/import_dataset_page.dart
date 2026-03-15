import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:fyp_prototype/utils/api_constants.dart';
import 'package:fyp_prototype/utils/token_storage.dart';
import 'package:fyp_prototype/utils/http_client.dart';
import 'package:fyp_prototype/widgets/custom_app_bar.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:http/http.dart' as http;

class ImportDatasetPage extends StatefulWidget {
  const ImportDatasetPage({super.key});

  @override
  State<ImportDatasetPage> createState() => _ImportDatasetPageState();
}

class _ImportDatasetPageState extends State<ImportDatasetPage> {
  String? _filePath;
  String? _fileName;
  List<List<String>> _previewRows = [];
  List<String> _headers = [];
  bool _isImporting = false;
  Map<String, dynamic>? _importResult;

  static const List<String> _expectedColumns = [
    'temperature', 'relative_humidity', 'soil_moisture',
    'rain', 'wind_speed', 'solar_radiation',
    'soil_temperature', 'weather_code', 'timestamp',
  ];

  static const List<String> _requiredColumns = [
    'temperature', 'relative_humidity', 'soil_moisture',
  ];

  static const Map<String, String> _aliases = {
    'humidity': 'relative_humidity',
    'rainfall': 'rain',
  };

  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['csv'],
    );

    if (result == null || result.files.single.path == null) return;

    final file = File(result.files.single.path!);
    final lines = await file.readAsLines();

    if (lines.isEmpty) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('CSV file is empty'), backgroundColor: Colors.red),
        );
      }
      return;
    }

    final headers = lines[0].split(',').map((h) => h.trim()).toList();
    final preview = <List<String>>[];
    for (var i = 1; i < lines.length && i <= 5; i++) {
      preview.add(lines[i].split(',').map((v) => v.trim()).toList());
    }

    setState(() {
      _filePath = result.files.single.path;
      _fileName = result.files.single.name;
      _headers = headers;
      _previewRows = preview;
      _importResult = null;
    });
  }

  List<String> get _normalizedHeaders {
    return _headers.map((h) {
      final lower = h.toLowerCase().trim();
      return _aliases[lower] ?? lower;
    }).toList();
  }

  Future<void> _importData() async {
    if (_filePath == null) return;

    setState(() => _isImporting = true);

    try {
      final token = await TokenStorage.getToken();
      if (token == null) throw Exception('Not authenticated');

      final uri = Uri.parse('${ApiConstants.baseUrl}${ApiConstants.sensorImport}');
      final request = http.MultipartRequest('POST', uri);
      request.headers['Authorization'] = 'Bearer $token';
      request.files.add(await http.MultipartFile.fromPath('file', _filePath!));

      final streamed = await appHttpClient.send(request);
      final response = await http.Response.fromStream(streamed);

      if (response.statusCode == 200) {
        setState(() {
          _importResult = json.decode(response.body);
        });
      } else {
        final data = json.decode(response.body);
        throw Exception(data['detail'] ?? 'Import failed');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Import failed: ${e.toString().replaceFirst("Exception: ", "")}'), backgroundColor: Colors.red),
        );
      }
    } finally {
      setState(() => _isImporting = false);
    }
  }

  void _reset() {
    setState(() {
      _filePath = null;
      _fileName = null;
      _headers = [];
      _previewRows = [];
      _importResult = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(title: 'Import Dataset', subtitle: 'Upload sensor data from CSV'),
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // File picker
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: _isImporting ? null : _pickFile,
                icon: const Icon(Icons.upload_file),
                label: Text(_fileName ?? 'Select CSV File'),
                style: OutlinedButton.styleFrom(
                  foregroundColor: const Color(0xFF53AD64),
                  side: const BorderSide(color: Color(0xFF53AD64)),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
              ),
            ),

            if (_headers.isNotEmpty) ...[
              const SizedBox(height: 20),

              // Column match summary
              Text('Column Matching', style: GoogleFonts.scheherazadeNew(fontSize: 18, fontWeight: FontWeight.w500)),
              const SizedBox(height: 10),
              ..._expectedColumns.map((col) {
                final matched = _normalizedHeaders.contains(col);
                final isRequired = _requiredColumns.contains(col);
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 2),
                  child: Row(
                    children: [
                      Icon(
                        matched ? Icons.check_circle : Icons.remove_circle_outline,
                        color: matched ? const Color(0xFF4BAE4F) : Colors.grey,
                        size: 18,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        col + (isRequired ? ' *' : ''),
                        style: TextStyle(
                          fontSize: 13,
                          color: matched ? Colors.black87 : Colors.grey,
                          fontWeight: isRequired ? FontWeight.w600 : FontWeight.normal,
                        ),
                      ),
                    ],
                  ),
                );
              }),
              const SizedBox(height: 4),
              Text('* Required fields', style: TextStyle(fontSize: 11, color: Colors.grey[600])),

              const SizedBox(height: 20),

              // Preview table
              Text('Preview (first 5 rows)', style: GoogleFonts.scheherazadeNew(fontSize: 18, fontWeight: FontWeight.w500)),
              const SizedBox(height: 10),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                  headingRowColor: WidgetStateProperty.all(const Color(0xFFF5F5F5)),
                  columnSpacing: 16,
                  columns: _headers.map((h) => DataColumn(label: Text(h, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)))).toList(),
                  rows: _previewRows.map((row) {
                    return DataRow(
                      cells: List.generate(
                        _headers.length,
                        (i) => DataCell(Text(i < row.length ? row[i] : '', style: const TextStyle(fontSize: 11))),
                      ),
                    );
                  }).toList(),
                ),
              ),

              const SizedBox(height: 20),

              // Import button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isImporting ? null : _importData,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF4BAE4F),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  ),
                  child: _isImporting
                      ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Text('Import Data', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                ),
              ),
            ],

            // Import result
            if (_importResult != null) ...[
              const SizedBox(height: 20),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFFF0F9F0),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: const Color(0xFF4BAE4F).withValues(alpha: 0.3)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Import Complete', style: GoogleFonts.inter(fontSize: 16, fontWeight: FontWeight.bold, color: const Color(0xFF2E7D32))),
                    const SizedBox(height: 10),
                    Text('Rows imported: ${_importResult!['rows_imported']}', style: const TextStyle(color: Color(0xFF2E7D32))),
                    if ((_importResult!['rows_skipped'] as int) > 0)
                      Text('Rows skipped: ${_importResult!['rows_skipped']}', style: const TextStyle(color: Colors.orange)),
                    if ((_importResult!['errors'] as List).isNotEmpty) ...[
                      const SizedBox(height: 10),
                      ExpansionTile(
                        title: Text('Errors (${(_importResult!['errors'] as List).length})', style: const TextStyle(fontSize: 13, color: Colors.red)),
                        tilePadding: EdgeInsets.zero,
                        children: (_importResult!['errors'] as List).map<Widget>((e) {
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 2),
                            child: Text('Row ${e['row']}: ${e['message']}', style: const TextStyle(fontSize: 11, color: Colors.red)),
                          );
                        }).toList(),
                      ),
                    ],
                    const SizedBox(height: 10),
                    TextButton(
                      onPressed: _reset,
                      child: const Text('Import Another File', style: TextStyle(color: Color(0xFF53AD64))),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
