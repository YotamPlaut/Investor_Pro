import 'dart:convert';
import 'package:intl/intl.dart';
import 'package:investor_pro/models/price_data_model.dart';

class PredictionModel {
  final int indexSymbol;
  final String symbolName;
  List<PriceDataModel> closePredictionsData;

  PredictionModel({
    required this.indexSymbol,
    required this.symbolName,
    required this.closePredictionsData,
  });

  // Factory constructor for creating a new Prediction instance from a map.
  factory PredictionModel.fromJson(Map<String, dynamic> json) {
    var list = json['close_predictions_data'] as List;
    List<PriceDataModel> predictionsList =
        list.map((e) => PriceDataModel.fromJson(e)).toList();
    predictionsList.sort((a, b) => a.date.compareTo(b.date));
    return PredictionModel(
      indexSymbol: json['index_symbol'] as int,
      symbolName: json['symbol_name'] as String,
      closePredictionsData: predictionsList,
    );
  }
}

class ClosePredictionData {
  final DateTime date;
  final double prediction;

  ClosePredictionData({
    required this.date,
    required this.prediction,
  });

  // Factory constructor for creating a new ClosePredictionData instance from a map.
  factory ClosePredictionData.fromJson(Map<String, dynamic> json) {
    return ClosePredictionData(
      date: DateFormat('yyyy-MM-dd HH:mm:ss').parse(json['date']),
      prediction: double.parse(json['prediction'].toString()),
    );
  }
}
