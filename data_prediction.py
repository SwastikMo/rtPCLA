import pickle

hour = 8
day =  1  # {'Fri': 0, 'Mon': 1, 'Sat': 2, 'Sun': 3, 'Thu': 4, 'Tue': 5, 'Wed': 6}

# load model  
with open('model.pickle', 'rb') as f:
    loaded_model = pickle.load(f)

# predicting for example input : 
predicted_file_path = loaded_model.predict([[hour, day]])
print(f"Predicted File Path: {predicted_file_path}")
