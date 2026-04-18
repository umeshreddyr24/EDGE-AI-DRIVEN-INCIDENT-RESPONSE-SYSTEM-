# Edge AI-Driven Incident Response System
**Team Goal Getters**

The Edge AI-Driven Incident Response System is an intelligent monitoring solution designed for real-time hazard detection and visual verification. By integrating low-power IoT hardware with high-level Python processing, the system provides an automated security hub capable of sub-second response times.

## ⚠️ Problem Statement

**Human Error**: Manual monitoring is highly susceptible to human error.

**Response Delays**: Manual systems create dangerous delays in emergency situations.

### Key Risks:
- Slow response to fires and gas leaks
- Lack of real-time visual confirmation for remote operators
- Absence of automated incident logging for forensic review

## ✔ Solution

An automated Security Hub that combines multi-sensor telemetry with live visual verification.

**Comprehensive Detection**: Monitors for Gas, Fire, Water, and Heat.

**High Performance**: Achieves sub-second sensor-to-alert latency.

**Evidence Retention**: Features a remote dashboard with an automated evidence log.

## 🛠 System Architecture

### Hardware: Edge Controller
- **Arduino**: Handles real-time sensor collection and local alarm logic
- **Connectivity**: Packages all sensor values into JSON and sends POST requests via WiFi to a central server

#### Sensors Integration:
- **DHT11**: Monitoring of Temperature and Humidity
- **Gas/Flame Sensors**: Detection of hazardous leaks and fire
- **Water Sensor**: Continuous flooding and leak monitoring

### Software: Backend & Computer Vision
- **Python Flask Server**: Acts as the central "brain," receiving data and hosting the web dashboard
- **Live Video Stream**: OpenCV manages a continuous camera feed embedded in the UI
- **ROI Highlighting**: During an alarm, the system draws a red bounding box on the frame labeled **CRITICAL** for instant context
- **Evidence Logging**: Automatically captures timestamped snapshots and saves them to a history folder

## ⚙️ Technical Specifications

| Feature | Specification |
|---------|---------------|
| Logic Threshold (Gas) | > 400 ppm |
| Logic Threshold (Temp) | > 60 °C |
| Alert Latency | Sub-second |
| Cloud Dependency | Zero (Fully Edge-Native) |
| Data Format | JSON via WiFi POST |

## 🚀 Future Scope

- **Advanced AI**: Integration of YOLO-based object and person detection
- **Notifications**: Implementation of Cloud SMS and Email alert systems
- **Scalability**: Development of a multi-node sensor network for large-scale facilities
- **Predictive Analytics**: ML-powered anomaly detection for predictive alerting

## 👥 Contributors

- **Umesh Reddy**: Hardware & Software & Sensor Integration
- **Hakuto**: Software Development
- **Yurin**: Software Development
- **Thao**: Sensor Specialist
- **Dat**: Sensor Specialist
