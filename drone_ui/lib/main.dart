import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(const MercyDroneUI());
}

class MercyDroneUI extends StatelessWidget {
  const MercyDroneUI({super.key});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => DroneFleetProvider(),
      child: MaterialApp(
        title: 'Mercy Drone Fleet',
        theme: ThemeData(
          primarySwatch: Colors.blue,
          textTheme: const TextTheme(
            displayLarge: TextStyle(fontSize: 32, color: Colors.white),
            bodyLarge: TextStyle(fontSize: 24, color: Colors.white),
          ),
          scaffoldBackgroundColor: Colors.black87,
        ),
        home: const DroneDashboard(),
      ),
    );
  }
}

class DroneFleetProvider extends ChangeNotifier {
  List<Drone> drones = List.generate(33, (i) => Drone(id: i + 1));
  
  void updateDrone(int id, {LatLng? position, int? battery, String? status}) {
    final drone = drones.firstWhere((d) => d.id == id);
    if (position != null) drone.position = position;
    if (battery != null) drone.battery = battery;
    if (status != null) drone.status = status;
    notifyListeners();
  }
}

class Drone {
  final int id;
  LatLng position = const LatLng(43.65, -79.38); // Toronto default
  int battery = 100;
  String status = "Nominal";
  
  Drone({required this.id});
}

class DroneDashboard extends StatelessWidget {
  const DroneDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mercy Drone Fleet — Joy Delivery Active'),
        centerTitle: true,
      ),
      body: Consumer<DroneFleetProvider>(
        builder: (context, provider, child) {
          return Column(
            children: [
              Expanded(
                child: GoogleMap(
                  initialCameraPosition: const CameraPosition(
                    target: LatLng(43.65, -79.38),
                    zoom: 12,
                  ),
                  markers: provider.drones.map((drone) {
                    return Marker(
                      markerId: MarkerId('drone_${drone.id}'),
                      position: drone.position,
                      infoWindow: InfoWindow(title: 'Drone ${drone.id} — ${drone.battery}% — ${drone.status}'),
                    );
                  }).toSet(),
                ),
              ),
              Container(
                padding: const EdgeInsets.all(16),
                color: Colors.blue[900],
                child: Column(
                  children: [
                    Text('Fleet Status — ${provider.drones.length} Drones', style: const TextStyle(fontSize: 28)),
                    const SizedBox(height: 8),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        ElevatedButton(
                          onPressed: () {},  // Voice command trigger
                          child: const Text('Deploy MercyGel Drop', style: TextStyle(fontSize: 24)),
                        ),
                        ElevatedButton(
                          onPressed: () {},  // Formation switch
                          child: const Text('Trinity Formation', style: TextStyle(fontSize: 24)),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
