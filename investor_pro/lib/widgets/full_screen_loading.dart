import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:investor_pro/theme.dart';

class LoadingOverlay extends StatelessWidget {
  final bool isLoading;
  final Widget child;

  const LoadingOverlay({
    super.key,
    required this.isLoading,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        child,
        if (isLoading)
          Positioned.fill(
            child: ModalBarrier(
              color: Colors.black.withOpacity(0.4),
              dismissible: false,
            ),
          ),
        if (isLoading)
          const Center(
            child: SpinKitSpinningLines(
              color: AppColors.secondary,
              size: 50.0,
            ),
          ),
      ],
    );
  }
}
