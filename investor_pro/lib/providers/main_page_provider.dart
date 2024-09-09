import 'package:flutter/material.dart';
import 'package:investor_pro/models/portfolio_model.dart';
import 'package:investor_pro/models/user_model.dart';

// import 'package:investor_pro/models/portfolio_model.dart';
// import 'package:investor_pro/services/api_service.dart';

class MainPageProvider with ChangeNotifier {
  late String userId;
  List<PortfolioModel> portfolios = [];
  bool isLoading = false;

  MainPageProvider(this.userId) {
    _init(userId);
  }

  Future<void> _init(String userId) async {
    isLoading = true;
    notifyListeners();

    await _getUser();
    await getPortfolios(userId);

    isLoading = false;
    notifyListeners();
  }

  Future<void> _getUser() async {
    try {
      isLoading = true;
      notifyListeners();
      // Fetch user data from API
      // user = await ApiService.fetchUser();
    } catch (e) {
      // Handle error
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> getPortfolios(String userId) async {
    try {
      isLoading = true;
      notifyListeners();
      portfolios = await PortfolioModel.fetchPortfolios(userId);
      notifyListeners();
    } catch (e) {
      // Handle error
      print(e);
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> addPortfolio(String userId, String portfolioName) async {
    try {
      isLoading = true;
      notifyListeners();
      await PortfolioModel.addPortfolio(userId, portfolioName);
    } catch (e) {
      debugPrint(e.toString());
      rethrow;
    } finally {
      await getPortfolios(userId);
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> deletePortfolio(String userId, String portfolioName) async {
    try {
      isLoading = true;
      notifyListeners();
      await PortfolioModel.deletePortfolio(userId, portfolioName);
    } catch (e) {
      debugPrint(e.toString());
      rethrow;
    } finally {
      await getPortfolios(userId);
      isLoading = false;
      notifyListeners();
    }
  }

  Future<void> removeStockFromPortfolio(
      String userId, String portfolioId, String stockId) async {
    try {
      isLoading = true;
      notifyListeners();
      await PortfolioModel.removeStockFromPortfolio(
          userId, portfolioId, stockId);
    } catch (e) {
      debugPrint(e.toString());
      rethrow;
    } finally {
      await getPortfolios(userId);
      isLoading = false;
      notifyListeners();
    }
  }
}
