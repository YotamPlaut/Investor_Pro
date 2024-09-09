import 'package:flutter/cupertino.dart';
import 'package:investor_pro/models/user_model.dart';
import 'package:investor_pro/providers/main_page_provider.dart';
import 'package:investor_pro/session_manager.dart';
import 'package:provider/provider.dart';

class LoginProvider with ChangeNotifier {
  late final TextEditingController usernameController = TextEditingController();
  late final TextEditingController passwordController = TextEditingController();

  bool isLoading = false;

  Future? performLogin(String userId, String password) async {
    startLoading();
    final String userIdTrimmed = userId.trim();
    final String passwordTrimmed = password.trim();
    final result = await UserModel.login(userIdTrimmed, passwordTrimmed)
        .catchError((error) {
      debugPrint(error.toString());
      stopLoading();
      throw (error);
    });
    debugPrint('stop');
    stopLoading();
    return result;
  }

  void startLoading() {
    isLoading = true;
    notifyListeners();
  }

  void stopLoading() {
    isLoading = false;
    notifyListeners();
  }
}
