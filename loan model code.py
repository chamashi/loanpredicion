# -*- coding: utf-8 -*-
"""loan3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1i7nAtSd6xLAwQxjozI7GYeuY7cidHcAP
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

loan_df = pd.read_csv("/content/drive/MyDrive/Loan Dataset/Loan_dataset.csv")

loan_df.head()

loan_df.shape

loan_df.describe()

loan_df.duplicated().sum()

loan_df.info()

loan_df.isnull().sum()

sns.countplot(x='Education',hue='Loan_Status',data=loan_df)

sns.countplot(x='Married',hue='Loan_Status',data=loan_df)

sns.countplot(x='Gender',hue='Loan_Status',data=loan_df)

sns.countplot(x='Dependents',hue='Loan_Status',data=loan_df)

sns.countplot(x='Self_Employed',hue='Loan_Status',data=loan_df)

ax = loan_df["ApplicantIncome"].hist(density=True, stacked=True, color='teal', alpha=0.6)
loan_df["ApplicantIncome"].plot(kind='density', color='teal')
ax.set(xlabel='Applicant Income')
plt.show()

ax = loan_df["CoapplicantIncome"].hist(density=True, stacked=True, color='teal', alpha=0.6)
loan_df["CoapplicantIncome"].plot(kind='density', color='teal')
ax.set(xlabel='Co-Applicant Income')
plt.show()

ax = loan_df["LoanAmount"].hist(density=True, stacked=True, color='teal', alpha=0.6)
loan_df["LoanAmount"].plot(kind='density', color='teal')
ax.set(xlabel='Loan Amount')
plt.show()

sns.countplot(x='Loan_Amount_Term',hue='Loan_Status',data=loan_df)

sns.countplot(x='Credit_History',hue='Loan_Status',data=loan_df)

sns.countplot(x='Property_Area',hue='Loan_Status',data=loan_df)

#handling missing values
new_loan = loan_df.copy()
new_loan['Gender'].fillna(new_loan['Gender'].value_counts().idxmax(), inplace=True)
new_loan['Married'].fillna(new_loan['Married'].value_counts().idxmax(), inplace=True)
new_loan['Dependents'].fillna(new_loan['Dependents'].value_counts().idxmax(), inplace=True)
new_loan['Self_Employed'].fillna(new_loan['Self_Employed'].value_counts().idxmax(), inplace=True)
new_loan["LoanAmount"].fillna(new_loan["LoanAmount"].mean(skipna=True), inplace=True)
new_loan['Loan_Amount_Term'].fillna(new_loan['Loan_Amount_Term'].value_counts().idxmax(), inplace=True)
new_loan['Credit_History'].fillna(new_loan['Credit_History'].value_counts().idxmax(), inplace=True)

#converting the categorical columns to numeric
new_loan['Gender'] = new_loan['Gender'].replace({"Female": 0, "Male": 1})
new_loan['Married'] = new_loan['Married'].replace({'No' : 0,'Yes' : 1})
new_loan['Dependents'] = new_loan['Dependents'].replace({'0':0,'1':1,'2':2,'3+':3})
new_loan['Education'] = new_loan['Education'].replace({'Not Graduate' : 0, 'Graduate' : 1})
new_loan['Self_Employed'] = new_loan['Self_Employed'].replace({'No' : 0,'Yes' : 1})
new_loan['Property_Area'] = new_loan['Property_Area'].replace({'Semiurban' : 0, 'Urban' : 1,'Rural' : 2})
new_loan['Loan_Status'] = new_loan['Loan_Status'].replace({"N" : 0, "Y" : 1})

new_loan.info()

plt.figure(figsize=(10,6))
sns.heatmap(round(new_loan.corr(),2), annot=True, cmap="coolwarm")

sns.boxplot(new_loan[['Gender','Married','Dependents','Education']])

sns.boxplot(new_loan[['ApplicantIncome','Self_Employed','Property_Area', 'Loan_Status']])

# Calculate the IQR, Upper and Lower Limits for gender
Q1 = new_loan['ApplicantIncome'].quantile(0.25)
Q3 = new_loan['ApplicantIncome'].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Filter out outliers
new_loan = new_loan[(new_loan['ApplicantIncome'] >= lower_limit) & (new_loan['ApplicantIncome'] <= upper_limit)]

sns.boxplot(new_loan[['LoanAmount','Loan_Amount_Term','Credit_History']])

# Calculate the IQR, Upper and Lower Limits for gender
Q1 = new_loan['CoapplicantIncome'].quantile(0.25)
Q3 = new_loan['CoapplicantIncome'].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Filter out outliers
new_loan = new_loan[(new_loan['CoapplicantIncome'] >= lower_limit) & (new_loan['CoapplicantIncome'] <= upper_limit)]

sns.boxplot(new_loan[['LoanAmount','Loan_Amount_Term','Credit_History']])

# Calculate the IQR, Upper and Lower Limits for gender
Q1 = new_loan['LoanAmount'].quantile(0.25)
Q3 = new_loan['LoanAmount'].quantile(0.75)
IQR = Q3 - Q1
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Filter out outliers
new_loan = new_loan[(new_loan['LoanAmount'] >= lower_limit) & (new_loan['LoanAmount'] <= upper_limit)]

sns.boxplot(new_loan[['Loan_Status']])

# separating the data and label
X = new_loan.drop(columns=['Loan_ID','Loan_Status'],axis=1)
y = new_loan['Loan_Status']

new_loan.head()

from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
def evaluate(model, X_test, y_test):
    pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, pred)
    precision = precision_score(y_test, pred, average='macro')
    recall = recall_score(y_test, pred, average='macro')
    f1 = f1_score(y_test, pred, average='macro')

    # Print the classification report
    print(classification_report(y_test, pred))

    # Print individual metrics
    print('Accuracy: %f' % accuracy)
    print('Precision: %f' % precision)
    print('Recall: %f' % recall)
    print('F1 score: %f' % f1)

    print("================================================================")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

models = [
    ('Decision Tree', DecisionTreeClassifier(random_state=1)),
    ('Random Forest', RandomForestClassifier(random_state=1)),
    ('SVC', SVC(random_state=1)),
]

for model_name, model in models:
    print(f"Model: {model_name}")
    model.fit(X_train, y_train)
    evaluate(model, X_test, y_test)

from sklearn.model_selection import GridSearchCV
models = [
    ('Decision Tree', DecisionTreeClassifier(random_state=1), {
        'criterion': ['gini', 'entropy'],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }),
    ('Random Forest', RandomForestClassifier(random_state=1), {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }),
    ('SVC', SVC(random_state=1), {
        'C': [0.25, 0.50, 0.75],
        'kernel': ['poly']
    })

]

best_model = None
best_model_name = ""
best_model_score = 0.0  # Initialize with a low value

# Loop through models, perform hyperparameter tuning, and print the best model
for model_name, model, param_grid in models:
    print(f"Model: {model_name}")

    # Initialize Grid Search with cross-validation
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1)

    # Fit Grid Search to the data
    grid_search.fit(X_train, y_train)

    # Get the best parameters and estimator
    best_params = grid_search.best_params_
    best_estimator = grid_search.best_estimator_

    # Evaluate the best model on the test set
    score = best_estimator.score(X_test, y_test)

    # Print and compare the performance of this model
    print(f"Best {model_name} Model (Score: {score:.4f}): {best_params}")

    # Update the best model if this one performs better
    if score > best_model_score:
        best_model = best_estimator
        best_model_name = model_name
        best_model_score = score

# Print the final best model
print(f"Final Best Model:{best_model_name} (Score: {best_model_score:.4f})")

final_model = best_model
final_model.fit(X, y)

import pickle
pickle.dump(final_model,open('loanmodel6.pkl','wb'))