import 'package:flutter/material.dart';
import 'package:investor_pro/pages/explore/search_bottom_sheet.dart';
import 'package:investor_pro/providers/explore_page_provider.dart';
import 'package:investor_pro/theme.dart';
import 'package:provider/provider.dart';

class SearchSection extends StatelessWidget {
  const SearchSection({super.key});

  void _openSearchBottomSheet(BuildContext context) {
    final provider = Provider.of<ExplorePageProvider>(context, listen: false);

    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      backgroundColor: AppColors.surface,
      isScrollControlled: true,
      builder: (context) => const SearchBottomSheet(),
    ).then((value) => provider.clearSearchResults());
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => _openSearchBottomSheet(context),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 15),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: AppColors.secondary),
        ),
        child: Row(
          children: [
            Icon(Icons.search, color: AppColors.secondary),
            const SizedBox(width: 10),
            Text(
              'Search assets',
              style: TextStyle(color: AppColors.onPrimary),
            ),
          ],
        ),
      ),
    );
  }
}
