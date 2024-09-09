import 'package:flutter/material.dart';
import 'package:investor_pro/models/portfolio_model.dart';
import 'package:investor_pro/pages/main_page/portfolio_card.dart';
import 'package:investor_pro/providers/main_page_provider.dart';
import 'package:investor_pro/session_manager.dart';
import 'package:provider/provider.dart';

class PortfolioList extends StatelessWidget {
  PortfolioList({super.key, required this.portfolios, required this.viewModel});

  late List<PortfolioModel> portfolios;
  final MainPageProvider viewModel;

  @override
  Widget build(BuildContext context) {
    final user = Provider.of<SessionMgr>(context, listen: false).userId ?? '';
    return ListView.builder(
      itemCount: portfolios.length,
      itemBuilder: (context, index) {
        final portfolio = portfolios[index];
        return PortfolioCard(
          portfolio: portfolio,
          onDelete: () {
            portfolios.removeAt(index);
            viewModel.deletePortfolio(
              Provider.of<SessionMgr>(context, listen: false).userId ?? '',
              portfolio.name,
            );
          },
          onRemoveStock: viewModel.removeStockFromPortfolio,
        );
      },
    );
  }
}
