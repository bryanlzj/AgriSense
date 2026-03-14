import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:fyp_prototype/providers/auth_provider.dart';
import 'package:fyp_prototype/pages/about_agrisense_page.dart';
import 'package:fyp_prototype/pages/alerts_page.dart';
import 'package:fyp_prototype/pages/chatbot_page.dart';
import 'package:fyp_prototype/pages/edit_profile_page.dart';
import 'package:fyp_prototype/pages/farm_management_page.dart';
import 'package:fyp_prototype/pages/forgot_password_page.dart';
import 'package:fyp_prototype/pages/help_support_page.dart';
import 'package:fyp_prototype/pages/import_dataset_page.dart';
import 'package:fyp_prototype/pages/login_page.dart';
import 'package:fyp_prototype/pages/main_page.dart';
import 'package:fyp_prototype/pages/notification_page.dart';
import 'package:fyp_prototype/pages/otp_page.dart';
import 'package:fyp_prototype/pages/pests_page.dart';
import 'package:fyp_prototype/pages/reset_password_page.dart';
import 'package:fyp_prototype/pages/settings_page.dart';
import 'package:fyp_prototype/pages/sign_up_page.dart';
import 'package:fyp_prototype/pages/success_page.dart';
import 'package:fyp_prototype/pages/weather_page.dart';
import 'package:google_fonts/google_fonts.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
      ],
      child: const AgriSenseApp(),
    );
  }
}

class AgriSenseApp extends StatefulWidget {
  const AgriSenseApp({super.key});

  @override
  State<AgriSenseApp> createState() => _AgriSenseAppState();
}

class _AgriSenseAppState extends State<AgriSenseApp> {
  @override
  void initState() {
    super.initState();
    // Check auth status after first frame
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AuthProvider>().checkAuthStatus();
    });
  }

  @override
  Widget build(BuildContext context) {
    // Route map
    final routes = {
      '/signUp': (context) => SignUpPage(),
      '/login': (context) => LoginPage(),
      '/forgotPassword': (context) => ForgotPasswordPage(),
      '/otp': (context) => OtpPage(),
      '/resetPassword': (context) => ResetPasswordPage(),
      '/success': (context) => SuccessPage(),
      '/main': (context) => MainPage(),
      '/weather': (context) => WeatherPage(),
      '/pests': (context) => PestsPage(),
      '/settings': (context) => SettingsPage(),
      '/chatbot': (context) => ChatbotPage(),
      '/farm': (context) => FarmManagementPage(),
      '/notification': (context) => NotificationPage(),
      '/import': (context) => ImportDatasetPage(),
      '/help': (context) => HelpSupportPage(),
      '/about': (context) => AboutAgrisensePage(),
      '/editProfile': (context) => EditProfilePage(),
      '/alerts': (context) => AlertsPage(),
    };

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        textTheme: GoogleFonts.interTextTheme(),
        textSelectionTheme: const TextSelectionThemeData(
          cursorColor: Color(0xFF53AD64),
          selectionColor: Color(0x7060AC75),
          selectionHandleColor: Color(0xFF4BAE4F),
        ),
      ),
      // Use AuthWrapper as home to handle auth-based routing
      home: const AuthWrapper(),
      routes: routes,
      // Custom animation for chatbot
      onGenerateRoute: (settings) {
        if (settings.name == '/chatbot') {
          return PageRouteBuilder(
            pageBuilder: (context, animation, secondaryAnimation) =>
                ChatbotPage(),
            transitionsBuilder: (context, animation, secondaryAnimation, child) {
              const begin = Offset(0.0, 1.0);
              const end = Offset.zero;
              const curve = Curves.easeInOut;

              final tween =
                  Tween(begin: begin, end: end).chain(CurveTween(curve: curve));
              final offsetAnimation = animation.drive(tween);

              return SlideTransition(
                position: offsetAnimation,
                child: child,
              );
            },
          );
        }

        // Default: use normal route map
        final builder = routes[settings.name];
        if (builder != null) {
          return MaterialPageRoute(
            builder: builder,
            settings: settings,
          );
        }

        return null;
      },
    );
  }
}

/// Wrapper that routes based on authentication state.
class AuthWrapper extends StatelessWidget {
  const AuthWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<AuthProvider>(
      builder: (context, auth, _) {
        // Show loading while checking auth
        if (auth.status == AuthStatus.initial || auth.isLoading) {
          return const SplashScreen();
        }

        // Route based on auth status
        if (auth.isAuthenticated) {
          return const MainPage();
        } else {
          return const LoginPage();
        }
      },
    );
  }
}

/// Simple splash screen shown while checking auth.
class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              'assets/images/logo.png',
              width: 120,
              height: 120,
            ),
            const SizedBox(height: 24),
            const CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF53AD64)),
            ),
          ],
        ),
      ),
    );
  }
}
