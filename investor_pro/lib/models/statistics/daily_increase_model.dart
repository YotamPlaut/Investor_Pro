import 'package:intl/intl.dart';
import 'package:investor_pro/models/statistics/daily_increase_buckets_model.dart';

class DailyIncreaseModel {
  int totalDaysInView;
  List<BucketDataModel>
      buckets; // Assuming buckets is a list of dynamic elements; specify the type if possible
  DateTime insertTime;

  DailyIncreaseModel({
    required this.totalDaysInView,
    required this.buckets,
    required this.insertTime,
  });

  // Factory constructor to create a DailyIncreaseModel from a JSON map.
  factory DailyIncreaseModel.fromJson(Map<String, dynamic> json) {
    final list = json['stats_info']['buckets'] as List;
    final bucketsList = list.map((e) => BucketDataModel.fromJson(e)).toList();
    return DailyIncreaseModel(
      totalDaysInView: json['stats_info']['total_days_in_view'] as int,
      buckets: bucketsList,
      insertTime: DateFormat('yyyy-MM-dd').parse(json['insert_time']),
    );
  }

  // Method to convert the DailyIncreaseModel instance to a JSON map.
  Map<String, dynamic> toJson() {
    return {
      'stats_info': {
        'total_days_in_view': totalDaysInView,
        'buckets': buckets,
      },
      'insert_time': DateFormat('yyyy-MM-dd').format(insertTime),
    };
  }
}
