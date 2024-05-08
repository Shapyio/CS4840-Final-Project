# Machine-Leanring-Final-Project
Soccer match prediction ML model.

## Table of Contents
- [Problem Statement](#problem-statement)
- [Installation Instructions/Dependencies](#installation-instructionsdependencies)
- [Usage](#usage)
- [Features](#features)
- [Contribution](#contribution)
- [License](#license)
- [Credits](#credits)
- [Contact Information](#contact-information)

## Problem Statement
The ML model will grab game stats/information to predict who will win a particular match. The matches are all Premier League matches spanning from the 2000 season to the 2023 season.

## Installation Instructions/Dependencies
To run the project, simply execute the main Python code `ML-proj.py`. Ensure you have the following dependencies installed:
- [imblearn](https://github.com/scikit-learn-contrib/imbalanced-learn): `pip install imblearn`
- [numpy](https://numpy.org/install/): `pip install numpy`
- [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html): `pip install pandas`
- [scikit-learn](https://scikit-learn.org/stable/install.html): `pip install scikit-learn`

### Usage
The code can be run by executing the main Python file.

## Features
The project utilizes multiple ML models to predict outcomes and compares the results from each model. It also incorporates data preprocessing to ensure consistent and proper data. The preprocessing involves:
- Encoding categorical features using label encoding
- Scaling numerical features using StandardScaler
- Dropping correlated or unusable features
- Experimenting with over and under sampling of the data to evaluate its influence on results.

### Machine Learning Models
The following models are utilized in the code and results compared. Here is a brief description and overview of each model.
- **k-Nearest Neighbors (kNN) Model**: kNN is a simple and intuitive algorithm that classifies data points based on the majority class of their k nearest neighbors in the feature space. In this project, the kNN model is implemented using the `KNeighborsClassifier` from scikit-learn.
  
- **Support Vector Classifier (SVC) Model**: SVC is a powerful algorithm for classification tasks. It works by finding the hyperplane that best separates different classes in the feature space. The SVC model implemented in this project utilizes the `SVC` class from scikit-learn with a polynomial kernel.
  
- **Logistic Regression Model**: Despite its name, logistic regression is a linear model for binary classification tasks. It estimates the probability that a given instance belongs to a particular class. The logistic regression model in this project is implemented using the `LogisticRegression` class from scikit-learn.

## Contribution
Contributions to the project are welcomed under the condition that proper credit is cited.

## License
This project is licensed under the [MIT License](LICENSE).

## Credits
This project is developed for the CS 4840 - Introduction to Machine Learning course at Wright State University.

## Contact Information
For inquiries or further information, please contact [Shapiy Sagiev](https://www.linkedin.com/in/shapiy-sagiev/).

