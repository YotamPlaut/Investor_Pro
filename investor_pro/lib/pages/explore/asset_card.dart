import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:investor_pro/models/stock_model.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/navigation/app_routes.dart';

class AssetCard extends StatelessWidget {
  final String stock;

  const AssetCard({super.key, required this.stock});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () =>
          NavigationHelper.navigateTo(context, AppRoutes.stock, data: stock),
      child: Card(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
        child: Container(
          width: 150, // Adjust width as needed
          padding: const EdgeInsets.all(10),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                stock ?? '',
                style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 15),
              ),
              SizedBox(height: 5),
              // Text(
              //   stock?.symbol.toString() ?? '',
              //   style: TextStyle(
              //     color: AppColors.secondary,
              //   ),
              // ),
              // Add more details if necessary
            ],
          ),
        ),
      ),
    );
  }
}
