import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:investor_pro/api_gateway.dart';

UserModel userModelFromJson(String str) => UserModel.fromJson(json.decode(str));

String userModelToJson(UserModel data) => json.encode(data.toJson());

class UserModel {
  String username;
  String email;
  String password;

  UserModel({
    required this.username,
    required this.email,
    required this.password,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) => UserModel(
        username: json["username"],
        email: json["email"],
        password: json["password"],
      );

  Map<String, dynamic> toJson() => {
        "username": username,
        "email": email,
        "password": password,
      };

  static const String baseUrl = ApiGateway.baseUrl;

  static Future<String> registerUser(UserModel user) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/create-new-account'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(user.toJson()),
      );

      if (response.statusCode == 200) {
        return response.body;
      } else {
        throw http.ClientException(
            'Failed to register user: ${response.reasonPhrase}');
      }
    } on http.ClientException catch (e) {
      throw http.ClientException('Network error: ${e.message}');
    } on TimeoutException {
      throw http.ClientException('Request timed out');
    } catch (e) {
      throw http.ClientException('Unexpected error: $e');
    }
  }

  static Future<String> login(String username, String password) async {
    Map<String, String> loginData = {
      'username': username,
      'password': password,
    };

    String loginJsonString = jsonEncode(loginData);

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login'),
        headers: {'Content-Type': 'application/json'},
        body: loginJsonString,
      );


      if (response.statusCode == 200) {
        return response.body;
      } else {
        throw http.ClientException(
            'Failed to login user: ${response.reasonPhrase}');
      }
    } on http.ClientException catch (e) {
      throw http.ClientException('Network error: ${e.message}');
    } on TimeoutException {
      throw http.ClientException('Request timed out');
    } catch (e) {
      throw http.ClientException('Unexpected error: $e');
    }
  }
}
