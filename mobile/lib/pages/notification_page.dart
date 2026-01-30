import 'package:flutter/material.dart';
import 'package:fyp_prototype/widgets/custom_app_bar.dart';
import 'package:fyp_prototype/widgets/notification_option_card.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:shared_preferences/shared_preferences.dart';

class NotificationPage extends StatefulWidget {
  const NotificationPage({super.key});

  @override
  State<NotificationPage> createState() => _NotificationPageState();
}

class _NotificationPageState extends State<NotificationPage> {
  //general
  bool pushNotificationsEnabled = true;
  //weather
  bool rainfallWarnings = true;
  bool droughtWarnings = false;
  //pest
  bool pestDetection = true;

  @override
  void initState(){
    super.initState();
    _loadSwitchValues();
  }

  Future<void> _loadSwitchValues() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      pushNotificationsEnabled = prefs.getBool('pushNotificationsEnabled') ?? true;
      rainfallWarnings = prefs.getBool('rainfallWarnings') ?? true;
      droughtWarnings = prefs.getBool('droughtWarnings') ?? false;
      pestDetection = prefs.getBool('pestDetection') ?? true;
    });
  }

    Future<void> _saveSwitchValue(String key, bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(key, value);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        title: 'Notification Settings',
        subtitle: 'Manage your alerts and reminders',
      ),
      backgroundColor: Colors.white,
      body: Padding(
        padding: EdgeInsets.symmetric(vertical: 20, horizontal: 20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'General',
              style: GoogleFonts.scheherazadeNew(
                fontSize: 20,
                fontWeight: FontWeight.w500,
              ),
            ),
            SizedBox(height: 15,),
            NotificationOptionCard(
              imagePath: 'assets/images/push_notification.png',
              title: 'Push Notifications',
              subtitle: 'Enable app notifications',
              value: pushNotificationsEnabled,
              onChanged: (newValue) {
                setState(() {
                  pushNotificationsEnabled = newValue;
                  //backend api call
                });
                _saveSwitchValue('pushNotificationsEnabled', newValue);
              },
            ),
            SizedBox(height: 20,),
            Text(
              'Weather Alerts',
              style: GoogleFonts.scheherazadeNew(
                fontSize: 20,
                fontWeight: FontWeight.w500,
              ),
            ),
            SizedBox(height: 15,),
            NotificationOptionCard(
              imagePath: 'assets/images/rainfall.png',
              title: 'Rainfall Warnings',
              subtitle: 'Get notified before rainfall',
              value: rainfallWarnings,
              onChanged: (newValue) {
                setState(() {
                  rainfallWarnings = newValue;
                  //backend api call
                });
                _saveSwitchValue('rainfallWarnings', newValue);
              },
            ),
            SizedBox(height: 15,),
            NotificationOptionCard(
              imagePath: 'assets/images/drought.png',
              title: 'Drought Warnings',
              subtitle: 'Get notified before dry spells',
              value: droughtWarnings,
              onChanged: (newValue) {
                setState(() {
                  droughtWarnings = newValue;
                  //backend api call
                });
                _saveSwitchValue('droughtWarnings', newValue);
              },
            ),
            SizedBox(height: 20,),
            Text(
              'Pests Alerts',
              style: GoogleFonts.scheherazadeNew(
                fontSize: 20,
                fontWeight: FontWeight.w500,
              ),
            ),
            SizedBox(height: 15,),
            NotificationOptionCard(
              imagePath: 'assets/images/pest_icon.png',
              title: 'Pest Detection',
              subtitle: 'Instant alerts when pests are detected',
              value: pestDetection,
              onChanged: (newValue) {
                setState(() {
                  pestDetection = newValue;
                  //backend api call
                });
                _saveSwitchValue('pestDetection', newValue);
              },
            ),
          ],
        ),
      ),
    );
  }
}
