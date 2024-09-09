import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:investor_pro/models/price_data_model.dart';
import 'package:investor_pro/theme.dart';
import 'dart:math';

class StockPriceChart extends StatefulWidget {
  final List<PriceDataModel>? data;
  final String dateRange;

  const StockPriceChart(
      {super.key, required this.data, required this.dateRange});

  @override
  State<StockPriceChart> createState() => _StockPriceChartState();
}

class _StockPriceChartState extends State<StockPriceChart> {
  int getXAxisInterval(String range, int length) {
    switch (range) {
      case '1M':
        return max(1, length ~/ 60);
      case '3M':
        return max(1, length ~/ 15);
      case '6M':
        return max(1, length ~/ 10);
      case '1Y':
        return max(1, length ~/ 12);
      default:
        return max(1, length ~/ 12);
    }
  }

  @override
  Widget build(BuildContext context) {
    final data = widget.data;
    if (data == null || data.isEmpty) {
      return const SizedBox(
          height: 320, child: Center(child: Text('No data available')));
    }

    final currentDate = DateTime.now();
    List<FlSpot> historicalSpots = [];
    List<FlSpot> futureSpots = [];

    for (int i = 0; i < data.length; i++) {
      DateTime date = DateTime.parse(data[i].date);
      double price = data[i].closePrice;
      FlSpot spot = FlSpot(i.toDouble(), price);
      if (date.isBefore(currentDate)) {
        historicalSpots.add(spot);
      } else {
        futureSpots.add(spot);
      }
    }

    double minX = 0;
    double maxX = data.length.toDouble() - 1;
    double minY = data.map((e) => e.closePrice).reduce(min) * 0.9;
    double maxY = data.map((e) => e.closePrice).reduce(max) * 1.1;
    int xAxisInterval = getXAxisInterval(widget.dateRange, data.length);

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
              color: Colors.grey.withOpacity(0.2),
              spreadRadius: 5,
              blurRadius: 7,
              offset: const Offset(0, 3)),
        ],
      ),
      padding: const EdgeInsets.all(12),
      child: SizedBox(
        height: 320,
        child: LineChart(
          LineChartData(
            gridData: const FlGridData(
                show: true,
                drawVerticalLine: true,
                horizontalInterval: 30,
                verticalInterval: 10),
            titlesData: FlTitlesData(
              bottomTitles: AxisTitles(
                sideTitles: SideTitles(
                  showTitles: true,
                  reservedSize: 20,
                  //interval: xAxisInterval.toDouble(),
                  getTitlesWidget: (value, meta) {
                    var index = value.toInt();
                    if (index % xAxisInterval == 0 && index < data.length) {
                      return SideTitleWidget(
                        axisSide: meta.axisSide,
                        space: 8.0,
                        child: Text(
                          DateFormat('MMM-dd')
                              .format(DateTime.parse(data[index].date)),
                          style: const TextStyle(
                              color: Color(0xff68737d),
                              fontWeight: FontWeight.bold,
                              fontSize: 9),
                        ),
                      );
                    }
                    return const Text('');
                  },
                ),
              ),
              leftTitles: AxisTitles(
                sideTitles: SideTitles(
                  showTitles: true,
                  interval: 100,
                  getTitlesWidget: (value, meta) => SideTitleWidget(
                    axisSide: meta.axisSide,
                    space: 10,
                    child: Text(
                      value.truncate().toString(),
                      style: const TextStyle(
                          color: Color(0xff67727d),
                          fontWeight: FontWeight.normal,
                          fontSize: 10),
                      textAlign: TextAlign.left,
                    ),
                  ),
                  reservedSize: 40,
                ),
              ),
            ),
            borderData: FlBorderData(
                show: true,
                border: Border.all(color: const Color(0xff37434d), width: 1)),
            minX: minX,
            maxX: maxX,
            minY: minY,
            maxY: maxY,
            lineBarsData: [
              LineChartBarData(
                spots: historicalSpots,
                isCurved: true,
                color: AppColors.secondaryVariant,
                barWidth: 1.5,
                isStrokeCapRound: true,
                belowBarData: BarAreaData(
                  show: true,
                  gradient: LinearGradient(
                    colors: [
                      Colors.blueAccent.withOpacity(0.3),
                      Colors.blueAccent.withOpacity(0.0)
                    ],
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                  ),
                ),
                dotData: const FlDotData(show: false),
              ),
              LineChartBarData(
                spots: futureSpots,
                isCurved: true,
                color: Colors.redAccent,
                // Different color for future data
                barWidth: 1.5,
                isStrokeCapRound: true,
                belowBarData: BarAreaData(
                  show: true,
                  gradient: LinearGradient(
                    colors: [
                      Colors.red.withOpacity(0.3),
                      Colors.red.withOpacity(0.0)
                    ],
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                  ),
                ),
                dotData: const FlDotData(show: false),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
