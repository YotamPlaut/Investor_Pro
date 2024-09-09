import 'package:flutter/material.dart';
import 'package:investor_pro/navigation/app_routes.dart';
import 'package:investor_pro/pages/main_page/main_page.dart';
import 'package:investor_pro/providers/main_page_provider.dart';
import 'package:investor_pro/session_manager.dart';
import 'package:investor_pro/providers/explore_page_provider.dart'; // Import ExplorePageProvider
import 'package:investor_pro/theme.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<SessionMgr>(
          create: (context) => SessionMgr(),
        ),
        ChangeNotifierProvider<ExplorePageProvider>(
          create: (context) => ExplorePageProvider(),
        ),
        ChangeNotifierProvider<MainPageProvider>(
          create: (context) => MainPageProvider(
              Provider.of<SessionMgr>(context, listen: false).userId ?? ''),
        ),
        // Add more providers here if needed
      ],
      child: MaterialApp.router(
        debugShowCheckedModeBanner: false,
        routerConfig: AppRouter.router,
        title: 'Flutter Demo',
        theme: appTheme, // Apply the theme
      ),
    );
  }
}
