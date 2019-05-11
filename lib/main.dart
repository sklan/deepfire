import 'package:flutter/material.dart';

import 'cardscrollwidget.dart';
import 'data.dart';
import 'rap.dart';

void main() => runApp(MaterialApp(
      home: MyApp(),
      debugShowCheckedModeBanner: false,
    ));

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => new _MyAppState();
}

class _MyAppState extends State<MyApp> {
  var currentPage = images.length - 1.0;

  @override
  Widget build(BuildContext context) {
    PageController controller = PageController(initialPage: images.length - 1);
    controller.addListener(() {
      setState(() {
        currentPage = controller.page;
      });
    });
    return Container(
      child: Scaffold(
        backgroundColor: Colors.white,
        body: SingleChildScrollView(
          child: Column(
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.only(
                    left: 12.0, right: 12.0, top: 180.0, bottom: 0.0),
              ),
              Stack(
                children: <Widget>[
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Text("DEEPFIRE",
                          style: TextStyle(
                            color: text_colors[currentPage.round()],
                            fontSize: 71.0,
                            fontFamily: "Calibre-Semibold",
                            letterSpacing: 4.0,
                          )),
                    ],
                  ),
                  Padding(
                      padding: const EdgeInsets.only(
                          left: 50.0, right: 0.0, top: 25.0, bottom: 0.0),
                      child: CardScrollWidget(currentPage)),
                  Positioned.fill(
                      child: InkWell(
                    child: PageView.builder(
                      itemCount: images.length,
                      controller: controller,
                      reverse: true,
                      itemBuilder: (context, index) {
                        return Container();
                      },
                    ),
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                            builder: (context) =>
                                Rap(currentPage: currentPage)),
                      );
                    },
                  ))
                ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Flexible(
                      child: Text(
                          "TAP ON " +
                              artists[currentPage.round()].toUpperCase(),
                          style: TextStyle(
                            color: text_colors[currentPage.round()],
                            fontSize: 25.0,
                            fontFamily: "Calibre-Semibold",
                            letterSpacing: 4.0,
                          ))),
                ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Text("TO GENERATE",
                      style: TextStyle(
                        color: text_colors[currentPage.round()],
                        fontSize: 25.0,
                        fontFamily: "Calibre-Semibold",
                        letterSpacing: 4.0,
                      )),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
