import 'package:flutter/material.dart';
import 'package:fyp_prototype/widgets/settings_option_card.dart';
import 'package:google_fonts/google_fonts.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        children: [
          Container(
            height: 275,
            width: double.infinity,
            decoration: BoxDecoration(color: Color(0xFF53AD64)),
            child: Padding(
              padding: EdgeInsets.only(top: 50.0,bottom: 20),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Image.asset('assets/images/Avatar.png'),
                  //SizedBox(height: 10),
                  Text(
                    'Ahmad Rahman',
                    style: GoogleFonts.scheherazadeNew(
                      color: Colors.white,
                      fontSize: 28,
                    ),
                  ),
                  Text('UserID: 012345', style: TextStyle(color: Colors.white, fontSize: 12)),
                  SizedBox(height: 10,),
                  SizedBox(
                    height: 30,
                    width: 250,
                    child: ElevatedButton(
                      onPressed: () {
                        
                      },
                      style: ElevatedButton.styleFrom(
                        elevation: 0,
                        backgroundColor: Color(0xFF6FCB7B),
                        foregroundColor: Color.fromARGB(255, 1, 119, 30),
                        //side: BorderSide(color: Colors.white),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadiusGeometry.circular(10),
                        ),
                      ),
                      child: Text(
                        'Edit Profile',
                        style: TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          Expanded(
            child: Padding(
              padding: EdgeInsets.only(top: 25.0, left: 25, right: 25),
              child: Column(
                //mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  SettingsOptionCard(
                    imagePath: 'assets/images/farm_icon.png',
                    title: 'Farm Management',
                    subtitle: 'Setup sectors, crops, and locations',
                    onTap: () {
                      Navigator.pushNamed(context, '/farm');
                    },
                  ),
                  SizedBox(height: 20,),
                  SettingsOptionCard(
                    imagePath: 'assets/images/notification_icon.webp',
                    title: 'Notification Settings',
                    subtitle: 'Manage alerts and reminders',
                    onTap: () {
                      Navigator.pushNamed(context, '/notification');
                    },
                  ),
                  SizedBox(height: 20,),
                  SettingsOptionCard(
                    imagePath: 'assets/images/import.png',
                    title: 'Import Dataset',
                    subtitle: 'Upload weather or pest-related data',
                    onTap: () {
                      Navigator.pushNamed(context, '/import');
                    },
                  ),
                  SizedBox(height: 20,),
                  SettingsOptionCard(
                    imagePath: 'assets/images/help_support.png',
                    title: 'Help & Support',
                    subtitle: 'FAQs and contact support',
                    onTap: () {
                      Navigator.pushNamed(context, '/help');
                    },
                  ),
                  SizedBox(height: 20,),
                  SettingsOptionCard(
                    imagePath: 'assets/images/farm_icon.png',
                    title: 'About AgriSense',
                    subtitle: 'Version 1.0.0',
                    onTap: () {
                      Navigator.pushNamed(context, '/about');
                    },
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
