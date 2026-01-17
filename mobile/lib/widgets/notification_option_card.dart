import 'package:flutter/material.dart';

class NotificationOptionCard extends StatelessWidget {
  final String imagePath;
  final String title;
  final String subtitle;
  final bool value;
  final ValueChanged<bool> onChanged;

  const NotificationOptionCard({
    super.key,
    required this.imagePath,
    required this.title,
    required this.subtitle,
    required this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 80,
      decoration: BoxDecoration(
        border: Border.all(
          color: Colors.black.withValues(alpha: 0.1),
          width: 1.5,
        ),
        borderRadius: BorderRadius.circular(15),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 15.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Image.asset(imagePath, width: 30, height: 30),
                const SizedBox(width: 15),
                Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      subtitle,
                      style: const TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w500,
                        color: Color(0xFF676767),
                      ),
                    ),
                  ],
                ),
              ],
            ),
            Transform.scale(
              scale: 0.8,
              child: Switch(
                value: value,
                onChanged: onChanged,
                activeColor: Colors.white, // dot color
                activeTrackColor: const Color(0xFF53AD64), // background when ON
                inactiveThumbColor: Colors.white, // dot when OFF
                inactiveTrackColor: const Color(
                  0xFFAFB1B6,
                ), // background when OFF
                trackOutlineWidth: WidgetStateProperty.resolveWith<double?>((
                  Set<WidgetState> states,
                ) {
                  if (states.contains(WidgetState.disabled)) {
                    return 1.0;
                  }
                  return 1.0; // Use the default width.
                }),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
