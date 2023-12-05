# Data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from imblearn.under_sampling import RandomUnderSampler
# Preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
# Models
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
# Evaluation
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

data = pd.read_csv("match_report_data.csv", encoding='ISO-8859-1')

# ========== Preprocessing ==========
# Initial data
print(data.head())
data.info()

# Visualized data
#data.hist(bins=20, figsize=(15,10))
#plt.show()

# === Processing objects ===
# Date
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
data['Year'] = data['Date'].dt.year.astype(str)
data['Month'] = data['Date'].dt.month.astype(str)
data['Day'] = data['Date'].dt.day.astype(str)
# Don't need "Date" as its converted to one-hot encoding
data = data.drop("Date", axis=1)

# Categorical columns
cat_columns = ['HomeTeam', 'AwayTeam', 'FTR', 'HTR', 'Referee']
data_cat = data[cat_columns].copy()

# === Label Encoding categorical objects ===
# Create a LabelEncoder for each column
label_encoders = {}
for column in cat_columns:
    le = LabelEncoder()
    data_cat[column] = le.fit_transform(data_cat[column])
    label_encoders[column] = le # Mapping label encoder

# Test to see if label encoding works
# print("Mapping for FTR/HTR:")
# for label, original_value in zip(range(len(label_encoders['FTR'].classes_)), label_encoders['FTR'].classes_):
#     print(f"{label} -> {original_value}")
# print(data_cat.head())

# === Cleaning numerical features ===
data_num = data.copy()
# Drop categorical data
data_num = data_num.drop('HomeTeam', axis=1)
data_num = data_num.drop('AwayTeam', axis=1)
data_num = data_num.drop('FTR', axis=1)
data_num = data_num.drop('HTR', axis=1)
data_num = data_num.drop('Referee', axis=1)

# === Checking correlation between data ===
# print("CORRELATION:")
# Data frame of combined data
data_combined_df = pd.concat([data_num, data_cat], axis=1)
corr_matrix = data_combined_df.corr(numeric_only=True)
# print(corr_matrix['FTR'].sort_values(ascending=False))

# === Dropping correlated data/unusable object data ===
# The model shouldn't train or test with these features because it strongly determines outcome of FTR (Home Winning)
# Catergorical data dropped
data_cat = data_cat.drop("HTR", axis=1)
# Numerical data dropped
data_num = data_num.drop("FTHG", axis=1)
data_num = data_num.drop("FTAG", axis=1)
data_num = data_num.drop("HTHG", axis=1)
data_num = data_num.drop("HTAG", axis=1)

# Separate true labels from data
data_labels = data_cat['FTR'].copy()
data_cat = data_cat.drop('FTR', axis=1)

# print("LABELS:\n", data_labels.head())
# print("FEATURES:\n", data_cat.head())

# === Scaling numerical data ===
# Applying scalar on numerical data remaining
std_scaler  = StandardScaler()
data_scaled = std_scaler.fit_transform(data_num)

# === Combining numerical and categorical ===
# Concatenating data frames together to ndarray
data_combined = np.concatenate([data_cat, data_scaled], axis=1)
# print("COMBINED DATA: \n", data_combined)

# === Checking new data frame ===
# Checking data types and if any nulls
# print("NULL VALUES: \n", np.any(np.isnan(data_combined)))
# print("DATA TYPES: \n", data_combined.dtype)

# ========== Normal Data ==========
# ==== Train-Test Split ====
# Assigning X train and y test features
X = data_combined # X is combined ndarray without true label ('FTR')
y = data_labels.to_numpy() # y is true label value for each data point

# print("PRE SPLIT: ")
# print("X SHAPE: ", X.shape)
# print("Y SHAPE: ", y.shape)

# train-test split with 80% for training and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Evaluating split ===
# print("POST SPLIT: ")
# print("X_TRAIN SHAPE: ", X_train.shape)
# print("Y_TRAIN SHAPE: ", y_train.shape)
# print("X_TEST SHAPE: ", X_test.shape)
# print("Y_TEST SHAPE: ", y_test.shape)

# ===== Models w/ Normal Data =====
print("\n===== Normal Data =====")
# === Logistic Regression ===
print("\nLogistic Regression")
# Create/Train
regression_model = LogisticRegression(max_iter=500)
regression_model.fit(X_train, y_train)
# Test
y_pred = regression_model.predict(X_test)
# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# === SVM Classification ===
print("\nSVM Classification")
# Create/Train
svm_model = SVC(kernel='poly', C=1.0)  # You can adjust the kernel and C parameter
svm_model.fit(X_train, y_train)
# Test
y_pred = svm_model.predict(X_test)
# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=1))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# === kNN Classification ===
print("\nkNN Classification")
# Create/Train
knn_model = KNeighborsClassifier(n_neighbors=15)  # You can adjust the number of neighbors
knn_model.fit(X_train, y_train)
# Test
y_pred = knn_model.predict(X_test)
# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ========== Undersampling Data ==========
rus = RandomUnderSampler(sampling_strategy='not majority', random_state=42) # Majority of games are value=2 (Home team loses), so we remove not majority to balance (less 0 and 1)
# Fit and apply the undersampling
X_resampled, y_resampled = rus.fit_resample(X.copy(), y.copy()) # Copies to ensure originals untouched
# Train-learn split with resampled data
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# ========== Models w/ Undersampled Data ==========
print("\n===== Undersampled Data =====")
# === Logistic Regression ===
print("\nLogistic Regression")
# Create/Train
regression_model = LogisticRegression(max_iter=500)
regression_model.fit(X_train, y_train)
# Test
y_pred = regression_model.predict(X_test)
# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# === SVM Classification ===
print("\nSVM Classification")
# Create/Train
svm_model = SVC(kernel='poly', C=1.0)  # You can adjust the kernel and C parameter
svm_model.fit(X_train, y_train)
# Test
y_pred = svm_model.predict(X_test)
# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred, zero_division=1))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# === kNN Classification ===
print("\nkNN Classification")
# Create/Train
knn_model = KNeighborsClassifier(n_neighbors=15)  # You can adjust the number of neighbors
knn_model.fit(X_train, y_train)
# Test
y_pred = knn_model.predict(X_test)
# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))