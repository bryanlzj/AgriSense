class RiskStatus {
  final String status;
  final String headline;
  final String description;
  final bool actionRequired;
  final String overallRisk;
  final int totalRisks;

  RiskStatus({
    required this.status,
    required this.headline,
    required this.description,
    required this.actionRequired,
    required this.overallRisk,
    required this.totalRisks,
  });

  /// Creates RiskStatus from backend API pest_risk response.
  factory RiskStatus.fromJson(Map<String, dynamic> json) {
    return RiskStatus(
      status: json['status'] as String? ?? 'unknown',
      headline: json['headline'] as String? ?? 'Unknown',
      description: json['description'] as String? ?? '',
      actionRequired: json['action_required'] as bool? ?? false,
      overallRisk: json['overall_risk'] as String? ?? 'unknown',
      totalRisks: json['total_risks'] as int? ?? 0,
    );
  }

  /// Returns a color-coded risk level for display.
  String get riskLevel {
    switch (overallRisk.toLowerCase()) {
      case 'critical':
      case 'high':
        return 'High';
      case 'medium':
        return 'Medium';
      case 'low':
        return 'Low';
      case 'none':
        return 'None';
      default:
        return 'Unknown';
    }
  }

  /// Returns an icon based on risk level.
  String get icon {
    switch (overallRisk.toLowerCase()) {
      case 'critical':
      case 'high':
        return '🔴';
      case 'medium':
        return '🟡';
      case 'low':
        return '🟢';
      case 'none':
        return '✅';
      default:
        return '⚪';
    }
  }
}
