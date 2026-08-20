from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib


# 1. load iris dataset

iris =load_iris()

x = iris.data
y = iris.target

# 2. Split data into training and testing sets

x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size = 0.2,
    random_state = 42,
    stratify = y
    
)


# 3. Create ML pipeline

model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(
        n_estimators = 100,
        random_state = 42

    ))
])

# 4. train the model

model.fit(x_train, y_train)

#5 make predictions

y_pred = model.predict(x_test)

# 6. Calculate accuracy

accuracy =  accuracy_score(y_test, y_pred)

print(f"Model Accuracy : {accuracy:.2f}")

# 7. Save the trained model

model_path = "ml/saved_model/model.joblib"

joblib.dump(model, model_path)

print(f"Model saved successfully at: {model_path}")