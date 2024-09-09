import 'package:another_flushbar/flushbar.dart';
import 'package:flutter/material.dart';
import 'package:investor_pro/navigation/app_routes.dart';
import 'package:investor_pro/providers/sign_up_provider.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';
import 'package:investor_pro/widgets/custom_button.dart';
import 'package:investor_pro/widgets/full_screen_loading.dart';
import 'package:provider/provider.dart';

class SignUpPage extends StatefulWidget {
  const SignUpPage({Key? key}) : super(key: key);

  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<SignUpProvider>(
      create: (_) => SignUpProvider(),
      child: Consumer<SignUpProvider>(
        builder: (context, viewModel, child) {
          return Scaffold(
            backgroundColor: AppColors.background,
            appBar: const CustomAppBar(
              title: 'Sign Up',
              showBackButton: true,
            ),
            body: LoadingOverlay(
              isLoading: viewModel.isLoading,
              child: SingleChildScrollView(
                child: Center(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 50),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const SizedBox(height: 40),
                        TextField(
                          controller: viewModel.usernameController,
                          decoration: const InputDecoration(
                            hintText: 'Username',
                            hintStyle: TextStyle(color: AppColors.onPrimary),
                          ),
                          cursorColor: AppColors.secondary,
                        ),
                        const SizedBox(height: 15),
                        TextField(
                          controller: viewModel.emailController,
                          decoration: const InputDecoration(
                            hintText: 'Email',
                            hintStyle: TextStyle(color: AppColors.onPrimary),
                          ),
                          cursorColor: AppColors.secondary,
                        ),
                        const SizedBox(height: 15),
                        TextField(
                          controller: viewModel.passwordController,
                          decoration: const InputDecoration(
                            hintText: 'Password',
                            hintStyle: TextStyle(color: AppColors.onPrimary),
                          ),
                          cursorColor: AppColors.secondary,
                          obscureText: true,
                        ),
                        const SizedBox(height: 15),
                        TextField(
                          controller: viewModel.confirmPasswordController,
                          decoration: const InputDecoration(
                            hintText: 'Confirm Password',
                            hintStyle: TextStyle(color: AppColors.onPrimary),
                          ),
                          cursorColor: AppColors.secondary,
                          obscureText: true,
                        ),
                        const SizedBox(height: 30),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Expanded(
                              child: CustomButton(
                                title: 'Sign Up',
                                onPressed: () async {
                                  try {
                                    /// add email ? or fix to get only two arguments
                                    final response =
                                        await viewModel.registerUser(
                                      username:
                                          viewModel.usernameController.text,
                                      password:
                                          viewModel.passwordController.text,
                                      emailAddress:
                                          viewModel.emailController.text,
                                    );

                                    if (!mounted) return;

                                    // Handle successful registration
                                    NavigationHelper.navigateTo(
                                        context, AppRoutes.login);
                                  } catch (e) {
                                    if (!mounted) return;

                                    Flushbar(
                                      message: e.toString(),
                                      duration: const Duration(seconds: 3),
                                    ).show(context);
                                  }
                                },
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 20),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Text(
                              "Already have an account?",
                              style: TextStyle(color: AppColors.onPrimary),
                            ),
                            TextButton(
                              onPressed: () => NavigationHelper.navigateTo(
                                  context, AppRoutes.login),
                              child: const Text(
                                'Login',
                                style: TextStyle(color: AppColors.secondary),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
