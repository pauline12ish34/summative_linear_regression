import 'package:flutter/material.dart';
import 'package:mobo_flood_app/prediction_page.dart';



void main() {
  runApp(FloodPredictionApp());
}

class FloodPredictionApp extends StatelessWidget {
  const FloodPredictionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flood Prediction App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: HomeScreen(), // Default home screen
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Rwanda Flood Prediction'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome to Flood Prediction App',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Navigate to PredictionPage
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => PredictionPage()),
                );
              },
              child: Text('Start Prediction'),
            ),
          ],
        ),
      ),
    );
  }
}