import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:investor_pro/api_gateway.dart';
import 'package:investor_pro/mock_data.dart';
import 'package:investor_pro/models/stock_model.dart';

class PortfolioModel {
  final String name;

  /// final List<int> stocks;
  final Map<String, String> stocks;

  PortfolioModel({required this.name, required this.stocks});

  static const String baseUrl = ApiGateway.baseUrl;

  factory PortfolioModel.fromJson(Map<String, dynamic> json) {
    var stockMap = json['stock_list'] as Map<String, dynamic>;

    final portfolioModel = PortfolioModel(
      name: json['port_name'] ?? '',
      stocks: stockMap.map((key, value) => MapEntry(key, value as String)),
    );

    return portfolioModel;
  }

  static Future<List<PortfolioModel>> fetchPortfolios(String userId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/get-all-user-portfolios')
          .replace(queryParameters: {'username': 'shachar'}),

      /// test 'shachar'
    );

    if (response.statusCode == 200) {
      final holder = jsonDecode(response.body) as List<dynamic>;
      final portfoliosList =
          holder.map((model) => PortfolioModel.fromJson(model)).toList();
      return portfoliosList;
    } else {
      throw Exception('Failed to load portfolios');
    }
  }

  static Future<void> addPortfolio(String userId, String portfolioName) async {
    final response = await http.post(
      Uri.parse('$baseUrl/create-new-portfolio'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': userId, 'portfolio_id': portfolioName}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to add portfolio');
    }
  }

  static Future<void> deletePortfolio(String userId, String portfolioId) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/delete-portfolio'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': userId, 'portfolio_id': portfolioId}),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to delete portfolio');
    }
  }

  static Future<void> removeStockFromPortfolio(
      String userId, String portfolioId, String stockId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/remove-stock-from-portfolio'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': userId,
        'portfolio_id': portfolioId,
        'stock_id': stockId
      }),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to delete portfolio');
    }
  }
}
