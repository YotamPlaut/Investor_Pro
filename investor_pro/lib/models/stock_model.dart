import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:investor_pro/api_gateway.dart';
import 'package:investor_pro/models/price_data_model.dart';
import 'package:investor_pro/models/statistics/daily_increase_model.dart';
import 'package:investor_pro/models/statistics/normal_distribution_model.dart';
import 'package:investor_pro/models/statistics/sharpe_ratio_model.dart';
import 'package:investor_pro/models/stock_predictions.dart';

class StockModel {
  final String name;
  final int symbol;
  final String description;
  final int numDays;
  final List<PriceDataModel> priceData;
  final DailyIncreaseModel dailyIncrease;
  final SharpeRatioModel sharpeRatio;
  final NormalDistributionModel normalDistribution;

  StockModel(
      {required this.name,
      required this.symbol,
      required this.description,
      required this.numDays,
      required this.priceData,
      required this.dailyIncrease,
      required this.normalDistribution,
      required this.sharpeRatio});

  factory StockModel.fromJson(Map<String, dynamic> json) {
    final prices = json['price_data'] as List<dynamic>;
    // final pricesAsListOfMaps = prices as List<Map<String, dynamic>>;
    final pricesAsList = prices.map((e) => PriceDataModel.fromJson(e)).toList();
    return StockModel(
      name: json['name'] as String,
      symbol: json['symbol'] as int,
      numDays: json['num_days'] as int,
      description: json['description'] as String,
      priceData: pricesAsList,
      dailyIncrease: DailyIncreaseModel.fromJson(json['daily_increase']),
      normalDistribution:
          NormalDistributionModel.fromJson(json['norm_distribution']),
      sharpeRatio: SharpeRatioModel.fromJson(json['sharpe_ratio']),
    );
  }

  static const String baseUrl = ApiGateway.baseUrl;

  static Future<List<StockModel>> searchAssets(String query) async {
    final response = await http
        .get(Uri.parse('http://your-api-url.com/search?query=$query'));
    if (response.statusCode == 200) {
      Iterable list = jsonDecode(response.body);
      return list.map((model) => StockModel.fromJson(model)).toList();
    } else {
      throw Exception('Failed to search assets');
    }
  }

  static Future<StockModel> fetchStockDetails(String stockId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/get-stock-info')
          .replace(queryParameters: {'stock_name': stockId}),
    );
    if (response.statusCode == 200) {
      return StockModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load stock details');
    }
  }

  static Future<PredictionModel> fetchStockPredictions(String stockId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/get-stock-prediction')
          .replace(queryParameters: {'stock_name': stockId}),
    );
    if (response.statusCode == 200) {
      return PredictionModel.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load stock details');
    }
  }

  static Future<void> addStockToPortfolio({
      required String username, required String portfolioId, required String stockId}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/add-stock-to-portfolio'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'portfolio_id': portfolioId,
        'stock_id': stockId
      }),
    );
    if (response.statusCode != 201) {
      throw Exception('Failed to add stock to portfolio');
    }
  }

// static Future<List<ChartData>> fetchPriceData(String stockId) async {
//   final response = await http.get(Uri.parse('http://your-api-url.com/stocks/$stockId/price-data'));
//   if (response.statusCode == 200) {
//     Iterable list = jsonDecode(response.body);
//    // return list.map((model) => ChartData(model['date'], model['price'])).toList();
//   } else {
//     throw Exception('Failed to load price data');
//   }
// }
}
