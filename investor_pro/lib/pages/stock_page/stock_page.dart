import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:investor_pro/models/price_data_model.dart';
import 'package:investor_pro/models/stock_model.dart';
import 'package:investor_pro/pages/stock_page/daily_increase_pie_chart.dart';
import 'package:investor_pro/pages/stock_page/date_range_selector.dart';
import 'package:investor_pro/pages/stock_page/normal_distribution_chart.dart';
import 'package:investor_pro/providers/explore_page_provider.dart';
import 'package:investor_pro/providers/main_page_provider.dart';
import 'package:investor_pro/session_manager.dart';
import 'package:investor_pro/widgets/full_screen_loading.dart';
import 'package:provider/provider.dart';
import 'package:investor_pro/pages/stock_page/price_chart.dart';
import 'package:investor_pro/providers/stock_page_provider.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/widgets/custom_app_bar.dart';

class StockPage extends StatefulWidget {
  final String stockId;

  const StockPage({super.key, required this.stockId});

  @override
  _StockPageState createState() => _StockPageState();
}

class _StockPageState extends State<StockPage> {
  String currentRange = '1M'; // Default range

  @override
  Widget build(BuildContext context) {
    final portfolios = Provider.of<MainPageProvider>(context, listen: false)
        .portfolios
        .map((e) => e.name)
        .toList();
    return ChangeNotifierProvider<StockProvider>(
      create: (_) => StockProvider(widget.stockId),
      child: Consumer<StockProvider>(
        builder: (context, viewModel, child) {
          final stock = viewModel.stock;
          final filteredData =
              filterDataByRange(viewModel.priceData, currentRange);

          return LoadingOverlay(
            isLoading: viewModel.isLoading,
            child: Scaffold(
              appBar: CustomAppBar(
                title: 'Stock Details',
                showBackButton: true,
                actions: [
                  IconButton(
                    icon: const Icon(Icons.add),
                    onPressed: () {
                      _showAddToPortfolioDialog(context, viewModel, portfolios);
                    },
                  ),
                ],
              ),
              body: SingleChildScrollView(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      stock?.symbol.toString() ?? '',
                      style: Theme.of(context).textTheme.headline3?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: AppColors.secondary,
                          ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      stock?.name ?? '',
                      style: Theme.of(context).textTheme.subtitle1?.copyWith(
                            color: Colors.grey[600],
                          ),
                    ),
                    const SizedBox(height: 16),
                    Divider(color: Colors.grey[400]),
                    const SizedBox(height: 16),
                    Text(
                      'Company Details',
                      style: Theme.of(context).textTheme.headline6?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      stock?.description ?? '',
                      style: const TextStyle(
                          fontSize: 16, color: AppColors.onBackground),
                    ),
                    const SizedBox(height: 16),
                    Divider(color: Colors.grey[400]),
                    const SizedBox(height: 16),
                    Text(
                      'Price Chart',
                      style: Theme.of(context).textTheme.headline6?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 8),
                    DateRangeSelector(
                      onRangeSelected: (range) {
                        setState(() {
                          currentRange = range;
                        });
                      },
                    ),
                    const SizedBox(height: 16),
                    StockPriceChart(
                      data: filteredData,
                      dateRange: currentRange,
                    ),
                    const SizedBox(height: 32),
                    Divider(color: Colors.grey[400]),
                    const SizedBox(height: 16),
                    Text(
                      'Statistics:',
                      style: Theme.of(context)
                          .textTheme
                          .headline4
                          ?.copyWith(
                            fontWeight: FontWeight.bold,
                          )
                          .copyWith(fontSize: 30),
                    ),
                    Text(
                      'Over ${viewModel.stock?.sharpeRatio.totalDaysInView} days.',
                      style: const TextStyle(
                          fontSize: 16, color: AppColors.onBackground),
                    ),
                    const SizedBox(
                      height: 20,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Sharpe Ratio: ${viewModel.stock?.sharpeRatio.sharpRatio.toStringAsFixed(3)}',
                          style: Theme.of(context)
                              .textTheme
                              .headline6
                              ?.copyWith(
                                  fontWeight: FontWeight.bold, fontSize: 25),
                        ),
                        GestureDetector(
                            onTap: () => showSharpeRatioExplanation(context),
                            child: const Icon(
                              Icons.info_outline,
                              color: Colors.white,
                            )),
                      ],
                    ),
                    Divider(color: Colors.grey[400]),
                    const SizedBox(
                      height: 15,
                    ),
                    Text(
                      'Daily Increase:',
                      style: Theme.of(context).textTheme.headline6?.copyWith(
                            fontWeight: FontWeight.bold,
                            fontSize: 25,
                          ),
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    SizedBox(
                      child: DailyIncreasePieChart(
                        data: viewModel.stock?.dailyIncrease.buckets ?? [],
                      ),
                    ),
                    const SizedBox(
                      height: 10,
                    ),
                    Divider(color: Colors.grey[400]),
                    const SizedBox(
                      height: 10,
                    ),
                    // NormalDistributionChart(
                    //   stdDev:
                    //       viewModel.stock?.normalDistribution.stdDailyReturns ??
                    //           0,
                    //   mean:
                    //       viewModel.stock?.normalDistribution.avgDailyReturns ??
                    //           0,
                    // )
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  void showSharpeRatioExplanation(BuildContext context) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Sharpe Ratio Explanation'),
          content: const SingleChildScrollView(
            child: Text(
              'The Sharpe Ratio measures the performance of an investment compared to a risk-free asset, adjusting for its risk. It shows the return earned per unit of risk, helping investors evaluate the risk-adjusted return of different investments.',
              style:
                  const TextStyle(fontSize: 16, color: AppColors.onBackground),
            ),
          ),
          actions: <Widget>[
            TextButton(
              child: const Text(
                'Close',
                style: const TextStyle(
                    fontSize: 16, color: AppColors.onBackground),
              ),
              onPressed: () {
                Navigator.of(context).pop(); // Dismiss the dialog
              },
            ),
          ],
        );
      },
    );
  }

  void _showAddToPortfolioDialog(
      BuildContext context, StockProvider viewModel, List<String> portfolios) {
    showDialog(
      context: context,
      builder: (context) {
        String selectedPortfolio = portfolios[0];
        return StatefulBuilder(
          builder: (BuildContext context, StateSetter setState) {
            return AlertDialog(
              title: const Text('Add to Portfolio'),
              content: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('Select a portfolio to add this stock to.'),
                  const SizedBox(height: 16),
                  DropdownButton<String>(
                    value: selectedPortfolio,
                    items: portfolios.map((String value) {
                      return DropdownMenuItem<String>(
                        value: value,
                        child: Text(value),
                      );
                    }).toList(),
                    onChanged: (String? newValue) {
                      setState(() {
                        // This now refers to the StateSetter from StatefulBuilder
                        selectedPortfolio = newValue!;
                      });
                    },
                  ),
                ],
              ),
              actions: [
                TextButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  child: const Text(
                    'Cancel',
                    style: TextStyle(color: Colors.white),
                  ),
                ),
                ElevatedButton(
                  onPressed: () {
                    final user = Provider.of<SessionMgr>(context, listen: false)
                            .userId ??
                        '';
                    viewModel.addStockToPortfolio(
                        username: user,
                        portfolioId: selectedPortfolio,
                        stockId: viewModel.stock?.name ?? '');
                    Provider.of<MainPageProvider>(context, listen: false)
                        .getPortfolios(user);
                    Navigator.of(context).pop();
                  },
                  child: const Text('Add'),
                ),
              ],
            );
          },
        );
      },
    );
  }

  List<PriceDataModel> filterDataByRange(
      List<PriceDataModel> data, String range) {
    DateTime now = DateTime.now();
    DateTime startDate;

    switch (range) {
      case '1M':
        startDate = DateTime(now.year, now.month - 1, now.day);
        break;
      case '3M':
        startDate = DateTime(now.year, now.month - 3, now.day);
        break;
      case '6M':
        startDate = DateTime(now.year, now.month - 6, now.day);
        break;
      case '1Y':
        startDate = DateTime(now.year - 1, now.month, now.day);
        break;
      default:
        startDate =
            DateTime(now.year, now.month - 1, now.day); // Default to 1 year
        break;
    }

    return data.where((item) {
      DateTime itemDate = DateTime.parse(item.date);
      return itemDate.isAfter(startDate) &&
          itemDate.isBefore(DateTime(now.year, now.month, now.day + 7));
    }).toList();
  }
}
