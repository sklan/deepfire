import 'package:flutter/material.dart';

List<String> images = [
  "assets/image_06.png",
  "assets/image_05.png",
  "assets/image_04.png",
  "assets/image_03.png",
  "assets/image_02.png",
  "assets/image_01.png",
];

List<String> artists = [
  'asaprocky',
  'jcole',
  'tyler',
  'snoop',
  'kanye',
  'eminem',
];

List<Color> text_colors = [
  Color(0xFF85BCBD),
  Color(0xFF8E4D37),
  Color(0xFFC66B43),
  Color(0xFF2EADDA),
  Color(0xFFE0CD57),
  Color(0xFF000000)
];

var cardAspectRatio = 5.0 / 7.0 - .15;
var widgetAspectRatio = cardAspectRatio * 1.25;

String get_request = 'http://127.0.0.1/predict?artist=';
