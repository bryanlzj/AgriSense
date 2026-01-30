import 'package:flutter/material.dart';

class AboutAgrisensePage extends StatefulWidget {
  const AboutAgrisensePage({super.key});

  @override
  State<AboutAgrisensePage> createState() => _AboutAgrisensePageState();
}

class _AboutAgrisensePageState extends State<AboutAgrisensePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'About AgriSense',
        ),
      ),
    );
  }
}