import pandas as pd
from geopy.distance import geodesic

# -------- CONFIG --------
INPUT_PATH = "/home/damnkrishna/Downloads/datam/drone_communication_dataset.csv"       # path to read dataset
OUTPUT_PATH = "/home/damnkrishna/Downloads/datam/drone_communication_dataset_tagged.csv" # path to save labeled dataset
SUMMARY_PATH = "/home/damnkrishna/Downloads/datam/attack_summary.csv"                   # path to save summary
# ------------------------

def detect_attacks(df):
    attack_types = []
    
    for i in range(len(df)):
        attack = "normal"  # default
        
        protocol = df.loc[i, "communication_protocol"]
        freq = float(df.loc[i, "frequency_band"])
        packets = int(df.loc[i, "network_traffic_volume"])  # using network_traffic_volume as packets
        signal = float(df.loc[i, "signal_strength"])
        coord = eval(df.loc[i, "drone_gps_coordinates"])  # tuple (lat, lon)
        timestamp = pd.to_datetime(df.loc[i, "timestamp"])
        
        # -------- Protocol-Frequency Mismatch --------
        if (protocol == "ZigBee" and freq not in [2.4]) or \
           (protocol == "LoRa" and freq not in [0.868, 2.4]) or \
           (protocol == "Wi-Fi" and freq not in [2.4, 5.0]):
            attack = "Protocol_Frequency_Mismatch"
        
        # -------- GPS Spoofing (distance/time anomaly) --------
        if i > 0:
            prev_coord = eval(df.loc[i-1, "drone_gps_coordinates"])
            prev_time = pd.to_datetime(df.loc[i-1, "timestamp"])
            hours = (timestamp - prev_time).total_seconds() / 3600
            if hours > 0:
                dist = geodesic(coord, prev_coord).km
                speed = dist / hours
                if speed > 500:  # >500 km/h is unrealistic for drone
                    attack = "GPS_Spoofing"
        
        # -------- Packet Traffic Anomaly --------
        if packets > 1000:  # threshold adjusted because dataset has large values
            attack = "Traffic_Anomaly"
        
        # -------- Signal Strength Jamming --------
        if i > 0:
            prev_signal = float(df.loc[i-1, "signal_strength"])
            if abs(signal - prev_signal) > 20:
                attack = "Signal_Jamming"
        
        attack_types.append(attack)
    
    return attack_types


def main():
    # Read dataset
    df = pd.read_csv(INPUT_PATH)
    
    # Add attack detection
    df["Attack_Type"] = detect_attacks(df)
    df["Label"] = df["Attack_Type"].apply(lambda x: "malicious" if x != "normal" else "normal")
    
    # Save labeled dataset
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"[+] Analysis complete. Labeled dataset saved to {OUTPUT_PATH}")

    # --- Expanded Report ---
    print("\n[+] Expanded Attack Report")

    # Count overall normal vs malicious
    print("\nLabel Distribution:")
    print(df["Label"].value_counts())

    # Count by Attack Type
    print("\nAttack Type Breakdown:")
    print(df["Attack_Type"].value_counts())

    # Save breakdown to CSV
    breakdown = df["Attack_Type"].value_counts().reset_index()
    breakdown.columns = ["Attack_Type", "Count"]
    breakdown.to_csv(SUMMARY_PATH, index=False)
    print(f"\n[+] Detailed attack summary saved to {SUMMARY_PATH}")

    # Optional: show some correlations with features (basic example)
    feature_cols = ["signal_strength", "packet_loss_rate", "round_trip_time",
                    "frequency_band", "altitude", "speed_trajectory"]
    print("\n[+] Sample Feature Averages per Attack Type:")
    print(df.groupby("Attack_Type")[feature_cols].mean(numeric_only=True).head())


if __name__ == "__main__":
    main()
