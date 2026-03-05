import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:fyp_prototype/services/auth_service.dart';
import 'package:fyp_prototype/services/weather_service.dart';
import 'package:fyp_prototype/utils/token_storage.dart';
import 'package:fyp_prototype/models/user.dart';
import 'package:fyp_prototype/models/sensor_weather.dart';

class WeatherPage extends StatefulWidget {
  const WeatherPage({super.key});

  @override
  State<WeatherPage> createState() => _WeatherPageState();
}

class _WeatherPageState extends State<WeatherPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  // Current tab data
  bool _currentLoading = true;
  String? _currentError;
  SensorCurrentWeather? _sensorCurrent;

  // Historical tab data
  bool _historicalLoading = false;
  String? _historicalError;
  HistoricalWeatherData? _historicalData;
  String _selectedPeriod = '24h';
  DateTimeRange? _customDateRange;

  // Forecast tab data
  bool _forecastLoading = true;
  String? _forecastError;
  WeatherSummaryData? _forecastData;
  User? _user;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _tabController.addListener(_onTabChanged);
    _loadCurrentWeather();
    _loadForecastData();
  }

  @override
  void dispose() {
    _tabController.removeListener(_onTabChanged);
    _tabController.dispose();
    super.dispose();
  }

  void _onTabChanged() {
    if (!_tabController.indexIsChanging) return;
    if (_tabController.index == 1 && _historicalData == null && !_historicalLoading) {
      _loadHistoricalData();
    }
  }

  Future<void> _loadCurrentWeather() async {
    setState(() {
      _currentLoading = true;
      _currentError = null;
    });

    try {
      final data = await WeatherService.getSensorCurrent();
      if (mounted) {
        setState(() {
          _sensorCurrent = data;
          _currentLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _currentError = e.toString().replaceFirst('Exception: ', '');
          _currentLoading = false;
        });
      }
    }
  }

  Future<void> _loadHistoricalData() async {
    setState(() {
      _historicalLoading = true;
      _historicalError = null;
    });

    try {
      String? startDate;
      String? endDate;
      if (_selectedPeriod == 'custom' && _customDateRange != null) {
        startDate = DateFormat('yyyy-MM-dd').format(_customDateRange!.start);
        endDate = DateFormat('yyyy-MM-dd').format(_customDateRange!.end);
      }

      final data = await WeatherService.getHistorical(
        period: _selectedPeriod,
        startDate: startDate,
        endDate: endDate,
      );

      if (mounted) {
        setState(() {
          _historicalData = data;
          _historicalLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _historicalError = e.toString().replaceFirst('Exception: ', '');
          _historicalLoading = false;
        });
      }
    }
  }

  Future<void> _loadForecastData() async {
    setState(() {
      _forecastLoading = true;
      _forecastError = null;
    });

    try {
      final token = await TokenStorage.getToken();
      if (token == null) throw Exception('Not authenticated');

      final user = await AuthService.getCurrentUser(token);
      final weatherData = await WeatherService.getSummary(
        latitude: user.farmLocationLat,
        longitude: user.farmLocationLng,
        locationName: user.farmLocationName,
      );

      if (mounted) {
        setState(() {
          _user = user;
          _forecastData = weatherData;
          _forecastLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _forecastError = e.toString().replaceFirst('Exception: ', '');
          _forecastLoading = false;
        });
      }
    }
  }

  // --- Weather condition helpers ---

  IconData _getWeatherIcon(String? condition) {
    switch (condition) {
      case 'Sunny':
        return Icons.wb_sunny;
      case 'Cloudy':
        return Icons.cloud;
      case 'Light Rain':
        return Icons.grain;
      case 'Heavy Rain':
        return Icons.thunderstorm;
      default:
        return Icons.help_outline;
    }
  }

  Color _getWeatherColor(String? condition) {
    switch (condition) {
      case 'Sunny':
        return Colors.orange;
      case 'Cloudy':
        return const Color(0xFF78909C);
      case 'Light Rain':
        return Colors.lightBlue;
      case 'Heavy Rain':
        return const Color(0xFF1565C0);
      default:
        return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F5F5),
      body: NestedScrollView(
        headerSliverBuilder: (context, innerBoxIsScrolled) {
          return [
            SliverAppBar(
              expandedHeight: 140,
              floating: false,
              pinned: true,
              backgroundColor: const Color(0xFF53AD64),
              flexibleSpace: FlexibleSpaceBar(
                background: Container(
                  decoration: const BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [Color(0xFF53AD64), Color(0xFF2E7D32)],
                    ),
                  ),
                  child: SafeArea(
                    child: Center(
                      child: Padding(
                        padding: const EdgeInsets.only(top: 8),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(
                              _sensorCurrent != null
                                  ? _getWeatherIcon(
                                      _sensorCurrent!.weatherCondition)
                                  : Icons.cloud,
                              size: 40,
                              color: Colors.white,
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Weather',
                              style: GoogleFonts.inter(
                                fontSize: 22,
                                fontWeight: FontWeight.w600,
                                color: Colors.white,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              bottom: TabBar(
                controller: _tabController,
                indicatorColor: Colors.white,
                indicatorWeight: 3,
                labelColor: Colors.white,
                unselectedLabelColor: Colors.white60,
                labelStyle: GoogleFonts.inter(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                ),
                unselectedLabelStyle: GoogleFonts.inter(
                  fontSize: 14,
                  fontWeight: FontWeight.w400,
                ),
                tabs: const [
                  Tab(text: 'Current'),
                  Tab(text: 'Historical'),
                  Tab(text: 'Forecast'),
                ],
              ),
            ),
          ];
        },
        body: TabBarView(
          controller: _tabController,
          children: [
            _buildCurrentTab(),
            _buildHistoricalTab(),
            _buildForecastTab(),
          ],
        ),
      ),
    );
  }

  // ============================
  // TAB 1: Current (Sensor + ML)
  // ============================

  Widget _buildCurrentTab() {
    if (_currentLoading) {
      return const Center(
        child: CircularProgressIndicator(
          valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF53AD64)),
        ),
      );
    }

    if (_currentError != null) {
      return _buildErrorWidget(_currentError!, _loadCurrentWeather);
    }

    final data = _sensorCurrent!;

    return RefreshIndicator(
      color: const Color(0xFF53AD64),
      onRefresh: _loadCurrentWeather,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Weather condition hero card
            _buildConditionHeroCard(data),
            const SizedBox(height: 16),

            // Sensor metrics grid
            _buildSensorMetricsGrid(data),
            const SizedBox(height: 16),

            // Last updated + source
            _buildSourceInfoCard(data),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  Widget _buildConditionHeroCard(SensorCurrentWeather data) {
    final condition = data.weatherCondition;
    final confidence = data.confidence;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          Icon(
            _getWeatherIcon(condition),
            size: 64,
            color: _getWeatherColor(condition),
          ),
          const SizedBox(height: 12),
          Text(
            condition ?? 'Unknown',
            style: GoogleFonts.inter(
              fontSize: 24,
              fontWeight: FontWeight.w700,
              color: const Color(0xFF333333),
            ),
          ),
          const SizedBox(height: 8),
          if (confidence != null)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: const Color(0xFF53AD64).withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                '${(confidence * 100).toStringAsFixed(1)}% confidence',
                style: GoogleFonts.inter(
                  fontSize: 13,
                  fontWeight: FontWeight.w600,
                  color: const Color(0xFF2E7D32),
                ),
              ),
            ),
          if (!data.modelLoaded) ...[
            const SizedBox(height: 8),
            Text(
              'ML model not loaded - using fallback',
              style: GoogleFonts.inter(
                fontSize: 12,
                color: Colors.orange,
                fontStyle: FontStyle.italic,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildSensorMetricsGrid(SensorCurrentWeather data) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Sensor Readings',
          style: GoogleFonts.inter(
            fontSize: 18,
            fontWeight: FontWeight.w600,
            color: const Color(0xFF333333),
          ),
        ),
        const SizedBox(height: 12),
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          mainAxisSpacing: 12,
          crossAxisSpacing: 12,
          childAspectRatio: 1.6,
          children: [
            _buildMetricCard(
              Icons.thermostat,
              'Temperature',
              '${data.temperature.toStringAsFixed(1)}°C',
              Colors.red.shade400,
            ),
            _buildMetricCard(
              Icons.water_drop,
              'Humidity',
              '${data.relativeHumidity.toStringAsFixed(1)}%',
              Colors.blue.shade400,
            ),
            _buildMetricCard(
              Icons.air,
              'Wind Speed',
              '${data.windSpeed.toStringAsFixed(1)} m/s',
              Colors.teal.shade400,
            ),
            _buildMetricCard(
              Icons.umbrella,
              'Rainfall',
              '${data.rain.toStringAsFixed(1)} mm',
              Colors.indigo.shade400,
            ),
            _buildMetricCard(
              Icons.landscape,
              'Soil Temp',
              data.soilTemperature != null
                  ? '${data.soilTemperature!.toStringAsFixed(1)}°C'
                  : 'N/A',
              Colors.brown.shade400,
            ),
            _buildMetricCard(
              Icons.grass,
              'Soil Moisture',
              '${data.soilMoisture.toStringAsFixed(1)}%',
              const Color(0xFF53AD64),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildMetricCard(
      IconData icon, String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  label,
                  style: GoogleFonts.inter(
                    fontSize: 12,
                    color: const Color(0xFF999999),
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: GoogleFonts.inter(
              fontSize: 20,
              fontWeight: FontWeight.w700,
              color: const Color(0xFF333333),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSourceInfoCard(SensorCurrentWeather data) {
    final now = DateTime.now();
    final diff = now.difference(data.timestamp.toLocal());
    String timeAgo;
    if (diff.inMinutes < 1) {
      timeAgo = 'Just now';
    } else if (diff.inMinutes < 60) {
      timeAgo = '${diff.inMinutes} minutes ago';
    } else if (diff.inHours < 24) {
      timeAgo = '${diff.inHours} hours ago';
    } else {
      timeAgo = DateFormat('dd/MM HH:mm').format(data.timestamp.toLocal());
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          const Icon(Icons.sensors, color: Color(0xFF53AD64), size: 20),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Sensor Data + AI Classification',
                  style: GoogleFonts.inter(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: const Color(0xFF2E7D32),
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  'Last updated: $timeAgo',
                  style: GoogleFonts.inter(
                    fontSize: 12,
                    color: const Color(0xFF999999),
                  ),
                ),
              ],
            ),
          ),
          IconButton(
            icon: const Icon(Icons.refresh, color: Color(0xFF53AD64)),
            onPressed: _loadCurrentWeather,
          ),
        ],
      ),
    );
  }

  // ============================
  // TAB 2: Historical
  // ============================

  Widget _buildHistoricalTab() {
    return RefreshIndicator(
      color: const Color(0xFF53AD64),
      onRefresh: _loadHistoricalData,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Period selector
            _buildPeriodSelector(),
            const SizedBox(height: 16),

            if (_historicalLoading)
              const SizedBox(
                height: 300,
                child: Center(
                  child: CircularProgressIndicator(
                    valueColor:
                        AlwaysStoppedAnimation<Color>(Color(0xFF53AD64)),
                  ),
                ),
              )
            else if (_historicalError != null)
              _buildInlineError(_historicalError!, _loadHistoricalData)
            else if (_historicalData == null ||
                _historicalData!.readings.isEmpty)
              _buildEmptyHistorical()
            else ...[
              // Temperature chart
              _buildChartCard(
                'Temperature',
                '°C',
                _historicalData!.readings
                    .map((r) => _ChartPoint(r.timestamp, r.temperature))
                    .toList(),
                const Color(0xFFEF5350),
              ),
              const SizedBox(height: 16),

              // Humidity chart
              _buildChartCard(
                'Humidity',
                '%',
                _historicalData!.readings
                    .map((r) => _ChartPoint(r.timestamp, r.relativeHumidity))
                    .toList(),
                const Color(0xFF42A5F5),
              ),
              const SizedBox(height: 16),

              // Summary card
              _buildHistoricalSummaryCard(),
              const SizedBox(height: 20),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildPeriodSelector() {
    return Container(
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          _buildPeriodButton('24h', '24h'),
          _buildPeriodButton('7d', '7d'),
          _buildPeriodButton('custom', 'Custom'),
        ],
      ),
    );
  }

  Widget _buildPeriodButton(String value, String label) {
    final isSelected = _selectedPeriod == value;
    return Expanded(
      child: GestureDetector(
        onTap: () async {
          if (value == 'custom') {
            final range = await showDateRangePicker(
              context: context,
              firstDate: DateTime.now().subtract(const Duration(days: 365)),
              lastDate: DateTime.now(),
              initialDateRange: _customDateRange,
              builder: (context, child) {
                return Theme(
                  data: Theme.of(context).copyWith(
                    colorScheme: const ColorScheme.light(
                      primary: Color(0xFF53AD64),
                    ),
                  ),
                  child: child!,
                );
              },
            );
            if (range != null) {
              setState(() {
                _customDateRange = range;
                _selectedPeriod = 'custom';
              });
              _loadHistoricalData();
            }
          } else {
            setState(() {
              _selectedPeriod = value;
            });
            _loadHistoricalData();
          }
        },
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFF53AD64) : Colors.transparent,
            borderRadius: BorderRadius.circular(10),
          ),
          child: Center(
            child: Text(
              label,
              style: GoogleFonts.inter(
                fontSize: 14,
                fontWeight: FontWeight.w600,
                color: isSelected ? Colors.white : const Color(0xFF666666),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildEmptyHistorical() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(40),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          const Icon(Icons.timeline, size: 48, color: Colors.grey),
          const SizedBox(height: 12),
          Text(
            'No data for this period',
            style: GoogleFonts.inter(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: const Color(0xFF666666),
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Sensor readings will appear here once available.',
            style: GoogleFonts.inter(
              fontSize: 13,
              color: const Color(0xFF999999),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildChartCard(
      String title, String unit, List<_ChartPoint> points, Color lineColor) {
    if (points.isEmpty) return const SizedBox.shrink();

    // Determine how many x-axis labels to show (avoid crowding)
    final labelInterval = (points.length / 6).ceil().clamp(1, points.length);

    final minY =
        points.map((p) => p.value).reduce((a, b) => a < b ? a : b) - 2;
    final maxY =
        points.map((p) => p.value).reduce((a, b) => a > b ? a : b) + 2;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '$title ($unit)',
            style: GoogleFonts.inter(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: const Color(0xFF2E7D32),
            ),
          ),
          const SizedBox(height: 16),
          SizedBox(
            height: 200,
            child: LineChart(
              LineChartData(
                gridData: FlGridData(
                  show: true,
                  drawVerticalLine: false,
                  horizontalInterval: ((maxY - minY) / 4).clamp(1, 100),
                  getDrawingHorizontalLine: (value) => FlLine(
                    color: Colors.grey.shade200,
                    strokeWidth: 1,
                  ),
                ),
                titlesData: FlTitlesData(
                  topTitles: const AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                  rightTitles: const AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                  leftTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 40,
                      getTitlesWidget: (value, meta) {
                        return Text(
                          value.toStringAsFixed(0),
                          style: GoogleFonts.inter(
                            fontSize: 10,
                            color: const Color(0xFF999999),
                          ),
                        );
                      },
                    ),
                  ),
                  bottomTitles: AxisTitles(
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 30,
                      interval: labelInterval.toDouble(),
                      getTitlesWidget: (value, meta) {
                        final idx = value.toInt();
                        if (idx < 0 || idx >= points.length) {
                          return const SizedBox.shrink();
                        }
                        final dt = points[idx].time.toLocal();
                        final label = _selectedPeriod == '7d' ||
                                _selectedPeriod == 'custom'
                            ? DateFormat('dd/MM').format(dt)
                            : DateFormat('HH:mm').format(dt);
                        return Padding(
                          padding: const EdgeInsets.only(top: 8),
                          child: Text(
                            label,
                            style: GoogleFonts.inter(
                              fontSize: 10,
                              color: const Color(0xFF999999),
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ),
                borderData: FlBorderData(show: false),
                minX: 0,
                maxX: (points.length - 1).toDouble(),
                minY: minY,
                maxY: maxY,
                lineTouchData: LineTouchData(
                  touchTooltipData: LineTouchTooltipData(
                    getTooltipItems: (touchedSpots) {
                      return touchedSpots.map((spot) {
                        final idx = spot.x.toInt();
                        final dt = idx >= 0 && idx < points.length
                            ? points[idx].time.toLocal()
                            : DateTime.now();
                        return LineTooltipItem(
                          '${spot.y.toStringAsFixed(1)}$unit\n${DateFormat('HH:mm dd/MM').format(dt)}',
                          GoogleFonts.inter(
                            fontSize: 12,
                            color: Colors.white,
                            fontWeight: FontWeight.w600,
                          ),
                        );
                      }).toList();
                    },
                  ),
                ),
                lineBarsData: [
                  LineChartBarData(
                    spots: points
                        .asMap()
                        .entries
                        .map((e) => FlSpot(e.key.toDouble(), e.value.value))
                        .toList(),
                    isCurved: true,
                    preventCurveOverShooting: true,
                    color: lineColor,
                    barWidth: 2.5,
                    dotData: FlDotData(
                      show: points.length <= 24,
                      getDotPainter: (spot, percent, barData, index) =>
                          FlDotCirclePainter(
                        radius: 3,
                        color: lineColor,
                        strokeWidth: 0,
                      ),
                    ),
                    belowBarData: BarAreaData(
                      show: true,
                      color: lineColor.withOpacity(0.1),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHistoricalSummaryCard() {
    final summary = _historicalData!.summary;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Summary',
            style: GoogleFonts.inter(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: const Color(0xFF2E7D32),
            ),
          ),
          const SizedBox(height: 12),

          // Temperature row
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildSummaryItem(
                  'Avg Temp', '${summary.avgTemperature.toStringAsFixed(1)}°C'),
              _buildSummaryItem(
                  'Max Temp', '${summary.maxTemperature.toStringAsFixed(1)}°C'),
              _buildSummaryItem(
                  'Min Temp', '${summary.minTemperature.toStringAsFixed(1)}°C'),
            ],
          ),
          const SizedBox(height: 12),

          // Other stats
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildSummaryItem(
                  'Avg Humidity', '${summary.avgHumidity.toStringAsFixed(1)}%'),
              _buildSummaryItem(
                  'Total Rain', '${summary.totalRain.toStringAsFixed(1)} mm'),
              _buildSummaryItem(
                  'Readings', '${_historicalData!.readingsCount}'),
            ],
          ),

          if (summary.dominantCondition != null) ...[
            const SizedBox(height: 16),
            const Divider(),
            const SizedBox(height: 8),
            Row(
              children: [
                Icon(
                  _getWeatherIcon(summary.dominantCondition),
                  color: _getWeatherColor(summary.dominantCondition),
                  size: 20,
                ),
                const SizedBox(width: 8),
                Text(
                  'Dominant: ${summary.dominantCondition}',
                  style: GoogleFonts.inter(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                    color: const Color(0xFF333333),
                  ),
                ),
              ],
            ),
          ],

          if (summary.conditionBreakdown.isNotEmpty) ...[
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: summary.conditionBreakdown.entries.map((e) {
                return Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: _getWeatherColor(e.key).withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    '${e.key}: ${e.value}',
                    style: GoogleFonts.inter(
                      fontSize: 12,
                      fontWeight: FontWeight.w500,
                      color: _getWeatherColor(e.key),
                    ),
                  ),
                );
              }).toList(),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildSummaryItem(String label, String value) {
    return Column(
      children: [
        Text(
          value,
          style: GoogleFonts.inter(
            fontSize: 16,
            fontWeight: FontWeight.w700,
            color: const Color(0xFF333333),
          ),
        ),
        const SizedBox(height: 2),
        Text(
          label,
          style: GoogleFonts.inter(
            fontSize: 11,
            color: const Color(0xFF999999),
          ),
        ),
      ],
    );
  }

  // ============================
  // TAB 3: Forecast (Open-Meteo)
  // ============================

  Widget _buildForecastTab() {
    if (_forecastLoading) {
      return const Center(
        child: CircularProgressIndicator(
          valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF53AD64)),
        ),
      );
    }

    if (_forecastError != null) {
      return _buildErrorWidget(_forecastError!, _loadForecastData);
    }

    final data = _forecastData!;

    return RefreshIndicator(
      color: const Color(0xFF53AD64),
      onRefresh: _loadForecastData,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Source label
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: const Color(0xFF53AD64).withOpacity(0.08),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Row(
                children: [
                  const Icon(Icons.public, color: Color(0xFF2E7D32), size: 18),
                  const SizedBox(width: 8),
                  Text(
                    'Forecast (Open-Meteo)',
                    style: GoogleFonts.inter(
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                      color: const Color(0xFF2E7D32),
                    ),
                  ),
                  const Spacer(),
                  if (_user != null)
                    Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.location_on,
                            color: Color(0xFF53AD64), size: 14),
                        const SizedBox(width: 4),
                        Text(
                          _user!.farmLocationName,
                          style: GoogleFonts.inter(
                            fontSize: 12,
                            color: const Color(0xFF666666),
                          ),
                        ),
                      ],
                    ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Current conditions brief
            _buildForecastCurrentCard(data.current),
            const SizedBox(height: 16),

            // 24-hour horizontal scroll
            _buildHourlyForecast(data.forecast),
            const SizedBox(height: 16),

            // Weather alerts
            _buildForecastAlertsSection(data.alerts),
            const SizedBox(height: 16),

            // Agricultural recommendations
            _buildForecastRecommendationsSection(data.recommendations),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  Widget _buildForecastCurrentCard(CurrentWeather current) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Icon(current.iconData, size: 48, color: current.iconColor),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${current.temperature.toStringAsFixed(1)}°C',
                  style: GoogleFonts.inter(
                    fontSize: 28,
                    fontWeight: FontWeight.w700,
                    color: const Color(0xFF333333),
                  ),
                ),
                Text(
                  current.weatherMain,
                  style: GoogleFonts.inter(
                    fontSize: 14,
                    color: const Color(0xFF666666),
                  ),
                ),
              ],
            ),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.water_drop,
                      size: 14, color: Color(0xFF42A5F5)),
                  const SizedBox(width: 4),
                  Text(
                    '${current.humidity}%',
                    style: GoogleFonts.inter(
                      fontSize: 13,
                      color: const Color(0xFF666666),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 4),
              Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.air, size: 14, color: Color(0xFF78909C)),
                  const SizedBox(width: 4),
                  Text(
                    '${current.windSpeed.toStringAsFixed(1)} m/s',
                    style: GoogleFonts.inter(
                      fontSize: 13,
                      color: const Color(0xFF666666),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildHourlyForecast(List<ForecastItem> forecast) {
    final hourlyForecast = forecast.take(12).toList();

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '24-Hour Forecast',
            style: GoogleFonts.inter(
              fontSize: 16,
              fontWeight: FontWeight.w600,
              color: const Color(0xFF2E7D32),
            ),
          ),
          const SizedBox(height: 16),
          if (hourlyForecast.isEmpty)
            Center(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Text(
                  'No forecast data available',
                  style: GoogleFonts.inter(color: Colors.grey),
                ),
              ),
            )
          else
            SizedBox(
              height: 120,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: hourlyForecast.length,
                itemBuilder: (context, index) {
                  final item = hourlyForecast[index];
                  return Container(
                    width: 70,
                    margin: const EdgeInsets.only(right: 8),
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF5F5F5),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          _formatHour(item.forecastTime),
                          style: GoogleFonts.inter(
                            fontSize: 12,
                            color: Colors.grey,
                          ),
                        ),
                        const SizedBox(height: 4),
                        Icon(item.iconData, size: 28, color: item.iconColor),
                        const SizedBox(height: 4),
                        Text(
                          '${item.temperature.toStringAsFixed(0)}°',
                          style: GoogleFonts.inter(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        Text(
                          '${(item.rainProbability * 100).toStringAsFixed(0)}%',
                          style: GoogleFonts.inter(
                            fontSize: 11,
                            color: Colors.blue,
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildForecastAlertsSection(List<WeatherAlert> alerts) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Weather Alerts',
          style: GoogleFonts.inter(
            fontSize: 18,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 12),
        if (alerts.isEmpty)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Row(
              children: [
                const Icon(Icons.check_circle,
                    color: Color(0xFF53AD64), size: 32),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'No weather alerts',
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      color: Colors.grey[600],
                    ),
                  ),
                ),
              ],
            ),
          )
        else
          ...alerts.map((alert) => _buildAlertCard(alert)),
      ],
    );
  }

  Widget _buildAlertCard(WeatherAlert alert) {
    Color severityColor;
    switch (alert.severity.toLowerCase()) {
      case 'high':
        severityColor = Colors.red;
        break;
      case 'medium':
        severityColor = Colors.orange;
        break;
      default:
        severityColor = Colors.blue;
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: severityColor.withOpacity(0.3)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(alert.icon, style: const TextStyle(fontSize: 24)),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  alert.title,
                  style: GoogleFonts.inter(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: severityColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  alert.severity.toUpperCase(),
                  style: GoogleFonts.inter(
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                    color: severityColor,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            alert.description,
            style: GoogleFonts.inter(
              fontSize: 13,
              color: Colors.grey[700],
            ),
          ),
          if (alert.recommendations.isNotEmpty) ...[
            const SizedBox(height: 12),
            Text(
              'Recommendations:',
              style: GoogleFonts.inter(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 4),
            ...alert.recommendations.take(3).map((rec) => Padding(
                  padding: const EdgeInsets.only(left: 8, top: 2),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('• ',
                          style: TextStyle(color: Colors.grey[600])),
                      Expanded(
                        child: Text(
                          rec,
                          style: GoogleFonts.inter(
                            fontSize: 12,
                            color: Colors.grey[600],
                          ),
                        ),
                      ),
                    ],
                  ),
                )),
          ],
        ],
      ),
    );
  }

  Widget _buildForecastRecommendationsSection(
      List<WeatherRecommendation> recommendations) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Agricultural Recommendations',
          style: GoogleFonts.inter(
            fontSize: 18,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 12),
        if (recommendations.isEmpty)
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(12),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Row(
              children: [
                const Icon(Icons.thumb_up,
                    color: Color(0xFF53AD64), size: 32),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'No recommendations at this time',
                    style: GoogleFonts.inter(
                      fontSize: 14,
                      color: Colors.grey[600],
                    ),
                  ),
                ),
              ],
            ),
          )
        else
          ...recommendations
              .map((rec) => _buildRecommendationCard(rec)),
      ],
    );
  }

  Widget _buildRecommendationCard(WeatherRecommendation rec) {
    Color priorityColor;
    switch (rec.priority.toLowerCase()) {
      case 'high':
        priorityColor = Colors.red;
        break;
      case 'medium':
        priorityColor = Colors.orange;
        break;
      default:
        priorityColor = Colors.green;
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(rec.icon, style: const TextStyle(fontSize: 24)),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  rec.title,
                  style: GoogleFonts.inter(
                    fontSize: 14,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: priorityColor.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  rec.priority.toUpperCase(),
                  style: GoogleFonts.inter(
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                    color: priorityColor,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            rec.description,
            style: GoogleFonts.inter(
              fontSize: 13,
              color: Colors.grey[700],
            ),
          ),
          const SizedBox(height: 4),
          Text(
            rec.reason,
            style: GoogleFonts.inter(
              fontSize: 12,
              color: Colors.grey,
              fontStyle: FontStyle.italic,
            ),
          ),
          if (rec.actions.isNotEmpty) ...[
            const SizedBox(height: 12),
            ...rec.actions.take(3).map((action) => Padding(
                  padding: const EdgeInsets.only(left: 8, top: 2),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.check_circle,
                          size: 14, color: Color(0xFF53AD64)),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          action,
                          style: GoogleFonts.inter(
                            fontSize: 12,
                            color: Colors.grey[600],
                          ),
                        ),
                      ),
                    ],
                  ),
                )),
          ],
        ],
      ),
    );
  }

  // ============================
  // Shared helpers
  // ============================

  Widget _buildErrorWidget(String message, VoidCallback onRetry) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.cloud_off, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            Text(
              'Failed to load data',
              style: GoogleFonts.inter(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              message,
              style: GoogleFonts.inter(color: Colors.grey),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: onRetry,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF4BAE4F),
                foregroundColor: Colors.white,
              ),
              child: const Text('Retry'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInlineError(String message, VoidCallback onRetry) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        children: [
          const Icon(Icons.error_outline, size: 48, color: Colors.orange),
          const SizedBox(height: 12),
          Text(
            message,
            style: GoogleFonts.inter(
              fontSize: 14,
              color: const Color(0xFF666666),
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: onRetry,
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF53AD64),
              foregroundColor: Colors.white,
            ),
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  }

  String _formatHour(DateTime time) {
    final localTime = time.toLocal();
    final hour = localTime.hour;
    if (hour == 0) return '12 AM';
    if (hour == 12) return '12 PM';
    if (hour < 12) return '$hour AM';
    return '${hour - 12} PM';
  }
}

/// Internal helper for chart data points.
class _ChartPoint {
  final DateTime time;
  final double value;
  _ChartPoint(this.time, this.value);
}
