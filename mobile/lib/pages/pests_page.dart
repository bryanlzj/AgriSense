import 'dart:io';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:image_picker/image_picker.dart';
import 'package:intl/intl.dart';
import 'package:fyp_prototype/services/pest_service.dart';
import 'package:fyp_prototype/models/pest_detection.dart';

class PestsPage extends StatefulWidget {
  const PestsPage({super.key});

  @override
  State<PestsPage> createState() => _PestsPageState();
}

class _PestsPageState extends State<PestsPage> {
  bool _isLoading = true;
  String? _errorMessage;
  List<PestDetection> _detections = [];
  final ImagePicker _imagePicker = ImagePicker();

  @override
  void initState() {
    super.initState();
    _loadDetections();
  }

  Future<void> _loadDetections() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final detections = await PestService.getDetections();
      if (mounted) {
        setState(() {
          _detections = detections;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = e.toString().replaceFirst('Exception: ', '');
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _showImageSourceDialog() async {
    showModalBottomSheet(
      context: context,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                'Upload Pest Image',
                style: GoogleFonts.inter(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _buildImageSourceOption(
                    icon: Icons.camera_alt,
                    label: 'Camera',
                    onTap: () {
                      Navigator.pop(context);
                      _pickImage(ImageSource.camera);
                    },
                  ),
                  _buildImageSourceOption(
                    icon: Icons.photo_library,
                    label: 'Gallery',
                    onTap: () {
                      Navigator.pop(context);
                      _pickImage(ImageSource.gallery);
                    },
                  ),
                ],
              ),
              SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildImageSourceOption({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Column(
        children: [
          Container(
            padding: EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Color(0xFF53AD64).withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, size: 32, color: Color(0xFF53AD64)),
          ),
          SizedBox(height: 8),
          Text(
            label,
            style: GoogleFonts.inter(
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _pickImage(ImageSource source) async {
    try {
      final XFile? pickedFile = await _imagePicker.pickImage(
        source: source,
        maxWidth: 1920,
        maxHeight: 1920,
        imageQuality: 85,
      );

      if (pickedFile != null) {
        _showDetectionDialog(File(pickedFile.path));
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to pick image: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _showDetectionDialog(File imageFile, {int retryCount = 0}) async {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => _DetectionDialog(
        imageFile: imageFile,
        retryCount: retryCount,
        onComplete: (result) {
          Navigator.pop(context);
          if (result != null) {
            _showResultDialog(result, imageFile);
          }
        },
      ),
    );
  }

  void _showResultDialog(EnhancedPestDetection result, File imageFile) {
    showDialog(
      context: context,
      builder: (context) => _ResultDialog(
        result: result,
        imageFile: imageFile,
        onRetry: () {
          Navigator.pop(context);
          _showDetectionDialog(imageFile, retryCount: result.canRetry ? 1 : 0);
        },
        onDone: () {
          Navigator.pop(context);
          _loadDetections();
        },
      ),
    );
  }

  Future<void> _deleteDetection(PestDetection detection) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Delete Detection'),
        content: Text('Are you sure you want to delete this detection?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: Text('Delete'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      try {
        await PestService.deleteDetection(detection.id);
        _loadDetections();
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Failed to delete detection'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFF5F5F5),
      appBar: AppBar(
        title: Text(
          'Pest Detection',
          style: GoogleFonts.inter(fontWeight: FontWeight.w600),
        ),
        backgroundColor: Color(0xFF53AD64),
        foregroundColor: Colors.white,
      ),
      body: _isLoading
          ? Center(
              child: CircularProgressIndicator(
                valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF53AD64)),
              ),
            )
          : _errorMessage != null
              ? _buildErrorWidget()
              : _detections.isEmpty
                  ? _buildEmptyWidget()
                  : RefreshIndicator(
                      onRefresh: _loadDetections,
                      color: Color(0xFF53AD64),
                      child: ListView.builder(
                        padding: EdgeInsets.all(16),
                        itemCount: _detections.length,
                        itemBuilder: (context, index) {
                          return _buildDetectionCard(_detections[index]);
                        },
                      ),
                    ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _showImageSourceDialog,
        icon: Icon(Icons.camera_alt),
        label: Text('Scan Pest'),
        backgroundColor: Color(0xFF53AD64),
        foregroundColor: Colors.white,
      ),
    );
  }

  Widget _buildErrorWidget() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.error_outline, size: 64, color: Colors.red[300]),
            SizedBox(height: 16),
            Text(
              'Failed to load detections',
              style: GoogleFonts.inter(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 8),
            Text(
              _errorMessage ?? 'Unknown error',
              style: GoogleFonts.inter(color: Colors.grey),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 24),
            ElevatedButton(
              onPressed: _loadDetections,
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF53AD64),
                foregroundColor: Colors.white,
              ),
              child: Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyWidget() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.bug_report_outlined, size: 64, color: Colors.grey[400]),
          SizedBox(height: 16),
          Text(
            'No pest detections yet',
            style: GoogleFonts.inter(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.grey[600],
            ),
          ),
          SizedBox(height: 8),
          Text(
            'Tap the button below to scan for pests',
            style: GoogleFonts.inter(color: Colors.grey),
          ),
        ],
      ),
    );
  }

  Widget _buildDetectionCard(PestDetection detection) {
    final confidenceColor = detection.confidenceScore >= 0.7
        ? Colors.green
        : detection.confidenceScore >= 0.5
            ? Colors.orange
            : Colors.red;

    return Dismissible(
      key: Key('detection_${detection.id}'),
      direction: DismissDirection.endToStart,
      background: Container(
        alignment: Alignment.centerRight,
        padding: EdgeInsets.only(right: 20),
        margin: EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(
          color: Colors.red,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Icon(Icons.delete, color: Colors.white),
      ),
      confirmDismiss: (direction) async {
        return await showDialog<bool>(
          context: context,
          builder: (context) => AlertDialog(
            title: Text('Delete Detection'),
            content: Text('Are you sure you want to delete this detection?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context, false),
                child: Text('Cancel'),
              ),
              TextButton(
                onPressed: () => Navigator.pop(context, true),
                style: TextButton.styleFrom(foregroundColor: Colors.red),
                child: Text('Delete'),
              ),
            ],
          ),
        );
      },
      onDismissed: (direction) {
        PestService.deleteDetection(detection.id);
        setState(() {
          _detections.removeWhere((d) => d.id == detection.id);
        });
      },
      child: Container(
        margin: EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.05),
              blurRadius: 10,
              offset: Offset(0, 2),
            ),
          ],
        ),
        child: Material(
          color: Colors.transparent,
          child: InkWell(
            borderRadius: BorderRadius.circular(12),
            onTap: () => _showDetectionDetails(detection),
            child: Padding(
              padding: EdgeInsets.all(12),
              child: Row(
                children: [
                  // Image thumbnail
                  ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      detection.imageUrl,
                      width: 60,
                      height: 60,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) {
                        return Container(
                          width: 60,
                          height: 60,
                          color: Colors.grey[200],
                          child: Icon(Icons.image_not_supported, color: Colors.grey),
                        );
                      },
                    ),
                  ),
                  SizedBox(width: 12),

                  // Content
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          detection.pestType,
                          style: GoogleFonts.inter(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        SizedBox(height: 4),
                        Row(
                          children: [
                            Container(
                              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                              decoration: BoxDecoration(
                                color: confidenceColor.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                '${(detection.confidenceScore * 100).toInt()}% confidence',
                                style: GoogleFonts.inter(
                                  fontSize: 11,
                                  fontWeight: FontWeight.w600,
                                  color: confidenceColor,
                                ),
                              ),
                            ),
                          ],
                        ),
                        SizedBox(height: 4),
                        Text(
                          DateFormat('MMM d, yyyy h:mm a').format(detection.detectedAt),
                          style: GoogleFonts.inter(
                            fontSize: 12,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  ),

                  Icon(Icons.chevron_right, color: Colors.grey),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  void _showDetectionDetails(PestDetection detection) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.5,
        maxChildSize: 0.95,
        expand: false,
        builder: (context, scrollController) => SingleChildScrollView(
          controller: scrollController,
          child: Padding(
            padding: EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Center(
                  child: Container(
                    width: 40,
                    height: 4,
                    decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ),
                SizedBox(height: 20),

                // Image
                ClipRRect(
                  borderRadius: BorderRadius.circular(12),
                  child: Image.network(
                    detection.imageUrl,
                    width: double.infinity,
                    height: 200,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) {
                      return Container(
                        width: double.infinity,
                        height: 200,
                        color: Colors.grey[200],
                        child: Icon(Icons.image_not_supported, size: 48, color: Colors.grey),
                      );
                    },
                  ),
                ),
                SizedBox(height: 20),

                // Pest type
                Text(
                  detection.pestType,
                  style: GoogleFonts.inter(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                if (detection.scientificName != null) ...[
                  SizedBox(height: 4),
                  Text(
                    detection.scientificName!,
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      fontStyle: FontStyle.italic,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
                SizedBox(height: 12),

                // Confidence and danger level
                Row(
                  children: [
                    Icon(Icons.analytics, size: 20, color: Colors.grey),
                    SizedBox(width: 8),
                    Text(
                      'Confidence: ${(detection.confidenceScore * 100).toInt()}%',
                      style: GoogleFonts.inter(
                        fontSize: 16,
                        color: Colors.grey[700],
                      ),
                    ),
                    if (detection.dangerLevel != null) ...[
                      SizedBox(width: 16),
                      Container(
                        padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: detection.dangerLevel == 'high'
                              ? Colors.red.withAlpha(26)
                              : detection.dangerLevel == 'medium'
                                  ? Colors.orange.withAlpha(26)
                                  : Colors.green.withAlpha(26),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          detection.dangerLevel!.toUpperCase(),
                          style: GoogleFonts.inter(
                            fontSize: 11,
                            fontWeight: FontWeight.w600,
                            color: detection.dangerLevel == 'high'
                                ? Colors.red
                                : detection.dangerLevel == 'medium'
                                    ? Colors.orange
                                    : Colors.green,
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
                SizedBox(height: 8),

                // Date
                Row(
                  children: [
                    Icon(Icons.calendar_today, size: 20, color: Colors.grey),
                    SizedBox(width: 8),
                    Text(
                      DateFormat('MMMM d, yyyy at h:mm a').format(detection.detectedAt),
                      style: GoogleFonts.inter(
                        fontSize: 16,
                        color: Colors.grey[700],
                      ),
                    ),
                  ],
                ),

                // Description
                if (detection.description != null) ...[
                  SizedBox(height: 20),
                  Text(
                    'About this pest',
                    style: GoogleFonts.inter(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    detection.description!,
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      color: Colors.grey[700],
                      height: 1.5,
                    ),
                  ),
                ],

                // Recommendations
                if (detection.pestRecommendations != null &&
                    detection.pestRecommendations!.isNotEmpty) ...[
                  SizedBox(height: 20),
                  Text(
                    'Recommendations',
                    style: GoogleFonts.inter(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  SizedBox(height: 8),
                  ...detection.pestRecommendations!.map((rec) => Padding(
                    padding: EdgeInsets.only(bottom: 6),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('• ', style: GoogleFonts.inter(fontSize: 14, color: Color(0xFF53AD64))),
                        Expanded(
                          child: Text(
                            rec,
                            style: GoogleFonts.inter(fontSize: 14, color: Colors.grey[700], height: 1.4),
                          ),
                        ),
                      ],
                    ),
                  )),
                ],

                // User notes
                if (detection.recommendations != null) ...[
                  SizedBox(height: 20),
                  Text(
                    'Notes',
                    style: GoogleFonts.inter(
                      fontSize: 18,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    detection.recommendations!,
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      color: Colors.grey[700],
                    ),
                  ),
                ],

                SizedBox(height: 30),

                // Delete button
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton.icon(
                    onPressed: () {
                      Navigator.pop(context);
                      _deleteDetection(detection);
                    },
                    icon: Icon(Icons.delete_outline),
                    label: Text('Delete Detection'),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.red,
                      side: BorderSide(color: Colors.red),
                      padding: EdgeInsets.symmetric(vertical: 12),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

/// Dialog that shows detection progress
class _DetectionDialog extends StatefulWidget {
  final File imageFile;
  final int retryCount;
  final Function(EnhancedPestDetection?) onComplete;

  const _DetectionDialog({
    required this.imageFile,
    required this.retryCount,
    required this.onComplete,
  });

  @override
  State<_DetectionDialog> createState() => _DetectionDialogState();
}

class _DetectionDialogState extends State<_DetectionDialog> {
  bool _isAnalyzing = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _analyze();
  }

  Future<void> _analyze() async {
    try {
      final result = await PestService.detectPest(
        imageFile: widget.imageFile,
        retryCount: widget.retryCount,
      );
      if (mounted) {
        widget.onComplete(result);
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isAnalyzing = false;
          _errorMessage = e.toString().replaceFirst('Exception: ', '');
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (_isAnalyzing) ...[
            SizedBox(height: 20),
            CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF53AD64)),
            ),
            SizedBox(height: 20),
            Text(
              'Analyzing image...',
              style: GoogleFonts.inter(fontSize: 16),
            ),
            SizedBox(height: 8),
            Text(
              'This may take a few seconds',
              style: GoogleFonts.inter(fontSize: 13, color: Colors.grey),
            ),
            SizedBox(height: 20),
          ] else if (_errorMessage != null) ...[
            Icon(Icons.error_outline, size: 48, color: Colors.red),
            SizedBox(height: 16),
            Text(
              'Analysis Failed',
              style: GoogleFonts.inter(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 8),
            Text(
              _errorMessage!,
              style: GoogleFonts.inter(fontSize: 14, color: Colors.grey),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                TextButton(
                  onPressed: () => widget.onComplete(null),
                  child: Text('Cancel'),
                ),
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _isAnalyzing = true;
                      _errorMessage = null;
                    });
                    _analyze();
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFF53AD64),
                    foregroundColor: Colors.white,
                  ),
                  child: Text('Retry'),
                ),
              ],
            ),
          ],
        ],
      ),
    );
  }
}

/// Dialog that shows detection results
class _ResultDialog extends StatelessWidget {
  final EnhancedPestDetection result;
  final File imageFile;
  final VoidCallback onRetry;
  final VoidCallback onDone;

  const _ResultDialog({
    required this.result,
    required this.imageFile,
    required this.onRetry,
    required this.onDone,
  });

  @override
  Widget build(BuildContext context) {
    Color statusColor;
    IconData statusIcon;
    String statusText;

    if (result.isDetected) {
      statusColor = Colors.green;
      statusIcon = Icons.check_circle;
      statusText = 'Pest Detected';
    } else if (result.isPartial) {
      statusColor = Colors.orange;
      statusIcon = Icons.help;
      statusText = 'Possible Match';
    } else {
      statusColor = Colors.red;
      statusIcon = Icons.help_outline;
      statusText = 'Unable to Identify';
    }

    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Status icon
              Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: statusColor.withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: Icon(statusIcon, size: 48, color: statusColor),
              ),
              SizedBox(height: 16),

              // Status text
              Text(
                statusText,
                style: GoogleFonts.inter(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: statusColor,
                ),
              ),
              SizedBox(height: 8),

              // Confidence
              Text(
                '${result.confidencePercent}% confidence',
                style: GoogleFonts.inter(
                  fontSize: 14,
                  color: Colors.grey,
                ),
              ),
              SizedBox(height: 16),

              // Pest info (if detected)
              if (result.pestName != null) ...[
                Container(
                  padding: EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        result.pestName!,
                        style: GoogleFonts.inter(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (result.scientificName != null) ...[
                        SizedBox(height: 4),
                        Text(
                          result.scientificName!,
                          style: GoogleFonts.inter(
                            fontSize: 14,
                            fontStyle: FontStyle.italic,
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                      if (result.description != null) ...[
                        SizedBox(height: 8),
                        Text(
                          result.description!,
                          style: GoogleFonts.inter(fontSize: 14),
                        ),
                      ],
                      if (result.dangerLevel != null) ...[
                        SizedBox(height: 12),
                        Row(
                          children: [
                            Icon(
                              Icons.warning_amber,
                              size: 16,
                              color: _getDangerColor(result.dangerLevel!),
                            ),
                            SizedBox(width: 4),
                            Text(
                              'Danger: ${result.dangerLevel!.toUpperCase()}',
                              style: GoogleFonts.inter(
                                fontSize: 13,
                                fontWeight: FontWeight.w600,
                                color: _getDangerColor(result.dangerLevel!),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ],
                  ),
                ),
                SizedBox(height: 16),
              ],

              // Recommendations (if available)
              if (result.recommendations != null && result.recommendations!.isNotEmpty) ...[
                Container(
                  width: double.infinity,
                  padding: EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Color(0xFF53AD64).withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Recommendations',
                        style: GoogleFonts.inter(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Color(0xFF53AD64),
                        ),
                      ),
                      SizedBox(height: 8),
                      ...result.recommendations!.map((rec) => Padding(
                        padding: EdgeInsets.only(bottom: 4),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('• ', style: GoogleFonts.inter(fontSize: 14)),
                            Expanded(
                              child: Text(
                                rec,
                                style: GoogleFonts.inter(fontSize: 14),
                              ),
                            ),
                          ],
                        ),
                      )),
                    ],
                  ),
                ),
                SizedBox(height: 16),
              ],

              // Retry tip (if available)
              if (result.retryTip != null) ...[
                Container(
                  width: double.infinity,
                  padding: EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.amber[50],
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.amber),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.lightbulb_outline, color: Colors.amber[700], size: 20),
                      SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          result.retryTip!,
                          style: GoogleFonts.inter(
                            fontSize: 13,
                            color: Colors.amber[900],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 16),
              ],

              // Action buttons
              Row(
                children: [
                  if (result.canRetry) ...[
                    Expanded(
                      child: OutlinedButton(
                        onPressed: onRetry,
                        child: Text('Try Again'),
                      ),
                    ),
                    SizedBox(width: 12),
                  ],
                  Expanded(
                    child: ElevatedButton(
                      onPressed: onDone,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFF53AD64),
                        foregroundColor: Colors.white,
                      ),
                      child: Text('Done'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getDangerColor(String level) {
    switch (level.toLowerCase()) {
      case 'high':
        return Colors.red;
      case 'medium':
        return Colors.orange;
      default:
        return Colors.green;
    }
  }
}
