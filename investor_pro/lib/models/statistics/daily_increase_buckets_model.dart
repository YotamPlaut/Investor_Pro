class BucketDataModel {
  final double bucketStart;
  final double bucketEnd;
  final int count;
  final double percentageOfTotal;

  BucketDataModel({
    required this.bucketStart,
    required this.bucketEnd,
    required this.count,
    required this.percentageOfTotal,
  });

  // Factory constructor to create a BucketData from a JSON map.
  factory BucketDataModel.fromJson(Map<String, dynamic> json) {
    return BucketDataModel(
      bucketStart: json['bucket_start'] as double,
      bucketEnd: json['bucket_end'] as double,
      count: json['count'] as int,
      percentageOfTotal: json['percentage_of_total'] as double,
    );
  }

  // Method to convert the BucketData instance to a JSON map.
  Map<String, dynamic> toJson() {
    return {
      'bucket_start': bucketStart,
      'bucket_end': bucketEnd,
      'count': count,
      'percentage_of_total': percentageOfTotal,
    };
  }
}
