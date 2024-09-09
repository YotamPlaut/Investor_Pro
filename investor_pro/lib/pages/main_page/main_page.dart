import 'package:another_flushbar/flushbar.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:investor_pro/navigation/app_routes.dart';
import 'package:investor_pro/navigation/navigation_utils.dart';
import 'package:investor_pro/pages/main_page/add_portfolio_dialog.dart';
import 'package:investor_pro/pages/main_page/portfolio_list.dart';
import 'package:investor_pro/providers/main_page_provider.dart';
import 'package:investor_pro/session_manager.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';
import 'package:investor_pro/widgets/custom_button.dart';
import 'package:investor_pro/widgets/full_screen_loading.dart';
import 'package:provider/provider.dart';

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    final userId = Provider.of<SessionMgr>(context, listen: false).userId ?? '';


    return ChangeNotifierProvider<MainPageProvider>(
      create: (_) => MainPageProvider(userId),
      child: Consumer<MainPageProvider>(
        builder: (context, viewModel, child) {
          return LoadingOverlay(
            isLoading: viewModel.isLoading,
            child: RefreshIndicator(
              onRefresh: () => viewModel.getPortfolios(userId),
              child: Scaffold(
                appBar: const CustomAppBar(
                  title: 'Investor Pro',
                  showBackButton: false,
                ),
                body: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Column(
                    children: [
                      const SizedBox(
                        height: 8,
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Expanded(
                            child: CustomButton(
                              onPressed: () => NavigationHelper.navigateTo(
                                  context, AppRoutes.explore),
                              title: 'Explore',
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(
                        height: 8,
                      ),
                      const Divider(
                        color: AppColors.onPrimary,
                      ),
                      //SearchSection(),
                      const SizedBox(height: 10),
                      CustomAppBar(
                        title: 'My Portfolios',
                        showBackButton: false,
                        transparentBackGround: true,
                        actions: [
                          IconButton(
                            icon: const Icon(Icons.add),
                            onPressed: () =>
                                _navigateToAddPortfolio(context, viewModel),
                          ),
                        ],
                      ),
                      const SizedBox(height: 15),
                      Expanded(
                        child: PortfolioList(
                            portfolios: viewModel.portfolios,
                            viewModel: viewModel),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Future<NavigationResult?> _navigateToAddPortfolio(
      BuildContext context, MainPageProvider viewModel) async {
    final result = await showDialog(
      context: context,
      builder: (context) => AddPortfolioDialog(
        onPortfolioCreated: (portfolioName) {
          viewModel.addPortfolio(
              Provider.of<SessionMgr>(context, listen: false).userId ?? '',
              portfolioName);
        },
      ),
    );

    // if (result == NavigationResult.success) {
    //   if (!context.mounted) return null;
    //   Flushbar(
    //     message: 'Portfolio added successfully',
    //     duration: const Duration(seconds: 3),
    //   ).show(context);
    // }
  }
}
