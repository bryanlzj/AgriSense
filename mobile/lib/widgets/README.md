# Widgets

Reusable UI components for the AgriSense mobile app.

## TODO: Create Reusable Widgets

### Common Widgets to Create:

1. **CustomButton** - Styled button with loading state
2. **CustomTextField** - Styled text input field
3. **LoadingIndicator** - Loading spinner
4. **ErrorMessage** - Error display widget
5. **SuccessMessage** - Success display widget
6. **SensorCard** - Card to display sensor reading
7. **AlertCard** - Card to display alert
8. **PestCard** - Card to display pest detection
9. **WeatherCard** - Card to display weather info
10. **StatCard** - Card to display statistics
11. **EmptyState** - Empty state placeholder
12. **BottomNavBar** - Bottom navigation bar

## Example Widget Structure:

```dart
import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final bool isLoading;
  
  const CustomButton({
    super.key,
    required this.text,
    required this.onPressed,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      child: isLoading
          ? const CircularProgressIndicator()
          : Text(text),
    );
  }
}
```
