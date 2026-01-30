import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class PestsPage extends StatefulWidget {
  const PestsPage({super.key});

  @override
  State<PestsPage> createState() => _PestsPageState();
}

class _PestsPageState extends State<PestsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 80,
        foregroundColor: Colors.white,
        backgroundColor: const Color(0xFF53AD64),
        title: Padding(
          padding: const EdgeInsets.only(left: 20.0, ),
          child: Text(
            'Pests Alerts',
            style: GoogleFonts.scheherazadeNew(fontSize: 28),
          ),
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 20.0),
            child: IconButton(onPressed: (){}, icon: Icon(Icons.add, size: 30,)),
          )
        ],
      ),
      backgroundColor: Colors.white,
      body: Column(
        children: [
          Row(
            children: [
              FilterChip(label: Text('All'), onSelected: (bool selected){})
            ],
          ),
        ],
      ),
    );
  }
}
