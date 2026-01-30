import 'package:flutter/material.dart';
import 'package:fyp_prototype/pages/about_agrisense_page.dart';
import 'package:fyp_prototype/pages/chatbot_page.dart';
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
  WidgetsFlutterBinding.ensureInitialized(); // ✅ needed before async stuff
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Route map - MainPage now fetches its own data
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
      '/about': (context) => AboutAgrisensePage()
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
      initialRoute: '/login',

      // keep your routes map
      routes: routes,

      // override only chatbot with custom animation
      onGenerateRoute: (settings) {
        if (settings.name == '/chatbot') {
          return PageRouteBuilder(
            pageBuilder: (context, animation, secondaryAnimation) =>
                ChatbotPage(),
            transitionsBuilder: (context, animation, secondaryAnimation, child) {
              // slide from bottom to top
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

        // default: use your normal route map
        final builder = routes[settings.name];
        if (builder != null) {
          return MaterialPageRoute(
            builder: builder,
            settings: settings,
          );
        }

        return null; // if unknown route
      },
    );
  }
}
