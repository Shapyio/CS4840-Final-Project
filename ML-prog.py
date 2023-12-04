import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder


data = pd.read_csv("match_report_data.csv", encoding='ISO-8859-1')
# ========== Preprocessing ==========
# Initial data
print(data.head())
data.info()

# Visualized data
#data.hist(bins=20, figsize=(15,10))
#plt.show()

# Converting objects into int64
# LABEL ENCODING ATTEMPT
#label_encoder = LabelEncoder()
#data['Referee_Label'] = label_encoder.fit_transform(data['Referee'])
#print(data)
#data.info()

#ONE-HOT ENCODING ATTEMPT
data_encoded = data[['Referee']]
data_encoded = pd.get_dummies(data, columns=['Referee'], prefix=['Referee'])
data_encoded['Referee'] - data_encoded.values.tolist()
data = pd.concat([data.drop('Referee', axis=1), data_encoded], axis=1)
print(data)




#Logistic Regression w/

#SVM Classification

#kNN Classification