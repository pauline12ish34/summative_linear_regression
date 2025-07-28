import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class PredictionPage extends StatefulWidget {
  const PredictionPage({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _PredictionPageState createState() => _PredictionPageState();
}

class _PredictionPageState extends State<PredictionPage> {
  // Controllers for all 20 input fields
  final List<TextEditingController> _controllers = List.generate(
    20,
    (index) => TextEditingController(),
  );

  String _predictionResult = '';
  bool _isLoading = false;

  // All 20 feature names exactly matching your API model
  final List<String> _featureNames = [
    'MonsoonIntensity',
    'TopographyDrainage',
    'RiverManagement',
    'Deforestation',
    'Urbanization',
    'ClimateChange',
    'DamsQuality',
    'Siltation',
    'AgriculturalPractices',
    'Encroachments',
    'IneffectiveDisasterPreparedness',
    'DrainageSystems',
    'CoastalVulnerability',
    'Landslides',
    'Watersheds',
    'DeterioratingInfrastructure',
    'PopulationScore',
    'WetlandLoss',
    'InadequatePlanning',
    'PoliticalFactors',
  ];

  // Helper text for each field
  final List<String> _fieldHints = [
    'Scale 1-10 (Higher = more rain)',
    'Scale 1-10 (Higher = better drainage)',
    'Scale 1-10 (Higher = better management)',
    'Scale 1-10 (Higher = more deforestation)',
    'Scale 1-10 (Higher = more urbanized)',
    'Scale 1-10 (Higher = more climate impact)',
    'Scale 1-10 (Higher = better dam quality)',
    'Scale 1-10 (Higher = more silt buildup)',
    'Scale 1-10 (Higher = more intensive)',
    'Scale 1-10 (Higher = more encroachment)',
    'Scale 1-10 (Higher = less preparedness)',
    'Scale 1-10 (Higher = better drainage)',
    'Scale 1-10 (Higher = more vulnerable)',
    'Scale 1-10 (Higher = more landslide risk)',
    'Scale 1-10 (Higher = more watersheds)',
    'Scale 1-10 (Higher = worse infrastructure)',
    'Scale 1-10 (Higher = denser population)',
    'Scale 1-10 (Higher = more wetland loss)',
    'Scale 1-10 (Higher = worse planning)',
    'Scale 1-10 (Higher = more political risk)',
  ];

  Future<void> _predictFlood() async {
    setState(() {
      _isLoading = true;
      _predictionResult = '';
    });

    // Prepare input data
    Map<String, dynamic> inputData = {};
    for (int i = 0; i < _featureNames.length; i++) {
      inputData[_featureNames[i]] = double.tryParse(_controllers[i].text) ?? 0.0;
    }

    try {
      final response = await http.post(
        // https://summative-linear-regression.onrender.com
        // Uri.parse('http://10.0.2.2:8000/predict'), // For emulator
        Uri.parse('http://10.0.2.2:8000/predict'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(inputData),
      );

      if (response.statusCode == 200) {
        final prediction = jsonDecode(response.body)['predicted_flood_probability'];
        setState(() {
          _predictionResult = '${(prediction * 100).toStringAsFixed(1)}% flood probability';
        });
      } else {
        setState(() {
          _predictionResult = 'Error: ${response.statusCode}\n${response.body}';
        });
      }
    } catch (e) {
      setState(() {
        _predictionResult = 'API Connection Failed\n${e.toString()}';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  void dispose() {
    // Clean up all controllers
    for (var controller in _controllers) {
      controller.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Flood Risk Prediction',style: TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.bold,
    color: Colors.white,
    letterSpacing: 1.2,
  ),
),
        backgroundColor: Colors.blue[800],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            children: [
              // Input fields for all 20 features
              for (int i = 0; i < _featureNames.length; i++)
                Padding(
                  padding: const EdgeInsets.only(bottom: 12.0),
                  child: TextField(
                    controller: _controllers[i],
                    keyboardType: TextInputType.numberWithOptions(decimal: true),
                    decoration: InputDecoration(
                      labelText: _featureNames[i],
                      hintText: _fieldHints[i],
                      border: OutlineInputBorder(),
                      filled: true,
                      fillColor: Colors.grey[100],
                    ),
                  ),
                ),
              
              SizedBox(height: 20),
              
              // Predict button
              ElevatedButton(
                onPressed: _isLoading ? null : _predictFlood,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue[800],
                  padding: EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
               
                child: _isLoading
                    ? CircularProgressIndicator(color: Colors.white)
                    : Text(
                        'PREDICT FLOOD RISK',
                        style: TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.bold,
    color: Colors.white,
    letterSpacing: 1.2,
  ),

                      ),
                      
              ),
              
              SizedBox(height: 24),
              
              // Output display
              Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: _predictionResult.contains('%')
                      ? _getColorForPrediction(_predictionResult)
                      : Colors.grey[200],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Center(
                  child: Text(
                    _predictionResult.isEmpty
                        ? 'Enter values and predict'
                        : _predictionResult,
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: _predictionResult.contains('%') 
                          ? Colors.white 
                          : Colors.black,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getColorForPrediction(String result) {
    if (!result.contains('%')) return Colors.grey;
    final percentage = double.tryParse(result.split('%')[0]) ?? 0;
    if (percentage < 30) return Colors.green;
    if (percentage < 60) return Colors.orange;
    return Colors.red;
  }
}