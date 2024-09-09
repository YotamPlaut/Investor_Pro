import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SessionMgr extends ChangeNotifier {
  String? _userId;

  String? get userId => _userId;

  Future<void> loadSession() async {
    final prefs = await SharedPreferences.getInstance();
    _userId = prefs.getString('user_id');
    notifyListeners();
  }

  Future<void> saveSession(String userId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('user_id', userId);
    _userId = userId;
    notifyListeners();
  }

  Future<void> clearSession() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('user_id');
    _userId = null;
    notifyListeners();
  }
}