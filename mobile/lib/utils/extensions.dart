extension ExtString on String {

  bool get isValidName {
    final nameRegExp = RegExp(r"^[a-zA-ZÀ-ÖØ-öø-ÿ' -]+$");
    return nameRegExp.hasMatch(this);
  }

  bool get isValidEmail {
    final emailRegExp = RegExp(r'^[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
    return emailRegExp.hasMatch(this);
  }

  bool get isValidPassword {
    final passwordRegExp = RegExp(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#\$&*~]).{8,}$');
    return passwordRegExp.hasMatch(this);
  }

  /// Validates username: 3-50 chars, alphanumeric + underscore only.
  bool get isValidUsername {
    return RegExp(r'^[a-zA-Z0-9_]{3,50}$').hasMatch(this);
  }

}

// -={}[]|\:";'<>,.?/!@#$%^&*()_+