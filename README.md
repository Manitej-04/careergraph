# CareerGraph

### Graph-Powered Career Recommendation System

CareerGraph is a graph-based web application that helps users explore career paths by connecting **career roles, required skills, practical projects, and technologies**.

The application uses a graph database to model relationships between these entities and provides career recommendations and an interactive graph visualization through a Flask-based web application.

---

## Overview

Choosing a career path often requires understanding how different skills, projects, and technologies relate to a particular role.

CareerGraph represents these relationships as a graph and allows users to select a target career and explore its connected learning path.

                  ┌──────────────┐
                  │     Role     │
                  └──────┬───────┘
                         │
                      REQUIRES
                         │
                         ▼
                  ┌──────────────┐
                  │    Skill     │
                  └──────┬───────┘
                         │
                      TEACHES
                         │
                         ▼
                  ┌──────────────┐
                  │   Project    │
                  └──────┬───────┘
                         │
                        USES
                         │
                         ▼
                  ┌──────────────┐
                  │ Technology   │
                  └──────────────┘

Example:
For the Data Analyst role, the graph can contain relationships such as:

    Data Analyst
        │
        ├── REQUIRES → Python
        ├── REQUIRES → SQL
        ├── REQUIRES → Statistics
        └── REQUIRES → Database Design

    Python
        ↑
        │ TEACHES
        │
    Analytics Dashboard
        │
        ├── USES → PostgreSQL
        ├── USES → Pandas
        └── USES → Power BI

## Features

- Career role selection
- Required skill discovery
- Project recommendations
- Technology relationships
- Interactive career graph
- Career statistics
- REST APIs

## Tech Stack

- Python
- Flask
- CognoDB
- Cypher
- HTML
- CSS
- JavaScript

## Steps to Run the Application

1. Create a CognoDB Cloud instance
  - Go to CognoDB Cloud.
  - Create an account and provision a free C0 instance.
  - Copy the following connection details:
  - URI: bolt+s://<instance-id>.databases.cognodb.cloud
  - Username: cognodb
  - Password: generated when the instance is created.
  - Save the password securely because CognoDB displays it only once.

2. Clone the repository
  - git clone <YOUR_GITHUB_REPOSITORY_URL>
  - cd CareerGraph

3. Create a Python virtual environment
  - python -m venv .venv
  - .venv\Scripts\activate

4. Install dependencies
  - pip install -r requirements.txt

5. Configure environment variables
  - COGNODB_URI=bolt+s://<your-instance-id>.databases.cognodb.cloud
  - COGNODB_USER=cognodb
  - COGNODB_PASSWORD=<your-cognodb-password>

6. Seed the graph database
  - python seed.py
  - Expected output:
      python seed.py

7. Start the Flask application
  - python app.py
  - Flask start on: http://127.0.0.1:5000


Author
Manitej Budigini