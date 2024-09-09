import 'package:flutter/material.dart';
import 'package:investor_pro/models/price_data_model.dart';
import 'package:investor_pro/models/stock_model.dart';
import 'package:investor_pro/models/stock_predictions.dart';

class ChartData {
  final String date;
  final double price;

  ChartData({required this.date, required this.price});
}

class StockProvider with ChangeNotifier {
  StockModel? stock;
  List<PriceDataModel> priceData = [];
  bool isLoading = false;
  PredictionModel? predictionModel;

  StockProvider(String stockId) {
    initData(stockId);
  }

  void initData(String stockId) async {
    await _fetchStock(stockId);
    await _fetchPredictions(stockId);
    _getPriceData();
  }

  Future<StockModel?> _fetchStock(String stockId) async {
    try {
      isLoading = true;
      notifyListeners();
      stock = await StockModel.fetchStockDetails(stockId);
      debugPrint(stock?.dailyIncrease.buckets
          .map((e) => e.toJson().toString())
          .toList()
          .toString());
      notifyListeners();
      return stock;
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<PredictionModel?> _fetchPredictions(String stockId) async {
    try {
      isLoading = true;
      notifyListeners();
      predictionModel = await StockModel.fetchStockPredictions(stockId);
      notifyListeners();
      return predictionModel;
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> addStockToPortfolio(
      {required String username,
      required String portfolioId,
      required String stockId}) async {
    try {
      isLoading = true;
      notifyListeners();
      await StockModel.addStockToPortfolio(
          username: username, portfolioId: portfolioId, stockId: stockId);
      notifyListeners();
    } catch (e) {
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> _getPriceData() async {
    priceData = stock?.priceData ?? [];
    final predictions = predictionModel?.closePredictionsData;
    predictions?.removeWhere(
        (data) => DateTime.parse(data.date).isBefore(DateTime.now()));
    priceData.addAll(predictions?.map((e) => e) ?? []);
  }
}
