import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  final String title;
  final String subtitle;

  const CustomAppBar({
    super.key,
    required this.title,
    required this.subtitle,
  });

  @override
  Size get preferredSize => const Size.fromHeight(80); // match toolbarHeight

  @override
  Widget build(BuildContext context) {
    return AppBar(
      leading: IconButton(
        icon: const Icon(
          CupertinoIcons.left_chevron,
          color: Colors.white,
        ),
        onPressed: () => Navigator.pop(context),
      ),
      toolbarHeight: 80,
      backgroundColor: const Color(0xFF53AD64),
      title: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: GoogleFonts.scheherazadeNew(
              fontSize: 28,
              color: Colors.white,
            ),
          ),
          Text(
            subtitle,
            style: const TextStyle(
              fontSize: 13,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }
}
