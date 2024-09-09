// To parse this JSON data, do
//
//     final priceDataModel = priceDataModelFromJson(jsonString);

import 'dart:convert';


String priceDataModelToJson(PriceDataModel data) => json.encode(data.toJson());

class PriceDataModel {
  final String date;
  final double closePrice;

  PriceDataModel({
    required this.date,
    required this.closePrice,
  });

  factory PriceDataModel.fromJson(Map<String, dynamic> json) => PriceDataModel(
        date: json["date"] as String,
        closePrice: json["close_price"] as double,
      );

  Map<String, dynamic> toJson() => {
        "date": date,
        "close_price": closePrice,
      };
}
