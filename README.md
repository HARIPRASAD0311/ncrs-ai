# NCRS-AI: Non-Compliance Risk Scoring for Chronic Disease Care

## Overview
NCRS-AI is a learning-based academic prototype that predicts a
Non-Compliance Risk Score (NCRS) for chronic disease patients such as
diabetes and hypertension.

The system helps identify patients who are at risk of missing
medication, diet, or physical activity routines, enabling early
attention through risk awareness.

## Problem
Chronic disease patients often fail to consistently follow care plans.
Most existing applications only track past data or provide reminders
and do not predict future non-compliance risk.

## Solution
NCRS-AI calculates an explainable NCRS score (0–100) classified as:
- Stable
- Warning
- Critical

It also provides a 7-day risk trend and an adaptive weekly care plan.
This system is designed as a decision-support and planning tool.

## What Makes NCRS-AI Different
- Moves from simple reminders to predictive risk scoring
- Uses a single, explainable Non-Compliance Risk Score (NCRS)
- Designed for Indian healthcare context with multilingual support
- Privacy-by-design using synthetic patient data

## Current Prototype Status
 - Synthetic patient dataset generated
 - NCRS calculation and risk classification implemented
 - 7-day risk trend visualization available
 - Patient and doctor dashboards implemented using Streamlit


## Evaluation Logic 
 The NCRS score is calculated using weighted factors such as:
  - Medication adherence
  - Diet deviation
  - Physical activity variation
  - Health signal instability

 The combined score is normalized to a 0–100 scale and classified
 into Stable, Warning, and Critical risk levels.

## Tech Stack
 - Python
 - NumPy, Pandas, scikit-learn
 - Streamlit (prototype dashboard)
 - Flask / FastAPI (backend APIs)
 - GitHub

## Repository Structure
 - ncrs_predictions.csv – sample NCRS outputs
 - patient_profiles.csv – synthetic patient profiles
 - trajectory_forecast.csv – 7-day risk forecast
 - requirements.txt – dependencies

## How to Run (Prototype)
1. Install required libraries using `requirements.txt`
2. Run the Streamlit application
3. View NCRS score and dashboards in the browser

## Live Demo (Prototype)
🔗 Streamlit App:https://ncrs-ai-dbscapph7snxjgguvywaane.streamlit.app/

Note: This is a learning-based academic prototype using synthetic data,
developed for hackathon demonstration purposes.


## Disclaimer
This project is an academic prototype developed for a hackathon.
It uses only synthetic data and does not provide medical diagnosis
or treatment recommendations.
