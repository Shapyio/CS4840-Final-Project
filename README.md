# Machine-Learning-Final-Project
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
The project utilizes multiple ML models to predict outcomes and compares the results from each model. The project also saw the development of a web scraper to collect data for the matches. It also incorporates data preprocessing to ensure consistent and proper data. The preprocessing involves:
- Encoding categorical features using label encoding
- Scaling numerical features using StandardScaler
- Dropping correlated or unusable features
- Experimenting with over and under sampling of the data to evaluate its influence on results.

### Machine Learning Models
The following models are utilized in the code and results compared. Here is a brief description and overview of each model.
- **k-Nearest Neighbors (kNN) Model**: kNN is a simple and intuitive algorithm that classifies data points based on the majority class of their k nearest neighbors in the feature space. In this project, the kNN model is implemented using the `KNeighborsClassifier` from scikit-learn.
  
- **Support Vector Classifier (SVC) Model**: SVC is a powerful algorithm for classification tasks. It works by finding the hyperplane that best separates different classes in the feature space. The SVC model implemented in this project utilizes the `SVC` class from scikit-learn with a polynomial kernel.
  
- **Logistic Regression Model**: Despite its name, logistic regression is a linear model for binary classification tasks. It estimates the probability that a given instance belongs to a particular class. The logistic regression model in this project is implemented using the `LogisticRegression` class from scikit-learn.

### Web Scraper for Match Data Collection

This project includes a web scraper built to collect match information from the website [fbref.com](https://fbref.com/). The scraper is designed to extract match data efficiently, utilizing multiple user agents and rotating them to prevent sending too many requests from the same agent. Additionally, an artificial sleep timer is incorporated to ensure that requests are not sent back-to-back, helping to prevent overloading the server.

The scraper collects match information by following these steps:

1. **Season Extraction**: It starts by extracting links to different seasons of matches available on the website.
   
2. **Match Link Extraction**: For each season, the scraper collects links to individual match reports.

3. **Data Extraction**: Using these links, the scraper retrieves match reports, extracting various details such as date, venue, attendance, referee, team statistics, and more.

4. **Error Handling**: The scraper includes error handling mechanisms to deal with timeouts and other issues that may arise during the scraping process. In case of errors, the problematic links are saved to a separate file for later review.

5. **Data Storage**: The extracted match data is formatted and stored in a CSV file for further analysis and processing.

By leveraging this web scraper, the project aims to gather comprehensive match data efficiently, facilitating the development of predictive models and analysis of football matches.

## Contribution
Contributions to the project are welcomed under the condition that proper credit is cited.

## License
This project is licensed under the [MIT License](LICENSE).

## Credits
This project is developed for the CS 4840 - Introduction to Machine Learning course at Wright State University.

## Contact Information
For inquiries or further information, please contact [Shapiy Sagiev](https://www.linkedin.com/in/shapiy-sagiev/).

