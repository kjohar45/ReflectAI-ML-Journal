# 🧠 AI Journal Companion

[![SDG 3](https://img.shields.io/badge/SDG-3--Good--Health--&--Well--Being-green)](https://sdgs.un.org/goals/goal3)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**AI Journal Companion** is a full-stack AI-powered web application designed to help users reflect on their daily thoughts, analyze emotional well-being, and receive personalized motivational feedback using modern AI techniques.

This project implements the **ReflectAI** mathematical framework, enabling real-time personalized sentiment calibration, emotional drift tracking, and cognitive distortion detection, replacing generic, population-level emotion thresholds with individual-specific metrics.

---

## 🚀 Key Features

* ✍️ **Daily Journaling**: Simple, distraction-free interface for free-form daily entries.
* 🧠 **ReflectAI Adaptive Sentiment Personalization (ASP)**: Overrides static sentiment models by locally learning your personal positive (`T_pos`) and negative (`T_neg`) baseline thresholds to accurately classify your emotions.
* 📊 **Emotional Risk & Drift Indices**: Calculates your real-time **Emotional Risk Index (ERI)**, **Emotional Volatility Index (EVI)**, and **Emotional Drift Score (EDS)** natively on the dashboard.
* 🛑 **Cognitive Pattern Detection (CPD)**: Scans journal entries to detect and highlight cognitive distortions (e.g., absolutist thinking or catastrophizing) based on CBT lexicons.
* 💬 **AI-Generated Motivation**: Uses **Groq SDK** and ReflectAI logic to generate empathetic, personalized messages that intercept risky behaviors or fall back to LLM encouragement.
* 🚨 **Consented SMS Crisis System**: Employs an LLM to secretly categorize entries into `SUICIDAL_IDEATION`, `SELF_HARM`, or `HARM_OTHERS`. It securely prompts users dynamically on the frontend before routing mocked text messages to their emergency cellular contacts (`sms_service.py`) or recommending the 988 lifeline.
* 📈 **Offline Research Generators**: Includes a `generate_paper_graphs.py` Pandas/Matplotlib script to mathematically output 30-day simulated datasets and dump print-friendly CSVs/PNGs replicating the ReflectAI research distributions.
* ✨ **Premium UI**: Fully responsive light-mode dashboard featuring fluid typography, CSS Grid, and custom charting.
* 💾 **Persistent Storage**: Robust **SQLite** database integration with automatic timestamping and secure JWT-based user authentication.

---

## 🏗️ System Architecture

The hybrid AI architecture ensures fast, explainable emotion detection coupled with deep contextual reasoning.

1. **React Frontend**: Captures user input and dynamically renders the ReflectMetrics, Calendar, and MoodChart.
2. **Flask REST API**: Orchestrates the data flow, authenticates users via JWT, and executes the math formulas.
3. **ReflectAI Engine**: Applies ASP, EVI, EDS, and CPD math logic directly to the user's isolated history (`reflect.py`).
4. **Groq (LLM) / VADER NLP**: Base text ingestion engines to extract syntax and provide fallback motivation.
5. **SQLite**: Handles data persistence securely.

---

## 🧑‍💻 Tech Stack

| Component | Technologies |
| :--- | :--- |
| **Frontend** | React.js, Axios, Chart.js, Vanilla CSS |
| **Backend** | Python, Flask, Flask-CORS, Flask-JWT-Extended |
| **AI / NLP** | VADER Sentiment, CBT Lexicons, Groq SDK |
| **Database** | SQLite |

---

## 📂 Setup & Testing

1. **Install Dependencies**:
   - Backend: `cd backend && source venv/bin/activate && pip install -r requirements.txt`
   - Frontend: `cd frontend && npm install`
2. **Setup Groq API**:
   - Ensure a `.env` file exists in `/backend` with `GROQ_API_KEY=your_key_here`. 
3. **Seed Test Data**:
   - To immediately visualize the ReflectAI dashboard charts, run `python backend/seed.py`.
   - Log in using Username: `demo`, Password: `password`.
4. **Run Servers**:
   - Backend: `python backend/app.py` (Runs on `localhost:5000`)
   - Frontend: `npm start` (Runs on `localhost:3000`)
