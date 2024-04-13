import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle


# Load data
data = pd.read_csv('new_output.csv')

# Feature Engineering
le = LabelEncoder()
data['day_encoded'] = le.fit_transform(data['day'])
label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
print(label_mapping)

# Split data
X = data[['time', 'day_encoded']]
y = data['file_path']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train Random Forest model
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# saving the model 
with open('model.pickle', 'wb') as f:
    pickle.dump(rf, f)

''' accuracy checked below '''
# # Calculate the accuracy
# accuracy = accuracy_score(y_test, rf.predict(X_test))
# print("Accuracy:", accuracy)
