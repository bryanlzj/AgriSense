import 'package:flutter/material.dart';

class CustomFormField extends StatefulWidget {
  //final bool obscureText;
  final bool isPassword;
  final String hintText;
  final String? Function(String?) validator;
  final TextEditingController controller;

  const CustomFormField({
    super.key,
    required this.hintText,
    required this.validator,
    //this.obscureText = false,
    this.isPassword = false,
    required this.controller,
  });

  @override
  State<CustomFormField> createState() => _CustomFormFieldState();
}

class _CustomFormFieldState extends State<CustomFormField> {
  bool _obscureText = true;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsetsGeometry.symmetric(vertical: 10),
      child: TextFormField(
        controller: widget.controller,
        obscureText: widget.isPassword ? _obscureText : false,
        cursorColor: Color(0xFF53AD64),//0xFF53AD64
        decoration: InputDecoration(
          //labelText: 'Name',
          errorMaxLines: 2,
          hintText: widget.hintText,
          contentPadding: EdgeInsets.symmetric(vertical: 10, horizontal: 16),
          hintStyle: TextStyle(
            color: Color(0xFF828282),
            fontSize: 14
          ),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: BorderSide(color: Color(0xFFE0E0E0)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: BorderSide(color: Color(0xFF53AD64)),
          ),
          suffixIcon: widget.isPassword
              ? IconButton(
                  icon: Icon(
                    _obscureText 
                      ? Icons.visibility_outlined 
                      : Icons.visibility_off_outlined,
                    color: Color(0xFFAFB1B6),
                  ),
                  onPressed: () {
                    setState(() {
                      _obscureText = !_obscureText;
                    });
                  },
                )
              : null,
        ),
        validator: widget.validator,
      ),
    );
  }
}