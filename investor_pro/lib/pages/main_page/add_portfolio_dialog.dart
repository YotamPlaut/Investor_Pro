import 'package:flutter/material.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/widgets/custom_button.dart';

import '../../navigation/navigation_utils.dart';

class AddPortfolioDialog extends StatefulWidget {
  final Function(String)? onPortfolioCreated;

  const AddPortfolioDialog({super.key, this.onPortfolioCreated});

  @override
  _AddPortfolioDialogState createState() => _AddPortfolioDialogState();
}

class _AddPortfolioDialogState extends State<AddPortfolioDialog> {
  late TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      actionsAlignment: MainAxisAlignment.spaceBetween,
      title: Text('Add New Portfolio'),
      content: TextFormField(
        controller: _controller,
        decoration: InputDecoration(
          hintStyle: Theme.of(context)
              .textTheme
              .titleMedium
              ?.copyWith(color: AppColors.onPrimary),
          hintText: 'Enter portfolio name',
        ),
      ),
      actions: [
        CustomButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          title: 'Cancel',
        ),
        CustomButton(
          onPressed: () {
            String portfolioName = _controller.text.trim();
            if (portfolioName.isNotEmpty) {
              widget.onPortfolioCreated?.call(portfolioName);
              Navigator.of(context).pop(NavigationResult.success);
            }
          },
          title: 'Create',
        ),
      ],
    );
  }
}
