import 'package:flutter/material.dart';
import 'package:fyp_prototype/widgets/custom_bottom_nav_bar.dart';
//import 'package:google_fonts/google_fonts.dart';
import 'package:fyp_prototype/data/mock_home_data.dart';
import 'package:fyp_prototype/models/home_page_data.dart';
import 'package:fyp_prototype/pages/home_page.dart';
import 'package:fyp_prototype/pages/pests_page.dart';
import 'package:fyp_prototype/pages/settings_page.dart';
import 'package:fyp_prototype/pages/weather_page.dart';

class MainPage extends StatefulWidget {
  final HomePageData homePageData;

  const MainPage({super.key, required this.homePageData});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _selectedIndex = 0;
  //int _previousIndex = 0;

  // pages list
  final List<Widget> _routes = [
    HomePage(homePageData: mockData),
    WeatherPage(),
    PestsPage(),
    SettingsPage(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      //_previousIndex = _selectedIndex;
      _selectedIndex = index;
    });
  }

  void _onChatbotTap() {
    Navigator.pushNamed(context, '/chatbot');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(index: _selectedIndex, children: _routes),
      bottomNavigationBar: CustomBottomNavBar(
        selectedIndex: _selectedIndex,
        onItemTapped: _onItemTapped,
        onChatbotTap: _onChatbotTap,
      ),
    );
  }
}
