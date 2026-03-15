import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/farm_sector.dart';

class FarmSectorCard extends StatelessWidget {
  final Sector sector;
  final VoidCallback onEdit;

  const FarmSectorCard({
    super.key,
    required this.sector,
    required this.onEdit,
  });

  Widget buildInfoRow(String iconPath, String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Image.asset(iconPath, height: 20, width: 20),
        const SizedBox(width: 10),
        Text.rich(
          TextSpan(
            text: '$label: ',
            style: GoogleFonts.inter(
              fontSize: 12,
              fontWeight: FontWeight.bold,
              color: const Color(0xFF676767),
            ),
            children: [
              TextSpan(
                text: value,
                style: GoogleFonts.inter(fontWeight: FontWeight.normal),
              ),
            ],
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      margin: const EdgeInsets.only(bottom: 15),
      decoration: BoxDecoration(
        border: Border.all(
          color: Colors.black.withValues(alpha: 0.1),
          width: 1.5,
        ),
        borderRadius: BorderRadius.circular(15),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 15),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  sector.name,
                  style: GoogleFonts.inter(fontWeight: FontWeight.bold),
                ),
                Material(
                  color: Colors.transparent,
                  child: InkWell(
                    onTap: onEdit,
                    child: Image.asset(
                      'assets/images/edit_icon.png',
                      height: 20,
                      width: 20,
                    ),
                  ),
                ),
              ],
            ),
            buildInfoRow('assets/images/pin.png', 'Location', sector.location),
            buildInfoRow('assets/images/area.png', 'Area', sector.areaDisplay),
            buildInfoRow('assets/images/crop.png', 'Crop', sector.crop),
            buildInfoRow('assets/images/calender.png', 'Planted', sector.planted),
          ],
        ),
      ),
    );
  }
}
