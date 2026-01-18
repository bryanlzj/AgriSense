import 'package:flutter/material.dart';
import 'package:fyp_prototype/utils/greetings.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:fyp_prototype/models/home_page_data.dart';

class HomePage extends StatefulWidget {
  final HomePageData homePageData;

  const HomePage({super.key, 
  required this.homePageData
  });

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Container(
            height: 300,
            width: double.infinity,
            decoration: BoxDecoration(
              color: Color(0xFF53AD64),
              borderRadius: BorderRadius.only(
                bottomLeft: Radius.circular(20),
                bottomRight: Radius.circular(20),
              ),
            ),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 30.0, vertical: 30),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "${getGreeting()}, ${widget.homePageData.userName}!",
                    style: GoogleFonts.scheherazadeNew(fontSize: 20, fontWeight: FontWeight.w500, color: Colors.white),
                  ),
                  SizedBox(height: 20,),
                  Container(
                    height: 30,
                    width: 225,
                    decoration: BoxDecoration(
                      color: Color(0xFF84CA84),
                      borderRadius: BorderRadiusGeometry.circular(64),
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
}

//0xFFEEF5F1