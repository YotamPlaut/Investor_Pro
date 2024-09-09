import 'package:flutter/material.dart';
import 'package:investor_pro/navigation/app_routes.dart';
import 'package:investor_pro/models/stock_model.dart';
import 'package:investor_pro/pages/explore/asset_card.dart';
import 'package:investor_pro/theme.dart';

class HorizontalAssetsList extends StatelessWidget {
  final String title;
  final List<String> stocksList;

  const HorizontalAssetsList(
      {super.key, required this.title, required this.stocksList});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: AppColors.secondary,
          ),
        ),
        const SizedBox(height: 10),
        SizedBox(
          height: 150, // Adjust height as needed
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: stocksList.length, // Number of items in the section
            itemBuilder: (context, index) {
              return AssetCard(stock: stocksList[index]);
            },
          ),
        ),
      ],
    );
  }
}
