import joblib

# Load the saved model
model_path = "ml/saved_model/model.joblib"

model = joblib.load(model_path)

# Sample Iris flower data
sample = [[5.1, 3.5, 1.4, 0.2]]

# Make prediction
prediction = model.predict(sample)

# Iris class names
class_names = ["setosa", "versicolor", "virginica"]

predicted_class = class_names[prediction[0]]

print(f"Predicted class: {predicted_class}")