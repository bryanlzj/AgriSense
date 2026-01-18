import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class OtpPage extends StatefulWidget {
  const OtpPage({super.key});

  @override
  State<OtpPage> createState() => _OtpPageState();
}

class _OtpPageState extends State<OtpPage> {
  final TextEditingController _otpController = TextEditingController();
  final FocusNode _focusNode = FocusNode();
  final int otpLength = 5;
  String? _errorText;

  @override
  void dispose() {
    _otpController.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  void _submitOtp() {
    String enteredOtp = _otpController.text.trim();

    setState(() {
      if (enteredOtp.length < otpLength) {
        _errorText = "Please enter the full OTP";
      } else {
        _errorText = null; // clear error
        // For now just simulate success
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("OTP Verified: $enteredOtp")));
        Navigator.pushNamedAndRemoveUntil(context, '/resetPassword',ModalRoute.withName('/login  '));
      }
    });

    // ✅ Here, you normally send the OTP to your backend for verification
    // Example:
    // await BackendAPI.verifyOtp(email, enteredOtp);

    // You can then navigate to reset password page
    // Navigator.pushReplacementNamed(context, '/resetPassword');
  }

  @override
  Widget build(BuildContext context) {
    final String email = ModalRoute.of(context)!.settings.arguments as String;

    return Scaffold(
      backgroundColor: Colors.white,
      body: Padding(
        padding: EdgeInsetsGeometry.symmetric(horizontal: 20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SizedBox(height: 40),
            BackButton(
              onPressed: () {
                Navigator.pop(context);
              },
            ),
            SizedBox(height: 30),
            Padding(
              padding: EdgeInsetsGeometry.symmetric(horizontal: 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Check your email',
                    style: GoogleFonts.poppins(
                      fontWeight: FontWeight.w500,
                      fontSize: 20,
                    ),
                  ),
                  SizedBox(height: 10),
                  Text.rich(
                    TextSpan(
                      children: [
                        TextSpan(
                          text: 'We sent a reset link to ',
                          style: TextStyle(color: Color(0xFF989898)),
                        ),
                        TextSpan(
                          text: email,
                          style: TextStyle(color: Colors.black),
                        ),
                        TextSpan(
                          text:
                              '\nEnter the 5 digit code mentioned in the email.',
                          style: TextStyle(color: Color(0xFF989898)),
                        ),
                      ],
                    ),
                  ),
                  SizedBox(height: 40),
                  //otp text field...
                  GestureDetector(
                    onTap: () {
                      FocusScope.of(context).requestFocus(_focusNode);
                    },
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: List.generate(otpLength, (i) {
                        String text = _otpController.text;
                        bool isActive = i == text.length;

                        return Container(
                          width: 55,
                          height: 55,
                          alignment: Alignment.center,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(
                              color: isActive
                                  ? Color(0xFF648DDB)
                                  : Color(0xFFE1E1E1),
                              width: 2,
                            ),
                          ),
                          child: Text(
                            i < text.length ? text[i] : "",
                            style: GoogleFonts.poppins(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        );
                      }),
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    _errorText ?? "", // empty string when no error
                    style: const TextStyle(color: Colors.red, fontSize: 12),
                  ),
                  // Hidden text field
                  SizedBox(
                    height: 0,
                    width: 0,
                    child: TextField(
                      controller: _otpController,
                      focusNode: _focusNode,
                      //keyboardType: TextInputType.number,
                      maxLength: otpLength,
                      onChanged: (_) => setState(() {}),
                      // Hide it
                      style: const TextStyle(color: Colors.transparent),
                      showCursor: false,
                      cursorColor: Colors.transparent, // hides cursor
                      enableInteractiveSelection: false,
                      decoration: const InputDecoration(
                        counterText: "",
                        border: InputBorder.none,
                      ),
                    ),
                  ),
                  SizedBox(height: 20),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: _submitOtp,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xFF4BAE4F),
                        foregroundColor: Color(0xFFFFFFFF),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadiusGeometry.circular(8),
                        ),
                      ),
                      child: Text(
                        'Verify Code',
                        style: TextStyle(
                          //fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                  SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        "Haven't got the email yet? ",
                        style: TextStyle(
                          fontSize: 12,
                          color: Color(0xFF828282),
                        ),
                      ),
                      TextButton(
                        onPressed: () {
                          //resend email
                        },
                        style: TextButton.styleFrom(
                          //side: BorderSide(color: Colors.black),
                          padding: EdgeInsets.zero,
                          minimumSize: Size.zero,
                        ),
                        child: Text(
                          'Resend email',
                          style: GoogleFonts.inter(color: Color(0xFF2E7D32)),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
