import 'package:flutter/material.dart';
import 'package:flutter_slidable/flutter_slidable.dart';
import 'package:investor_pro/navigation/app_routes.dart';
import 'package:investor_pro/session_manager.dart';
import 'package:investor_pro/theme.dart';
import 'package:investor_pro/models/portfolio_model.dart';
import 'package:investor_pro/widgets/custom_button.dart';
import 'package:provider/provider.dart';

class PortfolioCard extends StatefulWidget {
  final PortfolioModel portfolio;
  final VoidCallback onDelete; // Callback to delete the portfolio
  final Function onRemoveStock;

  const PortfolioCard(
      {super.key,
      required this.portfolio,
      required this.onDelete,
      required this.onRemoveStock});

  @override
  _PortfolioCardState createState() => _PortfolioCardState();
}

class _PortfolioCardState extends State<PortfolioCard>
    with SingleTickerProviderStateMixin {
  bool _isExpanded = false;
  late AnimationController _controller;
  late Animation<double> _expandAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    _expandAnimation = CurvedAnimation(
      parent: _controller,
      curve: Curves.fastOutSlowIn,
    );
  }

  void _toggleExpansion() {
    setState(() {
      _isExpanded = !_isExpanded;
      if (_isExpanded) {
        _controller.forward();
      } else {
        _controller.reverse();
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return _isExpanded
        ? _buildCardContent() // Render without Slidable if expanded
        : Slidable(
            key: ValueKey(widget.portfolio.name),
            startActionPane: ActionPane(
              motion: const StretchMotion(),
              extentRatio: 0.25,
              children: [
                Expanded(
                  child: GestureDetector(
                    onTap: () {
                      widget.onDelete();
                    },
                    child: Container(
                      height: 55, // Custom height for the red area
                      decoration: BoxDecoration(
                        color: Colors.red,
                        borderRadius: BorderRadius.circular(10),
                      ),
                      padding: const EdgeInsets.symmetric(horizontal: 30),
                      child: const Icon(
                        Icons.delete,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            child: _buildCardContent(), // Render with Slidable if not expanded
          );
  }

  Widget _buildCardContent() {
    final user = Provider.of<SessionMgr>(context, listen: false).userId ?? '';
    return GestureDetector(
      onTap: _toggleExpansion,
      child: Card(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
        child: Column(
          children: [
            ListTile(
              title: Text(
                widget.portfolio.name,
                style: TextStyle(color: AppColors.onPrimary),
              ),
              trailing: widget.portfolio.stocks.isEmpty
                  ? null
                  : Icon(
                      _isExpanded ? Icons.expand_less : Icons.expand_more,
                      color: AppColors.secondary,
                    ),
            ),
            SizeTransition(
              sizeFactor: _expandAnimation,
              child: Column(
                children: List.generate(
                  widget.portfolio.stocks.length,
                  (index) {
                    final stockName =
                        widget.portfolio.stocks.values.toList()[index];
                    return Column(
                      children: [
                        if (index == 0)
                          const Divider(
                            thickness: 0.3,
                          ),
                        ListTile(
                          title: Text(
                            stockName.toString(),
                            style: const TextStyle(color: AppColors.onPrimary),
                          ),
                          onTap: () => NavigationHelper.navigateTo(
                            context,
                            AppRoutes.stock,
                            data: stockName,
                          ),
                          onLongPress: () {
                            showDeleteConfirmation(
                                context,
                                widget.portfolio.name,
                                () => widget.onRemoveStock(
                                    user,
                                    widget.portfolio.name,
                                    widget.portfolio.stocks.keys
                                        .toList()[index]));
                          },
                        ),
                        if (index != widget.portfolio.stocks.length - 1)
                          const Divider(
                            thickness: 0.3,
                          ),
                      ],
                    );
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void showDeleteConfirmation(
      BuildContext context, String portName, Function onDelete) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Confirm Deletion'),
          content: Text(
              'Are you sure you want to delete this stock from \'$portName\' portfolio?'),
          actions: <Widget>[
            CustomButton(
              title: 'Cancel',
              onPressed: () {
                Navigator.of(context).pop(); // Close the dialog
              },
            ),
            CustomButton(
              title: 'Delete',
              onPressed: () {
                onDelete();
                Navigator.of(context).pop(); // Close the dialog after handling
              },
            ),
          ],
        );
      },
    );
  }
}
