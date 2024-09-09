// // import 'package:investor_pro/models/stock_model.dart';
// //
// // class MockStockData {
// //   static List<StockModel> portfolio1 = [
// //     StockModel(
// //       ticker: 'TEVA',
// //       name: 'Teva Pharmaceutical Industries Ltd.',
// //       details:
// //       'Teva Pharmaceutical Industries Ltd. develops, manufactures, and markets generic and specialty medicines.',
// //       predictions: 'The stock is predicted to rise by 5% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'ICL',
// //       name: 'ICL Group Ltd.',
// //       details:
// //       'ICL Group Ltd. operates as a specialty minerals and chemicals company worldwide.',
// //       predictions: 'The stock is predicted to rise by 8% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'BEZQ',
// //       name: 'Bezeq The Israel Telecommunication Corp., Ltd.',
// //       details:
// //       'Bezeq The Israel Telecommunication Corp., Ltd. provides communications services in Israel.',
// //       predictions: 'The stock is predicted to rise by 7% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'ELAL',
// //       name: 'El Al Israel Airlines Ltd.',
// //       details:
// //       'El Al Israel Airlines Ltd. provides passenger and cargo transportation services.',
// //       predictions: 'The stock is predicted to rise by 6% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'ZIM',
// //       name: 'ZIM Integrated Shipping Services Ltd.',
// //       details:
// //       'ZIM Integrated Shipping Services Ltd. provides container shipping and related services.',
// //       predictions: 'The stock is predicted to rise by 10% in the next quarter.',
// //     ),
// //   ];
// //
// //   static List<StockModel> portfolio2 = [
// //     StockModel(
// //       ticker: 'PZOL',
// //       name: 'Paz Oil Company Ltd.',
// //       details:
// //       'Paz Oil Company Ltd. operates in the energy and retail sectors in Israel.',
// //       predictions: 'The stock is predicted to rise by 4% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'NICE',
// //       name: 'NICE Ltd.',
// //       details:
// //       'NICE Ltd. provides enterprise software solutions.',
// //       predictions: 'The stock is predicted to rise by 3% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'MELI',
// //       name: 'Melisron Ltd.',
// //       details:
// //       'Melisron Ltd. operates and develops commercial and office real estate properties in Israel.',
// //       predictions: 'The stock is predicted to rise by 9% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'TA35',
// //       name: 'TA-35 Index',
// //       details:
// //       'TA-35 Index is a stock market index of the 35 largest companies on the Tel Aviv Stock Exchange.',
// //       predictions: 'The stock is predicted to rise by 5% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'STRA',
// //       name: 'Strauss Group Ltd.',
// //       details:
// //       'Strauss Group Ltd. manufactures and markets food products.',
// //       predictions: 'The stock is predicted to rise by 6% in the next quarter.',
// //     ),
// //   ];
// //
// //   static List<StockModel> portfolio3 = [
// //     StockModel(
// //       ticker: 'KEN',
// //       name: 'Kenon Holdings Ltd.',
// //       details:
// //       'Kenon Holdings Ltd. engages in the development and operation of power generation facilities.',
// //       predictions: 'The stock is predicted to rise by 5% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'OPAL',
// //       name: 'Opal Balance Ltd.',
// //       details:
// //       'Opal Balance Ltd. provides renewable energy solutions.',
// //       predictions: 'The stock is predicted to rise by 7% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'OPC',
// //       name: 'OPC Energy Ltd.',
// //       details: 'OPC Energy Ltd. generates and supplies electricity.',
// //       predictions: 'The stock is predicted to rise by 4% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'GZIT',
// //       name: 'Gazit Globe Ltd.',
// //       details:
// //       'Gazit Globe Ltd. engages in the acquisition, development, and management of commercial real estate.',
// //       predictions: 'The stock is predicted to rise by 5% in the next quarter.',
// //     ),
// //     StockModel(
// //       ticker: 'LRUP',
// //       name: 'Elron Electronic Industries Ltd.',
// //       details:
// //       'Elron Electronic Industries Ltd. operates as a technology investment company.',
// //       predictions: 'The stock is predicted to rise by 3% in the next quarter.',
// //     ),
// //   ];
// // }
// //
//
// // Sample Portfolio Data
// import 'package:investor_pro/models/portfolio_model.dart';
// import 'package:investor_pro/models/stock_model.dart';
//
//
// // Sample Stock Data
// List<StockModel> mockStockList = [
//   StockModel(
//     name: 'Teva Pharmaceutical Industries',
//     ticker: 'TEVA',
//     index: 1,
//     info: 'Teva Pharmaceutical Industries is an Israeli multinational pharmaceutical company.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Bank Hapoalim',
//     ticker: 'POLI',
//     index: 2,
//     info: 'Bank Hapoalim is one of the largest banks in Israel.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Israel Chemicals',
//     ticker: 'ICL',
//     index: 3,
//     info: 'Israel Chemicals is a multinational manufacturing company that develops, produces, and markets fertilizers, metals, and other chemical products.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Nice Ltd.',
//     ticker: 'NICE',
//     index: 4,
//     info: 'Nice Ltd. is a worldwide leading provider of software solutions that manage and analyze both customer interactions and financial transactions.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
// ];
//
// List<PortfolioModel> portfolioList = [
//   PortfolioModel(
//     name: 'Tech Portfolio',
//     stocks: [mockStockList[0], mockStockList[3]], // Teva Pharmaceutical Industries and Nice Ltd.
//   ),
//   PortfolioModel(
//     name: 'Banking Portfolio',
//     stocks: [mockStockList[1]], // Bank Hapoalim
//   ),
//   PortfolioModel(
//     name: 'Chemical Portfolio',
//     stocks: [mockStockList[2]], // Israel Chemicals
//   ),
//   PortfolioModel(
//     name: 'Mixed Portfolio',
//     stocks: [mockStockList[0], mockStockList[1], mockStockList[2], mockStockList[3]], // All stocks
//   ),
// ];
//
// /// ---> mock for explore:
// // Mock Data
//
// // Trending Stocks
// List<StockModel> trendingStocks = [
//   StockModel(
//     name: 'Teva Pharmaceutical',
//     ticker: 'TEVA',
//     index: 1,
//     info: 'Teva Pharmaceutical Industries is an Israeli multinational pharmaceutical company.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Bank Leumi',
//     ticker: 'LUMI',
//     index: 2,
//     info: 'Bank Leumi is one of the largest banks in Israel.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Israel Corp',
//     ticker: 'ILCO',
//     index: 3,
//     info: 'Israel Corp is a major holding company active in a wide range of industries.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Check Point Software',
//     ticker: 'CHKP',
//     index: 4,
//     info: 'Check Point Software Technologies is a multinational provider of software and hardware products for IT security.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
// ];
//
// // Popular Funds
// List<StockModel> popularFunds = [
//   StockModel(
//     name: 'iShares MSCI Israel ETF',
//     ticker: 'EIS',
//     index: 5,
//     info: 'ETF tracking the performance of the MSCI Israel Index.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Israel Innovation Fund',
//     ticker: 'IIF',
//     index: 6,
//     info: 'Fund investing in Israeli technology and innovation companies.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'KSM TA-35 ETF',
//     ticker: 'KSM35',
//     index: 7,
//     info: 'ETF that tracks the TA-35 Index, representing the 35 largest companies in Israel.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Harel Financial Fund',
//     ticker: 'HAREL',
//     index: 8,
//     info: 'Harel Financial Fund invests in diversified assets including equities and bonds.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
// ];
//
// // Recently Added
// List<StockModel> recentlyAdded = [
//   StockModel(
//     name: 'Azrieli Group',
//     ticker: 'AZRG',
//     index: 9,
//     info: 'Azrieli Group is a leading Israeli real estate and holding company.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Elbit Systems',
//     ticker: 'ESLT',
//     index: 10,
//     info: 'Elbit Systems is an international high technology company engaged in a wide range of defense-related programs.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Strauss Group',
//     ticker: 'STRS',
//     index: 11,
//     info: 'Strauss Group is a major food and beverage manufacturer in Israel.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
//   StockModel(
//     name: 'Mizrahi Tefahot Bank',
//     ticker: 'MZTF',
//     index: 12,
//     info: 'Mizrahi Tefahot Bank is one of Israel\'s largest banks, with a strong presence in mortgage lending.',
//     numDays: 30,
//     beginDate: DateTime(2024, 7, 1),
//     endDate: DateTime(2024, 7, 31),
//   ),
// ];