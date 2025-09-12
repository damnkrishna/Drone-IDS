# Passive Dataset Analysis

This module handles the **passive exploration** of drone communication datasets for anomaly detection. It uses publicly available Kaggle datasets to analyze drone traffic and prepare labeled datasets for later machine learning training.

---

## 📌 Overview

* **Purpose:** Analyze drone communication logs from a Kaggle dataset to identify normal and malicious activities.
* **Input:** Kaggle drone communication dataset (CSV format).
* **Output:**

  1. Labeled CSV file with `normal/malicious` tags and attack type.
  2. `attack_summary.csv` summarizing the frequency and type of detected attacks.

---

## 🖥️ Files in This Module

```
analyze_drone.py                       # Main script for dataset analysis
drone_communication_dataset.csv        # Raw dataset from Kaggle
drone_communication_dataset_tagged.csv # Labeled dataset with normal/malicious and attack type
attack_summary.csv                     # Summary of attacks detected
venv/                                  # Python virtual environment
```

---

<img width="388" height="55" alt="image" src="https://github.com/user-attachments/assets/c4436cc9-1a59-4361-92db-d5efc253a406" />

1. **Download Dataset:**

   * Get the drone communication dataset from Kaggle.

    https://www.kaggle.com/datasets/datasetengineer/drone-communication-dataset?utm_source=chatgpt.com

2. **Set Dataset Path:**

   * Open `analyze_drone.py` and update the dataset path variable to point to the downloaded CSV.

3. **Run the Script:**

```bash
python3 analyze_drone.py
```

4. **Outputs Generated:**

   * `drone_communication_dataset_tagged.csv` → Contains traffic labeled as `normal` or `malicious` along with the attack type.
   * `attack_summary.csv` → Summary of the final results with attack counts and types.

---

## 📝 Features

* **Automatic labeling:** Tags drone communication as `normal` or `malicious`.
* **Attack detection:** Identifies the type of attack present in the dataset.
* **Summary report:** Provides a quick overview of detected attacks for analysis.
* **Ready for ML training:** Outputs can be directly used to train anomaly detection models.

---

## 🔧 Dependencies

* Python 3.x
* pandas

Install dependencies with:

```bash
pip install pandas
```


## ✅ Outcome

* A **labeled dataset** ready for ML-based anomaly detection.
* **Insight into drone communication attacks** and frequency patterns.
* Simplifies the **first stage of the Drone IDS project** by preparing ML-ready data.


