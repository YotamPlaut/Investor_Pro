import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'dart:math';

class NormalDistributionChart extends StatelessWidget {
  final double mean;
  final double stdDev;

  const NormalDistributionChart({
    Key? key,
    required this.mean,
    required this.stdDev,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final data = getNormalDistributionData(
        mean, stdDev, 100); // Generate 100 data points

    return SizedBox(
      height: 250,
      child: LineChart(
        LineChartData(
          gridData: FlGridData(show: false),
          titlesData: FlTitlesData(show: false),
          borderData: FlBorderData(show: false),
          lineBarsData: [
            LineChartBarData(
              spots: data,
              isCurved: true,
              // Smooth the line
              //colors: [Colors.blue],
              barWidth: 2,
              isStrokeCapRound: true,
              dotData: FlDotData(show: false),
              // Do not show the dots
              belowBarData: BarAreaData(show: false),
            )
          ],
        ),
      ),
    );
  }

  List<FlSpot> getNormalDistributionData(
      double mean, double stdDev, int numPoints) {
    final List<FlSpot> points = [];
    final double start = mean - 4 * stdDev;
    final double end = mean + 4 * stdDev;
    final double step = (end - start) / numPoints;

    for (double x = start; x <= end; x += step) {
      final double y = (1 / (stdDev * sqrt(2 * pi))) *
          exp(-0.5 * pow((x - mean) / stdDev, 2));
      points.add(FlSpot(x, y));
    }

    return points;
  }
}
