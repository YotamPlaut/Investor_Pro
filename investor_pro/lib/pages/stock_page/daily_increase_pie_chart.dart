import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:investor_pro/models/statistics/daily_increase_buckets_model.dart';
import 'package:investor_pro/theme.dart';

class DailyIncreasePieChart extends StatelessWidget {
  final List<BucketDataModel> data;

  const DailyIncreasePieChart({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: data
                .map((bucket) => Text(
                      "• ${bucket.count} days. ${bucket.bucketStart.toStringAsFixed(2)} to ${bucket.bucketEnd.toStringAsFixed(2)}: ${bucket.percentageOfTotal.toStringAsFixed(1)}%",
                      style: const TextStyle(fontSize: 20),
                    ))
                .toList(),
          ),
        ),
        SizedBox(
          height: 250,
          child: PieChart(PieChartData(
            sections: data.map((bucket) {
              final isLarge = bucket.percentageOfTotal > 20;
              return PieChartSectionData(
                showTitle: true,
                titlePositionPercentageOffset: 0.7,
                color: isLarge ? AppColors.secondaryVariant : AppColors.secondary,
                value: bucket.percentageOfTotal,
                title: '${bucket.percentageOfTotal.toStringAsFixed(1)}%',
                radius: 120,
                titleStyle: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: const Color(0xffffffff),
                ),
              );
            }).toList(),
            centerSpaceRadius: 0,
            sectionsSpace: 3,
          )),
        ),
      ],
    );
  }
}
