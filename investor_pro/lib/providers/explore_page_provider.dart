import 'package:flutter/material.dart';
import 'package:investor_pro/api_gateway.dart';
import 'package:investor_pro/mock_data.dart';
import 'package:investor_pro/models/stock_model.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ExplorePageProvider with ChangeNotifier {
  List<String> searchResults = [];
  List<String> allStocks = [];
  static const String baseUrl = ApiGateway.baseUrl;
  final TextEditingController searchEditingController = TextEditingController();

  // List<StockModel> trending = MockStockData.portfolio1;
  // List<StockModel> popular = MockStockData.portfolio2;
  // List<StockModel> recentlyAdded = MockStockData.portfolio3;

  bool isLoading = false;

  ExplorePageProvider() {
    initData();
  }

  Future<void> initData() async {
    try {
      isLoading = true;
      allStocks = await getAllStocks();
      searchResults = allStocks; // Initially show all stocks
      notifyListeners();
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  void clearSearchResults() {
    searchResults = allStocks;
    searchEditingController.clear(); // Reset search results to all stocks
    notifyListeners();
  }

  Future<void> searchAssets(String query) async {
    try {
      searchResults = allStocks
          .where((stock) => stock.toLowerCase().contains(query.toLowerCase()))
          .toList();
      notifyListeners(); // Notify listeners after filtering the results
    } catch (e) {
      print(e);
    }
  }

  Future<void> fetchStockDetails(String stockId) async {
    try {
      isLoading = true;
      notifyListeners();
      StockModel stock = await StockModel.fetchStockDetails(stockId);
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> addStockToPortfolio(
      String username, String portfolioId, String stockId) async {
    try {
      isLoading = true;
      notifyListeners();
      await StockModel.addStockToPortfolio(
          portfolioId: portfolioId, stockId: stockId, username: username);
    } catch (e) {
      debugPrint(e.toString());
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  static Future<List<String>> getAllStocks() async {
    final response = await http.get(Uri.parse('$baseUrl/get-all-stocks'));
    if (response.statusCode == 200) {
      final holder = jsonDecode(response.body) as Map<String, dynamic>;
      final list = holder['result'] as List<dynamic>;
      return list.map((e) => e.toString()).toList();
    } else {
      throw Exception('Failed to search assets');
    }
  }
}
