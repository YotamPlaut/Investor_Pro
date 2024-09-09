import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:investor_pro/theme.dart';

class CustomAppBar extends StatelessWidget implements PreferredSizeWidget {
  const CustomAppBar({
    super.key,
    required this.title,
    this.actions,
    this.showBackButton = false,
    this.transparentBackGround = false,
  });

  final String title;
  final List<Widget>? actions;
  final bool showBackButton;
  final bool transparentBackGround;

  @override
  Widget build(BuildContext context) {
    return AppBar(
      automaticallyImplyLeading: false,
      leading: showBackButton
          ? IconButton(
        icon: Icon(Icons.arrow_back),
        onPressed: () {
          GoRouter.of(context).pop();
        },
      ) : null,
      title: Text(
        title,
        style: Theme.of(context)
            .textTheme
            .headlineLarge
            ?.copyWith(color: Colors.white, fontSize: 25),
      ),
      centerTitle: true,
      backgroundColor: transparentBackGround ? Colors.transparent : AppColors.primary , // Set the background color
      actions: actions,
    );
  }

  @override
  Size get preferredSize => Size.fromHeight(kToolbarHeight);
}
