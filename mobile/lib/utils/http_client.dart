import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:http/io_client.dart';

/// Returns an HTTP client that trusts all certificates in debug mode.
/// This is needed because Cloudflare's SSL certificate chain is not
/// trusted by the Android emulator's Dart HTTP client.
///
/// In release mode, uses the default client with strict certificate validation.
http.Client createHttpClient() {
  if (kDebugMode) {
    final ioClient = HttpClient()
      ..badCertificateCallback =
          (X509Certificate cert, String host, int port) => true;
    return IOClient(ioClient);
  }
  return http.Client();
}

/// Singleton HTTP client instance for reuse across services.
final http.Client appHttpClient = createHttpClient();
