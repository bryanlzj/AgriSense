import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:fyp_prototype/services/alert_service.dart';
import 'package:fyp_prototype/models/alert.dart';

class AlertsPage extends StatefulWidget {
  const AlertsPage({super.key});

  @override
  State<AlertsPage> createState() => _AlertsPageState();
}

class _AlertsPageState extends State<AlertsPage> {
  bool _isLoading = true;
  String? _errorMessage;
  List<Alert> _alerts = [];
  String? _selectedType;
  String? _selectedSeverity;
  bool? _showUnreadOnly;

  final List<String> _alertTypes = ['weather', 'pest', 'system', 'environmental'];
  final List<String> _severities = ['low', 'medium', 'high', 'critical'];

  @override
  void initState() {
    super.initState();
    _loadAlerts();
  }

  Future<void> _loadAlerts() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final response = await AlertService.getAlerts(
        type: _selectedType,
        severity: _selectedSeverity,
        isRead: _showUnreadOnly == true ? false : null,
      );

      if (mounted) {
        setState(() {
          _alerts = response.alerts;
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

  Future<void> _markAsRead(Alert alert) async {
    try {
      await AlertService.markAsRead(alert.id);
      _loadAlerts();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to mark as read'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _deleteAlert(Alert alert) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Delete Alert'),
        content: Text('Are you sure you want to delete this alert?'),
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
        await AlertService.deleteAlert(alert.id);
        _loadAlerts();
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Failed to delete alert'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  Future<void> _markAllAsRead() async {
    final unreadIds = _alerts.where((a) => !a.isRead).map((a) => a.id).toList();
    if (unreadIds.isEmpty) return;

    try {
      await AlertService.bulkMarkAsRead(unreadIds);
      _loadAlerts();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('All alerts marked as read'),
            backgroundColor: Color(0xFF53AD64),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to mark alerts as read'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color(0xFFF5F5F5),
      appBar: AppBar(
        title: Text(
          'Alerts',
          style: GoogleFonts.inter(fontWeight: FontWeight.w600),
        ),
        backgroundColor: Color(0xFF53AD64),
        foregroundColor: Colors.white,
        actions: [
          if (_alerts.any((a) => !a.isRead))
            TextButton(
              onPressed: _markAllAsRead,
              child: Text(
                'Mark all read',
                style: TextStyle(color: Colors.white),
              ),
            ),
        ],
      ),
      body: Column(
        children: [
          // Filters
          _buildFilters(),

          // Content
          Expanded(
            child: _isLoading
                ? Center(
                    child: CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF53AD64)),
                    ),
                  )
                : _errorMessage != null
                    ? _buildErrorWidget()
                    : _alerts.isEmpty
                        ? _buildEmptyWidget()
                        : RefreshIndicator(
                            onRefresh: _loadAlerts,
                            color: Color(0xFF53AD64),
                            child: ListView.builder(
                              padding: EdgeInsets.all(16),
                              itemCount: _alerts.length,
                              itemBuilder: (context, index) {
                                return _buildAlertCard(_alerts[index]);
                              },
                            ),
                          ),
          ),
        ],
      ),
    );
  }

  Widget _buildFilters() {
    return Container(
      padding: EdgeInsets.all(12),
      color: Colors.white,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: [
            // Type filter
            _buildFilterChip(
              label: _selectedType ?? 'All Types',
              isSelected: _selectedType != null,
              onTap: () => _showTypeFilter(),
            ),
            SizedBox(width: 8),

            // Severity filter
            _buildFilterChip(
              label: _selectedSeverity ?? 'All Severities',
              isSelected: _selectedSeverity != null,
              onTap: () => _showSeverityFilter(),
            ),
            SizedBox(width: 8),

            // Unread only toggle
            FilterChip(
              label: Text('Unread only'),
              selected: _showUnreadOnly == true,
              onSelected: (selected) {
                setState(() {
                  _showUnreadOnly = selected ? true : null;
                });
                _loadAlerts();
              },
              selectedColor: Color(0xFF53AD64).withOpacity(0.2),
              checkmarkColor: Color(0xFF53AD64),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFilterChip({
    required String label,
    required bool isSelected,
    required VoidCallback onTap,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected ? Color(0xFF53AD64).withOpacity(0.2) : Colors.grey[200],
          borderRadius: BorderRadius.circular(20),
          border: isSelected ? Border.all(color: Color(0xFF53AD64)) : null,
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              label,
              style: GoogleFonts.inter(
                fontSize: 13,
                color: isSelected ? Color(0xFF53AD64) : Colors.grey[700],
                fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
              ),
            ),
            SizedBox(width: 4),
            Icon(
              Icons.arrow_drop_down,
              size: 18,
              color: isSelected ? Color(0xFF53AD64) : Colors.grey[700],
            ),
          ],
        ),
      ),
    );
  }

  void _showTypeFilter() {
    showModalBottomSheet(
      context: context,
      builder: (context) => Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          ListTile(
            title: Text('All Types'),
            leading: _selectedType == null
                ? Icon(Icons.check, color: Color(0xFF53AD64))
                : SizedBox(width: 24),
            onTap: () {
              setState(() => _selectedType = null);
              Navigator.pop(context);
              _loadAlerts();
            },
          ),
          ..._alertTypes.map((type) => ListTile(
            title: Text(type[0].toUpperCase() + type.substring(1)),
            leading: _selectedType == type
                ? Icon(Icons.check, color: Color(0xFF53AD64))
                : SizedBox(width: 24),
            onTap: () {
              setState(() => _selectedType = type);
              Navigator.pop(context);
              _loadAlerts();
            },
          )).toList(),
        ],
      ),
    );
  }

  void _showSeverityFilter() {
    showModalBottomSheet(
      context: context,
      builder: (context) => Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          ListTile(
            title: Text('All Severities'),
            leading: _selectedSeverity == null
                ? Icon(Icons.check, color: Color(0xFF53AD64))
                : SizedBox(width: 24),
            onTap: () {
              setState(() => _selectedSeverity = null);
              Navigator.pop(context);
              _loadAlerts();
            },
          ),
          ..._severities.map((severity) => ListTile(
            title: Text(severity[0].toUpperCase() + severity.substring(1)),
            leading: _selectedSeverity == severity
                ? Icon(Icons.check, color: Color(0xFF53AD64))
                : SizedBox(width: 24),
            onTap: () {
              setState(() => _selectedSeverity = severity);
              Navigator.pop(context);
              _loadAlerts();
            },
          )).toList(),
        ],
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
              'Failed to load alerts',
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
              onPressed: _loadAlerts,
              style: ElevatedButton.styleFrom(
                backgroundColor: Color(0xFF4BAE4F),
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
          Icon(Icons.notifications_none, size: 64, color: Colors.grey[400]),
          SizedBox(height: 16),
          Text(
            'No alerts',
            style: GoogleFonts.inter(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.grey[600],
            ),
          ),
          SizedBox(height: 8),
          Text(
            _selectedType != null || _selectedSeverity != null || _showUnreadOnly == true
                ? 'Try adjusting your filters'
                : 'You\'re all caught up!',
            style: GoogleFonts.inter(color: Colors.grey),
          ),
        ],
      ),
    );
  }

  Widget _buildAlertCard(Alert alert) {
    Color severityColor;
    switch (alert.severity.toLowerCase()) {
      case 'critical':
        severityColor = Colors.red[700]!;
        break;
      case 'high':
        severityColor = Colors.red;
        break;
      case 'medium':
        severityColor = Colors.orange;
        break;
      default:
        severityColor = Colors.blue;
    }

    return Dismissible(
      key: Key('alert_${alert.id}'),
      direction: DismissDirection.endToStart,
      background: Container(
        alignment: Alignment.centerRight,
        padding: EdgeInsets.only(right: 20),
        color: Colors.red,
        child: Icon(Icons.delete, color: Colors.white),
      ),
      confirmDismiss: (direction) async {
        return await showDialog<bool>(
          context: context,
          builder: (context) => AlertDialog(
            title: Text('Delete Alert'),
            content: Text('Are you sure you want to delete this alert?'),
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
        AlertService.deleteAlert(alert.id);
        setState(() {
          _alerts.removeWhere((a) => a.id == alert.id);
        });
      },
      child: Container(
        margin: EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: alert.isRead ? Colors.transparent : severityColor.withOpacity(0.3),
            width: alert.isRead ? 0 : 2,
          ),
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
            onTap: () {
              if (!alert.isRead) {
                _markAsRead(alert);
              }
            },
            child: Padding(
              padding: EdgeInsets.all(16),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Icon
                  Container(
                    padding: EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: severityColor.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(alert.icon, style: TextStyle(fontSize: 20)),
                  ),
                  SizedBox(width: 12),

                  // Content
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Expanded(
                              child: Text(
                                alert.title,
                                style: GoogleFonts.inter(
                                  fontSize: 14,
                                  fontWeight: alert.isRead
                                      ? FontWeight.w500
                                      : FontWeight.w700,
                                  color: alert.isRead ? Colors.grey[700] : Colors.black,
                                ),
                              ),
                            ),
                            Container(
                              padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                              decoration: BoxDecoration(
                                color: severityColor.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(
                                alert.severityDisplay,
                                style: GoogleFonts.inter(
                                  fontSize: 10,
                                  fontWeight: FontWeight.w600,
                                  color: severityColor,
                                ),
                              ),
                            ),
                          ],
                        ),
                        SizedBox(height: 4),
                        Text(
                          alert.message,
                          style: GoogleFonts.inter(
                            fontSize: 13,
                            color: Colors.grey[600],
                          ),
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                        SizedBox(height: 8),
                        Row(
                          children: [
                            Icon(Icons.access_time, size: 12, color: Colors.grey),
                            SizedBox(width: 4),
                            Text(
                              alert.timeAgo,
                              style: GoogleFonts.inter(
                                fontSize: 11,
                                color: Colors.grey,
                              ),
                            ),
                            Spacer(),
                            if (!alert.isRead)
                              Container(
                                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                decoration: BoxDecoration(
                                  color: Colors.blue,
                                  borderRadius: BorderRadius.circular(10),
                                ),
                                child: Text(
                                  'NEW',
                                  style: GoogleFonts.inter(
                                    fontSize: 9,
                                    fontWeight: FontWeight.w600,
                                    color: Colors.white,
                                  ),
                                ),
                              ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
