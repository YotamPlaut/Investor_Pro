import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:investor_pro/models/stock_model.dart';
import 'package:investor_pro/pages/explore/explore_page.dart';
import 'package:investor_pro/pages/login_page.dart';
import 'package:investor_pro/pages/main_page/main_page.dart';
import 'package:investor_pro/pages/sign_up_page.dart';
import 'package:investor_pro/pages/stock_page/stock_page.dart';

enum AppRoutes {
  login,
  signUp,
  main,
  explore,
  stock;

  String get path {
    switch (this) {
      case AppRoutes.login:
        return '/';
      case AppRoutes.signUp:
        return '/signup';
      case AppRoutes.main:
        return '/main';
      case AppRoutes.explore:
        return '/explore';
      case AppRoutes.stock:
        return '/stock';
    }
  }
}

class AppRouter {
  static GoRouter router = GoRouter(
    initialLocation: AppRoutes.login.path,
    routes: [
      GoRoute(
        path: AppRoutes.login.path,
        builder: (context, state) => const LoginPage(),
      ),
      GoRoute(
        path: AppRoutes.signUp.path,
        builder: (context, state) => const SignUpPage(),
      ),
      GoRoute(
        path: AppRoutes.main.path,
        builder: (context, state) => const MainPage(),
      ),
      GoRoute(
        path: AppRoutes.explore.path,
        builder: (context, state) => const ExplorePage(),
      ),
      GoRoute(
        path: AppRoutes.stock.path,
        builder: (context, state) {
          final stockId = state.extra as String;
          return StockPage(stockId: stockId);
        },
      ),
    ],
  );
}

class NavigationHelper {
  static void navigateTo(BuildContext context, AppRoutes route,
      {Object? data}) {
    context.push(route.path, extra: data);
  }
}
