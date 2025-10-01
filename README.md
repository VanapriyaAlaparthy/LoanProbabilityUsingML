Loan Probability

A machine learning–powered web application that predicts the probability of loan approval based on applicant details. The project consists of:

Backend (Flask API) – serves prediction endpoints using a trained model.

Frontend (Flask/HTML/JS) – user interface for entering loan applicant details and viewing results.

Model Training – Python pipeline that trains a calibrated Random Forest classifier on loan data from PostgreSQL.

🚀 Features

Predicts loan approval probability (not just Yes/No).

Uses a Random Forest model with isotonic calibration for more accurate probabilities.

Connects to PostgreSQL database to fetch loan data.

Provides REST APIs:

GET /features → returns required input fields.

POST /predict → returns approval probability.

Frontend form for entering applicant details and seeing predictions.
