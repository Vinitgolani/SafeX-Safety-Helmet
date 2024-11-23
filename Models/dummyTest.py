import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate fall detection data
def generate_fall_data(num_samples=1000):
    timestamps = [datetime(2023, 1, 1) + timedelta(seconds=i) for i in range(num_samples)]
    acc_x = np.random.normal(0, 1, num_samples)
    acc_y = np.random.normal(0, 1, num_samples)
    acc_z = np.random.normal(-9.8, 0.1, num_samples)  # Assuming z-axis is aligned with gravity
    gyro_x = np.random.normal(0, 0.1, num_samples)
    gyro_y = np.random.normal(0, 0.1, num_samples)
    gyro_z = np.random.normal(0, 0.1, num_samples)
    fall_detected = np.random.choice([0, 1], num_samples, p=[0.99, 0.01])  # 1% fall rate

    # Simulate falls
    fall_indices = np.where(fall_detected == 1)[0]
    for idx in fall_indices:
        acc_x[idx:idx+10] = np.random.normal(0, 5, 10)
        acc_y[idx:idx+10] = np.random.normal(0, 5, 10)
        acc_z[idx:idx+10] = np.random.normal(0, 5, 10)
        gyro_x[idx:idx+10] = np.random.normal(0, 2, 10)
        gyro_y[idx:idx+10] = np.random.normal(0, 2, 10)
        gyro_z[idx:idx+10] = np.random.normal(0, 2, 10)

    df = pd.DataFrame({
        'timestamp': timestamps,
        'acc_x': acc_x,
        'acc_y': acc_y,
        'acc_z': acc_z,
        'gyro_x': gyro_x,
        'gyro_y': gyro_y,
        'gyro_z': gyro_z,
        'fall_detected': fall_detected
    })
    return df

# Generate heart rate data
def generate_heart_rate_data(num_samples=1000):
    timestamps = [datetime(2023, 1, 1) + timedelta(seconds=30*i) for i in range(num_samples)]
    heart_rate = np.random.normal(70, 5, num_samples)  # Normal heart rate around 70 bpm
    
    # Simulate some anomalies
    anomaly_indices = np.random.choice(num_samples, size=int(num_samples*0.01), replace=False)
    heart_rate[anomaly_indices] = np.random.normal(120, 10, len(anomaly_indices))

    df = pd.DataFrame({
        'timestamp': timestamps,
        'heart_rate': heart_rate.astype(int)
    })
    return df

# Generate and save the dummy data
fall_data = generate_fall_data()
fall_data.to_csv('fall_detection_data.csv', index=False)

heart_rate_data = generate_heart_rate_data()
heart_rate_data.to_csv('heart_rate_data.csv', index=False)

print("Dummy data generated and saved to CSV files.")