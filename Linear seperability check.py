import pandas as pd
from sklearn.svm import SVC

# Load the data from the CSV file
data = pd.read_csv('LowObject6DetectorsLJTest.csv')

# Separate the inputs (X) and the output (y)
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Create a Support Vector Machine (SVM) classifier
classifier = SVC(kernel='linear')

# Train the classifier
classifier.fit(X, y)

# Check if the data is linearly separable
is_linearly_separable = classifier.score(X, y) == 1.0

print(classifier.score(X, y))# Predict the outputs for the inputs

y_pred = classifier.predict(X)

# Find the indices of the misclassified samples
misclassified_indices = [i for i, (pred, true) in enumerate(zip(y_pred, y)) if pred != true]

# Print the misclassified inputs
for i in misclassified_indices:
    print(f"Input {i} was misclassified: {X.iloc[i]}")

if is_linearly_separable:
    print("The data is linearly separable.")
else:
    print("The data is not linearly separable.")