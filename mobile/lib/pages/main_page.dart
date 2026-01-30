import 'package:flutter/material.dart';
import 'package:fyp_prototype/widgets/custom_bottom_nav_bar.dart';
import 'package:fyp_prototype/models/home_page_data.dart';
import 'package:fyp_prototype/pages/home_page.dart';
import 'package:fyp_prototype/pages/pests_page.dart';
import 'package:fyp_prototype/pages/settings_page.dart';
import 'package:fyp_prototype/pages/weather_page.dart';
import 'package:fyp_prototype/services/dashboard_service.dart';
import 'package:fyp_prototype/utils/token_storage.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _selectedIndex = 0;
  bool _isLoading = true;
  String? _errorMessage;
  HomePageData? _homePageData;

  @override
  void initState() {
    super.initState();
    _loadDashboardData();
  }

  Future<void> _loadDashboardData() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final token = await TokenStorage.getToken();
      if (token == null) {
        // No token, redirect to login
        if (mounted) {
          Navigator.pushReplacementNamed(context, '/login');
        }
        return;
      }

      final dashboardData = await DashboardService.getDashboard(token);

      // Debug: Print weather data to console
      print('Dashboard weather data: ${dashboardData['weather']}');

      final homePageData = HomePageData.fromDashboardResponse(dashboardData);

      if (mounted) {
        setState(() {
          _homePageData = homePageData;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        final errorMsg = e.toString().replaceFirst('Exception: ', '');

        // Check if session expired
        if (errorMsg.contains('Session expired') || errorMsg.contains('401')) {
          await TokenStorage.deleteToken();
          Navigator.pushReplacementNamed(context, '/login');
          return;
        }

        setState(() {
          _errorMessage = errorMsg;
          _isLoading = false;
        });
      }
    }
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void _onChatbotTap() {
    Navigator.pushNamed(context, '/chatbot');
  }

  Widget _buildLoadingScreen() {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF53AD64)),
            ),
            SizedBox(height: 16),
            Text(
              'Loading dashboard...',
              style: TextStyle(
                color: Color(0xFF828282),
                fontSize: 14,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildErrorScreen() {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.error_outline,
                size: 64,
                color: Colors.red.shade300,
              ),
              SizedBox(height: 16),
              Text(
                'Failed to load dashboard',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF2E7D32),
                ),
              ),
              SizedBox(height: 8),
              Text(
                _errorMessage ?? 'Unknown error',
                style: TextStyle(
                  color: Color(0xFF828282),
                  fontSize: 14,
                ),
                textAlign: TextAlign.center,
              ),
              SizedBox(height: 24),
              ElevatedButton(
                onPressed: _loadDashboardData,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Color(0xFF4BAE4F),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                child: Text('Retry'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return _buildLoadingScreen();
    }

    if (_errorMessage != null) {
      return _buildErrorScreen();
    }

    // Build pages list with loaded data
    final routes = [
      HomePage(homePageData: _homePageData!),
      WeatherPage(),
      PestsPage(),
      SettingsPage(),
    ];

    return Scaffold(
      body: IndexedStack(index: _selectedIndex, children: routes),
      bottomNavigationBar: CustomBottomNavBar(
        selectedIndex: _selectedIndex,
        onItemTapped: _onItemTapped,
        onChatbotTap: _onChatbotTap,
      ),
    );
  }
}
