import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'data.dart';

Future<Post> fetchPost(double currentPage) async {
  final response = await http.get(get_request + artists[currentPage.round()]);
  print(get_request + artists[currentPage.round()]);
  if (response.statusCode == 200) {
    print('Success');
    return Post.fromJson(json.decode(response.body));
  } else {
    // If that call was not successful, throw an error.
    throw Exception('Failed to load post');
  }
}

class Post {
  final bool success;
  final String predictions;

  Post({this.success, this.predictions});

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(success: json['success'], predictions: json['predictions']);
  }
}

class Rap extends StatelessWidget {
  final Future<Post> post;
  final double currentPage;

  Rap({Key key, @required this.currentPage, this.post}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    print(get_request);
    return Scaffold(
        appBar: AppBar(
            backgroundColor: text_colors[currentPage.round()],
            leading: new IconButton(
                icon: new Icon(Icons.arrow_back),
                onPressed: () {
                  Navigator.pop(context, true);
                })),
        body: Container(
            color: Colors.white,
            child: Center(
              child: FutureBuilder<Post>(
                future: fetchPost(currentPage),
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    return SingleChildScrollView(
                      padding: const EdgeInsets.only(
                          left: 40.0, right: 40.0, top: 40.0, bottom: 0.0),
                      child: Text(snapshot.data.predictions,
                          style: TextStyle(
                            decorationColor: Colors.white,
                            color: Colors.black,
                            fontSize: 15.0,
                            fontFamily: "Roboto",
                            letterSpacing: 1.0,
                          )),
                    );
                  } else if (snapshot.hasError) {
                    return Text("${snapshot.error}");
                  }
                  return CircularProgressIndicator();
                },
              ),
            )));
  }
}
