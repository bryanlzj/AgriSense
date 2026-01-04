import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// TODO: Import screens when created
// import 'screens/auth/login_screen.dart';
// import 'screens/dashboard/dashboard_screen.dart';

// TODO: Import providers when created
// import 'providers/auth_provider.dart';

void main() {
  runApp(const AgriSenseApp());
}

class AgriSenseApp extends StatelessWidget {
  const AgriSenseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        // TODO: Add providers here
        // ChangeNotifierProvider(create: (_) => AuthProvider()),
        // ChangeNotifierProvider(create: (_) => SensorProvider()),
        // ChangeNotifierProvider(create: (_) => PestProvider()),
        // ChangeNotifierProvider(create: (_) => WeatherProvider()),
        // ChangeNotifierProvider(create: (_) => AlertProvider()),
      ],
      child: MaterialApp(
        title: 'AgriSense',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.green,
            brightness: Brightness.light,
          ),
          useMaterial3: true,
          appBarTheme: const AppBarTheme(
            centerTitle: true,
            elevation: 0,
          ),
        ),
        // TODO: Set initial route based on authentication status
        home: const PlaceholderScreen(),
        // home: const LoginScreen(), // When LoginScreen is created
        
        // TODO: Add routes when screens are created
        // routes: {
        //   '/login': (context) => const LoginScreen(),
        //   '/register': (context) => const RegisterScreen(),
        //   '/dashboard': (context) => const DashboardScreen(),
        //   '/sensors': (context) => const SensorListScreen(),
        //   '/pest-detection': (context) => const PestDetectionScreen(),
        //   '/weather': (context) => const WeatherScreen(),
        //   '/alerts': (context) => const AlertsScreen(),
        // },
      ),
    );
  }
}

/// Placeholder screen - Replace with LoginScreen when ready
class PlaceholderScreen extends StatelessWidget {
  const PlaceholderScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AgriSense'),
        backgroundColor: Colors.green,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.agriculture,
              size: 100,
              color: Colors.green[700],
            ),
            const SizedBox(height: 24),
            Text(
              'AgriSense Mobile',
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Colors.green[700],
                  ),
            ),
            const SizedBox(height: 16),
            Text(
              'Agricultural Intelligence System',
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: Colors.grey[600],
                  ),
            ),
            const SizedBox(height: 48),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 32.0),
              child: Text(
                'This is a placeholder screen.\n\n'
                'Member 3 will implement:\n'
                '• Authentication screens\n'
                '• Dashboard\n'
                '• Sensor data management\n'
                '• Pest detection\n'
                '• Weather forecast\n'
                '• Alert notifications',
                textAlign: TextAlign.center,
                style: TextStyle(height: 1.5),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
