import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class DateRangeSelector extends StatefulWidget {
  final Function(String) onRangeSelected;

  DateRangeSelector({required this.onRangeSelected});

  @override
  _DateRangeSelectorState createState() => _DateRangeSelectorState();
}

class _DateRangeSelectorState extends State<DateRangeSelector> {
  String currentRange = "1M";

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      value: currentRange,
      onChanged: (String? newValue) {
        if (newValue != null) {
          setState(() {
            currentRange = newValue;
            widget.onRangeSelected(newValue);
          });
        }
      },
      items: <String>['1M', '3M', '6M', '1Y', 'All']
          .map<DropdownMenuItem<String>>((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: Text(value),
        );
      }).toList(),
    );
  }
}