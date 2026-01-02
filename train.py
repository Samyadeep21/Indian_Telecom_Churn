#Step 1: The Engineer's Training Script (train.py)
#This script prepares the data. We’ll use XGBoost for training a churn prediction model on Indian telecom data.


import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# Loading the Indian Telecom Data
df = pd.read_csv('telecom_churn_data.csv')

# Preprocessing: Convert Indian States and Partners to Numbers
le_partner = LabelEncoder()
df['telecom_partner'] = le_partner.fit_transform(df['telecom_partner'])

# Feature Selection: Focus on usage patterns
features = ['age', 'estimated_salary', 'calls_made', 'sms_sent', 'data_used', 'telecom_partner']
X = df[features]
y = df['churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost - It handles large Indian datasets efficiently
model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1)
model.fit(X_train, y_train)

# Save everything for the Dashboard
pickle.dump(model, open('indian_churn_model.pkl', 'wb'))
pickle.dump(le_partner, open('partner_encoder.pkl', 'wb'))
print("Model trained on Indian Telecom data!")