# Edge AI-Driven Incident Response System
### [cite_start]**Developed by Team Goal Getters** [cite: 1]

[cite_start]An intelligent, edge-native security hub that integrates multi-sensor data with real-time computer vision to automate incident detection and visual verification[cite: 3, 4].

---

## ⚠ **The Problem**
* [cite_start]**Human Error**: Manual monitoring is highly prone to errors[cite: 22].
* [cite_start]**Response Delays**: Reliance on manual checks creates dangerous delays during emergencies[cite: 22].
* **Key Risks**: 
    * [cite_start]Slow response to fires and hazardous gas leaks[cite: 24].
    * [cite_start]Lack of real-time visual confirmation for remote operators[cite: 25].
    * [cite_start]Absence of automated incident logging for forensic review[cite: 26].

## ✔ **The Solution**
* [cite_start]**Automated Security Hub**: Combines multi-sensor data with live visual verification[cite: 28].
* [cite_start]**High Performance**: Achieves sub-second sensor-to-alert latency[cite: 31].
* [cite_start]**Remote Oversight**: Includes a web-based dashboard with an evidence log[cite: 32].

---

## 🛠 **System Architecture**

### **Hardware: Edge Controller**
[cite_start]The system uses an **Arduino** as the local controller for real-time responsiveness[cite: 35, 36]:
* **Sensor Suite**: 
    * [cite_start]**DHT11**: Monitoring Temperature and Humidity[cite: 41, 42, 43].
    * [cite_start]**Gas/Flame Sensors**: Detecting hazardous leaks and fire[cite: 44, 45, 47].
    * [cite_start]**Water Sensor**: Monitoring for flooding and leaks[cite: 48, 49, 50].
* [cite_start]**Local Alerts**: Instantly triggers a physical buzzer and LED when thresholds are met[cite: 40, 53].
* [cite_start]**Communication**: Packages data into JSON and sends POST requests via WiFi to the central server[cite: 39, 58].

### **Software: Backend & AI**
* [cite_start]**Flask Web Server**: A Python-based "brain" that receives data, hosts the dashboard, and manages alert states[cite: 60, 61].
* **OpenCV Computer Vision**: 
    * [cite_start]Manages a live camera feed for visual verification[cite: 68].
    * [cite_start]Automatically captures timestamped snapshots during an alarm[cite: 69].
    * [cite_start]Highlights the **Region of Interest (ROI)** with a red bounding box labeled **CRITICAL** during incidents[cite: 71, 72].
* [cite_start]**Evidence Logging**: Saves snapshots to a `/history` folder, retaining the last 5 critical events[cite: 74, 75].

---

## ⚙ **Operational Specifications**
* **Alarm Thresholds**: 
    * [cite_start]Gas Level > 400 ppm[cite: 52].
    * [cite_start]Temperature > 60 °C[cite: 53].
* **Dashboard Features**:
    * [cite_start]Live telemetry for Temperature, Humidity, and Gas[cite: 79, 80].
    * [cite_start]Embedded live OpenCV video stream[cite: 81, 82].
    * [cite_start]Browser-based audio alarm using Web Audio API[cite: 85, 86].
    * [cite_start]Incident history view for the last 5 critical snapshots[cite: 83, 84].

---

## 🚀 **Future Scope**
* [cite_start]Implementation of **YOLO-based** object and person detection[cite: 112].
* [cite_start]Integration of **Cloud SMS and Email** notifications[cite: 113].
* [cite_start]Scaling to a **multi-node sensor network** for large facilities[cite: 114].
* [cite_start]**ML-powered anomaly detection** for predictive alerts[cite: 115].

---

## [cite_start]👥 **The Team: Goal Getters** [cite: 1]
* [cite_start]**Umesh Reddy**: Hardware & Software & Sensor[cite: 9, 10, 11].
* [cite_start]**Hakuto**: Software[cite: 7, 8].
* [cite_start]**Yurin**: Software[cite: 12, 13].
* [cite_start]**Thao**: Sensor[cite: 14, 15].
* [cite_start]**Dat**: Sensor[cite: 16, 17].

---
[cite_start]**Thank you!!** [cite: 118]
