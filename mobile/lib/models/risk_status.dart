class RiskStatus {
  final String weatherRisk;
  final String pestRisk;

  RiskStatus({
    required this.weatherRisk,
    required this.pestRisk,
  });

  factory RiskStatus.fromJson(Map<String, dynamic> json) {
    return RiskStatus(
      weatherRisk: json['weatherRisk'],
      pestRisk: json['pestRisk'],
    );
  }
}
