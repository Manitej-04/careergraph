# CareerGraph

### Graph-Powered Career Recommendation System

CareerGraph is a graph-based web application that helps users explore career paths by connecting **career roles, required skills, practical projects, and technologies**.

The application uses a graph database to model relationships between these entities and provides career recommendations and an interactive graph visualization through a Flask-based web application.

---

## Overview

Choosing a career path often requires understanding how different skills, projects, and technologies relate to a particular role.

CareerGraph represents these relationships as a graph and allows users to select a target career and explore its connected learning path.

For example:

```text
Role
  │
  └── REQUIRES
        │
        ▼
      Skill
        ▲
        │
     TEACHES
        │
        │
      Project
        │
       USES
        │
        ▼
   Technology