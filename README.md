# 🚁 Drone Intrusion Detection System with 3D Demonstration

A comprehensive **Drone Intrusion Detection & Prevention System (IDS/IPS)** using **ArduPilot SITL + QGroundControl**, with real-time attack simulation, telemetry logging, anomaly detection, and automated defense mechanisms.

---

## 📌 Project Overview

This project demonstrates how drones can be protected from malicious intrusions in a simulated environment. It combines **simulation, attack emulation, real-time visualization, machine learning, and automated defense strategies** to build a complete intrusion detection system for drones.

---

## 🔧 Project Components

### 1. Observation of Drone Behaviour

* **ArduPilot SITL** simulates drone hardware (GPS, motors, sensors).
* **QGroundControl** provides telemetry, maps, altitude, and control.
* Observe drone responses to commands in **2D/3D visualization** without real hardware.

### 2. Manipulation & Attack Simulation

* Simulate both **legitimate user commands** and **malicious intrusions**.
* Attack vectors:

  * Spoofed commands.
  * Command delay/replay.
  * Unauthorized takeover attempts.

### 3. Real-time Visualization of Attacks

* Attacks cause visible effects in QGroundControl: jerks, crashes, abnormal route changes.
* All telemetry is logged for further analysis.

### 4. Training ML Model

* Telemetry data is stored, preprocessed, and fed into ML pipelines.
* Models are trained to **predict anomalies** in real drone operations.

### 5. Response / Defense System

* Monitor MAVLink traffic for anomalies.
* ML model detects malicious commands.
* Automated defense system:

  * Temporary block (2 minutes).
  * Permanent block if persistent.
* Logs and defense events are visualized in real time.

---

## 🖥️ Technologies Used

* **ArduPilot SITL** – Drone simulation.
* **QGroundControl** – Flight control software.
* **MAVLink Protocol** – Communication between drone and controller.
* **Machine Learning** – Anomaly detection.
* **Python** – Log parsing, analysis, and ML.

---

## 🚀 Project Flow

1. **Setup** → Install ArduPilot SITL + QGroundControl.
2. **Normal Operations** → Baseline drone behavior logging.
3. **Attack Simulation** → Inject spoofed, delayed, or takeover commands.
4. **Data Collection** → Save normal + malicious telemetry.
5. **ML Training** → Train anomaly detection models.
6. **Defense Implementation** → Deploy automated countermeasures.

---

## 🎯 Expected Outcomes

* Real-time visualization of drone attacks.
* Comprehensive **logs + structured datasets** for training.
* **ML-based anomaly detection** with measurable accuracy.
* Automated **IDS/IPS system** with blocking and defense rules.

---

## 🛠️ Level-wise Roadmap

### **Level 0 – Passive Exploration (Dataset-based)**

* Use Kaggle drone/IoT datasets.
* Parse logs, label traffic, generate synthetic logs.
* ✅ **Outcome:** ML-ready dataset, anomaly patterns understood.

### **Level 1 – Setup ArduPilot Environment**

* Install & configure ArduPilot SITL.
* Connect SITL with QGroundControl.
* ✅ **Outcome:** Working drone simulator.

* Perform normal commands (takeoff, waypoint navigation).
* Record telemetry & logs.
* ✅ **Outcome:** Baseline dataset.

### **Level 2 – Attack Simulation**

* Inject spoofed, replayed, or unauthorized commands.
* Observe abnormal behaviors in QGroundControl.
* ✅ **Outcome:** Malicious traffic dataset.

### **Level 3 – Log Management & Real-time Analysis (Pre-ML)**

* Store logs in CSV/JSON.
* Rule-based anomaly detection (e.g., altitude spikes).
* ✅ **Outcome:** Human-readable logs + rule-based IDS.

### **Level 4 – Machine Learning Anomaly Detection**

* Train ML models (Isolation Forest, One-Class SVM, Random Forest, XGBoost).
* Evaluate detection accuracy.
* ✅ **Outcome:** ML-powered IDS.

### **Level 5 – Automated Defense Mechanism**

* Real-time MAVLink sniffing.
* Pass traffic through ML model.
* Block attacker temporarily/permanently.
* ✅ **Outcome:** IDS + IPS with live defense actions.

---

## 📊 Final Project Flow

1. Dataset Analysis → **ML familiarity**.
2. Simulation Setup → **Drone environment**.
3. Attack Simulation → **Malicious patterns**.
4. Log Analysis → **Rule-based IDS**.
5. ML IDS → **Smarter detection**.
6. Defense IPS → **Automated protection**.

---

## 🏆 Outcomes & Future Scope

* Build a **full IDS/IPS system for drones** in a simulated environment.
* Extend project to **real drones (hardware integration)**.
* Improve anomaly detection using **deep learning models (LSTMs, Autoencoders)**.


