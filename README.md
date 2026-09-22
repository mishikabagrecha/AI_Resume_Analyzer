# AI Resume / ATS Analyzer

An AI-powered Applicant Tracking System (ATS) Resume Analyzer that helps job seekers evaluate their resumes against job requirements and identify areas for improvement.

## Overview

AI Resume / ATS Analyzer is designed to help candidates understand how well their resume matches a target job description.

The application analyzes resume content and provides insights that can help improve keyword matching, relevance, and overall ATS compatibility.

## Features

* Resume analysis using AI
* ATS-focused resume evaluation
* Job description analysis
* Resume-to-job matching
* Identification of relevant keywords
* Resume improvement suggestions
* Clean and user-friendly interface
* Secure environment-variable based API configuration

## Tech Stack

* **Python**
* **AI / LLM APIs**
* **HTML / CSS**
* **Streamlit / Python UI**
* **Virtual Environment (venv)**

## Project Structure

```text
AI_Resume_Analyzer/
│
├── app.py              # Main application
├── ui.py               # User interface components
├── styles.css          # Custom styling
├── .gitignore          # Git ignored files
├── .env                # Local environment variables
└── venv/               # Python virtual environment
```

## How It Works

1. Upload or provide your resume.
2. Provide the target job description.
3. The application analyzes the resume against the job requirements.
4. AI identifies relevant skills and keywords.
5. The application provides ATS-related insights and improvement suggestions.
6. Use the feedback to improve your resume for the target role.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mishikabagrecha/AI_Resume_Analyzer.git
cd AI_Resume_Analyzer
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

Install the required Python packages used by the project.

```bash
pip install -r requirements.txt
```

> If the project does not currently contain a `requirements.txt`, generate one from your environment with:
>
> ```bash
> pip freeze > requirements.txt
> ```

### 5. Configure environment variables

Create a `.env` file in the project root and add the required API configuration.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

Never commit your `.env` file or expose API keys publicly.

### 6. Run the application

Run the application using the command appropriate for your Python UI setup.

For Streamlit:

```bash
streamlit run app.py
```

## Security

API keys and other sensitive configuration are stored locally in `.env` and are excluded from Git using `.gitignore`.

Do not upload API keys, authentication tokens, passwords, or other credentials to GitHub.

## Future Improvements

* Resume PDF parsing
* Multiple resume format support
* Detailed ATS scoring
* Skill-gap analysis
* Job recommendation system
* Resume keyword optimization
* Resume section-wise feedback
* Resume improvement suggestions based on specific job roles
* Downloadable analysis reports

## Purpose

This project was built to explore the application of Artificial Intelligence and Natural Language Processing in resume analysis and recruitment technology.

## Author

**Mishika Bagrecha**

GitHub: [mishikabagrecha](https://github.com/mishikabagrecha)
