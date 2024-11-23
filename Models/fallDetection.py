import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


data = pd.read_csv('fall_detection_data.csv')

X = data[['acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']]
y = data['fall_detected']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
def predict_fall(acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z):
    input_data = np.array([[acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]])
    prediction = model.predict(input_data)
    return bool(prediction[0])