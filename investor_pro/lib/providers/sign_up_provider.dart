import 'package:flutter/cupertino.dart';
import 'package:investor_pro/models/user_model.dart';

class SignUpProvider with ChangeNotifier {
  late final UserModel? user;

  final TextEditingController usernameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController confirmPasswordController =
      TextEditingController();

  bool isLoading = false;

  Future? registerUser(
      {required String username,
      required String password,
      required String emailAddress}) async {
    isLoading = true;
    notifyListeners();

    UserModel user =
        UserModel(username: username, email: emailAddress, password: password);

    debugPrint('stop');
    try {
      final result = await UserModel.registerUser(user);
      debugPrint(result.toString());
    } catch (err) {
      debugPrint(err.toString());
      isLoading = false;
      notifyListeners();
      rethrow;
    }


    isLoading = false;
    notifyListeners();
  }
}
