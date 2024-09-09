import 'package:intl/intl.dart';

class SharpeRatioModel {
  int totalDaysInView;
  double sharpRatio;
  DateTime insertTime;

  SharpeRatioModel({
    required this.totalDaysInView,
    required this.sharpRatio,
    required this.insertTime,
  });

  // Factory constructor to create a new SharpeRatioModel from a map.
  factory SharpeRatioModel.fromJson(Map<String, dynamic> json) {
    return SharpeRatioModel(
      totalDaysInView: json['stats_info']['total_days_in_view'] as int,
      sharpRatio: json['stats_info']['sharp_ratio'] as double,
      insertTime: DateFormat('yyyy-MM-dd').parse(json['insert_time']),
    );
  }

  // Method to convert the SharpeRatioModel instance to a map.
  Map<String, dynamic> toJson() {
    return {
      'stats_info': {
        'total_days_in_view': totalDaysInView,
        'sharp_ratio': sharpRatio,
      },
      'insert_time': DateFormat('yyyy-MM-dd').format(insertTime),
    };
  }
}
