import 'package:flutter/material.dart';

class AppColors {
  // Primary colors
  static const Color primary = Color(0xFF1F1F1F); // Dark grey
  static const Color primaryVariant = Color(0xFF121212); // Almost black

  // Secondary colors
  static const Color secondary = Color(0xFFBB86FC); // Vibrant purple
  static const Color secondaryVariant = Color(0xFF3700B3); // Deep purple

  // Background and surface colors
  static const Color background = Color(0xFF121212); // Almost black
  static const Color surface = Color(0xFF1F1F1F); // Dark grey

  // Error colors
  static const Color error = Color(0xFFCF6679); // Soft red

  // On colors
  static const Color onPrimary = Colors.white38; // White
  static const Color onSecondary = Color(0xFF000000); // Black
  static const Color onBackground = Color(0xFFFFFFFF); // White
  static const Color onSurface = Color(0xFFFFFFFF); // White
  static const Color onError = Color(0xFF000000); // Black
}

class AppFonts {
  static const String primaryFont = 'Roboto';

  static const TextStyle displayLarge = TextStyle(
    fontFamily: primaryFont,
    fontSize: 96,
    fontWeight: FontWeight.w300,
    letterSpacing: -1.5,
  );

  static const TextStyle displayMedium = TextStyle(
    fontFamily: primaryFont,
    fontSize: 60,
    fontWeight: FontWeight.w300,
    letterSpacing: -0.5,
  );

  static const TextStyle displaySmall = TextStyle(
    fontFamily: primaryFont,
    fontSize: 48,
    fontWeight: FontWeight.normal,
    letterSpacing: 0,
  );

  static const TextStyle headlineLarge = TextStyle(
    fontFamily: primaryFont,
    fontSize: 34,
    fontWeight: FontWeight.normal,
    letterSpacing: 0.25,
  );

  static const TextStyle headlineMedium = TextStyle(
    fontFamily: primaryFont,
    fontSize: 24,
    fontWeight: FontWeight.normal,
    letterSpacing: 0,
  );

  static const TextStyle headlineSmall = TextStyle(
    fontFamily: primaryFont,
    fontSize: 20,
    fontWeight: FontWeight.normal,
    letterSpacing: 0.15,
  );

  static const TextStyle titleMedium = TextStyle(
    fontFamily: primaryFont,
    fontSize: 16,
    fontWeight: FontWeight.normal,
    letterSpacing: 0.15,
  );

  static const TextStyle titleSmall = TextStyle(
    fontFamily: primaryFont,
    fontSize: 14,
    fontWeight: FontWeight.normal,
    letterSpacing: 0.1,
  );

  static const TextStyle bodyLarge = TextStyle(
    fontFamily: primaryFont,
    fontSize: 16,
    fontWeight: FontWeight.normal,
    letterSpacing: 0.5,
  );

  static const TextStyle bodyMedium = TextStyle(
    fontFamily: primaryFont,
    fontSize: 14,
    fontWeight: FontWeight.normal,
    letterSpacing: 0.25,
  );

  static const TextStyle labelLarge = TextStyle(
    fontFamily: primaryFont,
    fontSize: 14,
    fontWeight: FontWeight.normal,
    letterSpacing: 1.25,
  );

  static const TextStyle bodySmall = TextStyle(
    fontFamily: primaryFont,
    fontSize: 12,
    fontWeight: FontWeight.normal,
    letterSpacing: 0.4,
  );

  static const TextStyle labelSmall = TextStyle(
    fontFamily: primaryFont,
    fontSize: 10,
    fontWeight: FontWeight.normal,
    letterSpacing: 1.5,
  );
}

ThemeData appTheme = ThemeData(
  primaryColor: AppColors.primary,
  primaryColorDark: AppColors.primaryVariant,
  scaffoldBackgroundColor: AppColors.background,
  textTheme: const TextTheme(
    displayLarge: AppFonts.displayLarge,
    displayMedium: AppFonts.displayMedium,
    displaySmall: AppFonts.displaySmall,
    headlineLarge: AppFonts.headlineLarge,
    headlineMedium: AppFonts.headlineMedium,
    headlineSmall: AppFonts.headlineSmall,
    titleMedium: AppFonts.titleMedium,
    titleSmall: AppFonts.titleSmall,
    bodyLarge: AppFonts.bodyLarge,
    bodyMedium: AppFonts.bodyMedium,
    labelLarge: AppFonts.labelLarge,
    bodySmall: AppFonts.bodySmall,
    labelSmall: AppFonts.labelSmall,
  ),
  colorScheme: const ColorScheme(
    primary: AppColors.primary,
    primaryContainer: AppColors.primaryVariant,
    secondary: AppColors.secondary,
    secondaryContainer: AppColors.secondaryVariant,
    surface: AppColors.surface,
    background: AppColors.background,
    error: AppColors.error,
    onPrimary: AppColors.onPrimary,
    onSecondary: AppColors.onSecondary,
    onSurface: AppColors.onSurface,
    onBackground: AppColors.onBackground,
    onError: AppColors.onError,
    brightness: Brightness.light,
  ).copyWith(background: AppColors.background),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ButtonStyle(
      backgroundColor: MaterialStateProperty.all(AppColors.onBackground),
      foregroundColor: MaterialStateProperty.all(AppColors.secondaryVariant),
      padding: MaterialStateProperty.all(
          EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0)),
      textStyle: MaterialStateProperty.all(
          TextStyle(fontSize: 16.0, fontWeight: FontWeight.bold)),
    ),
  ),
);
