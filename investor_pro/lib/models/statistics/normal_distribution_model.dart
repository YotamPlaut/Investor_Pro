import 'package:intl/intl.dart';

class NormalDistributionModel {
  int totalDaysInView;
  double avgDailyReturns;
  double stdDailyReturns;
  DateTime insertTime;

  NormalDistributionModel({
    required this.totalDaysInView,
    required this.avgDailyReturns,
    required this.stdDailyReturns,
    required this.insertTime,
  });

  // Factory constructor to create a NormalDistributionModel from a JSON map.
  factory NormalDistributionModel.fromJson(Map<String, dynamic> json) {
    return NormalDistributionModel(
      totalDaysInView: json['stats_info']['total_days_in_view'] as int,
      avgDailyReturns: json['stats_info']['avg_daily_returns'].toDouble(),
      stdDailyReturns: json['stats_info']['std_daily_returns'].toDouble(),
      insertTime: DateFormat('yyyy-MM-dd').parse(json['insert_time']),
    );
  }

  // Method to convert the NormalDistributionModel instance to a JSON map.
  Map<String, dynamic> toJson() {
    return {
      'stats_info': {
        'total_days_in_view': totalDaysInView,
        'avg_daily_returns': avgDailyReturns,
        'std_daily_returns': stdDailyReturns,
      },
      'insert_time': DateFormat('yyyy-MM-dd').format(insertTime),
    };
  }
}
