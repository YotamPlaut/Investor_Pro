import 'package:flutter/material.dart';
import 'package:investor_pro/navigation/app_routes.dart';
import 'package:investor_pro/widgets/full_screen_loading.dart';
import 'package:provider/provider.dart';
import 'package:investor_pro/providers/explore_page_provider.dart';
import 'package:investor_pro/theme.dart';

class SearchBottomSheet extends StatelessWidget {
  const SearchBottomSheet({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ExplorePageProvider>(
      builder: (context, viewModel, child) {
        return LoadingOverlay(
          isLoading: viewModel.isLoading,
          child: FractionallySizedBox(
            heightFactor: 0.75, // Occupy 3/4 of the screen height
            child: Padding(
              padding: MediaQuery.of(context).viewInsets,
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: TextField(
                      controller: viewModel.searchEditingController,
                      decoration: InputDecoration(
                        hintText: 'Search for a stock...',
                        hintStyle: TextStyle(color: AppColors.onPrimary),
                        prefixIcon:
                            Icon(Icons.search, color: AppColors.secondary),
                        enabledBorder: OutlineInputBorder(
                          borderSide: BorderSide(color: AppColors.secondary),
                          borderRadius: BorderRadius.circular(10),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderSide:
                              BorderSide(color: AppColors.secondaryVariant),
                          borderRadius: BorderRadius.circular(10),
                        ),
                      ),
                      cursorColor: AppColors.secondary,
                      onChanged: (value) {
                        viewModel.searchAssets(value);
                      },
                    ),
                  ),
                  viewModel.isLoading
                      ? const Center(child: CircularProgressIndicator())
                      : viewModel.searchResults.isEmpty
                          ? const Padding(
                              padding: EdgeInsets.all(16.0),
                              child: Text(
                                'No results found',
                                style: TextStyle(color: AppColors.onPrimary),
                              ),
                            )
                          : Expanded(
                              child: ListView.builder(
                                itemCount: viewModel.searchResults.length,
                                itemBuilder: (context, index) {
                                  final stock = viewModel.searchResults[index];
                                  return ListTile(
                                    title: Text(stock,
                                        style: const TextStyle(
                                            color: AppColors.onSurface)),
                                    onTap: () {
                                      NavigationHelper.navigateTo(
                                          context, AppRoutes.stock,
                                          data: stock);
                                      Navigator.pop(context);
                                    },
                                  );
                                },
                              ),
                            ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
