from database import driver


def seed():
    with driver.session() as session:

        # ============================================================
        # 1. CLEAR EXISTING GRAPH
        # ============================================================

        session.run("""
        MATCH (n)
        DETACH DELETE n
        """)

        # ============================================================
        # 2. CREATE NODES
        # ============================================================

        session.run("""
        CREATE

        // ------------------------------------------------------------
        // ROLES
        // ------------------------------------------------------------

        (backend:Role {
            name: 'Backend Developer',
            category: 'Software Engineering'
        }),

        (frontend:Role {
            name: 'Frontend Developer',
            category: 'Software Engineering'
        }),

        (data:Role {
            name: 'Data Analyst',
            category: 'Data & Analytics'
        }),


        // ------------------------------------------------------------
        // SKILLS
        // ------------------------------------------------------------

        (python:Skill {name: 'Python'}),
        (sql:Skill {name: 'SQL'}),
        (docker:Skill {name: 'Docker'}),
        (api:Skill {name: 'REST APIs'}),
        (react:Skill {name: 'React'}),
        (javascript:Skill {name: 'JavaScript'}),
        (statistics:Skill {name: 'Statistics'}),
        (git:Skill {name: 'Git'}),
        (database:Skill {name: 'Database Design'}),


        // ------------------------------------------------------------
        // TECHNOLOGIES
        // ------------------------------------------------------------

        (flask:Technology {name: 'Flask'}),
        (redis:Technology {name: 'Redis'}),
        (reactTech:Technology {name: 'React'}),
        (postgres:Technology {name: 'PostgreSQL'}),
        (pandas:Technology {name: 'Pandas'}),
        (powerbi:Technology {name: 'Power BI'}),
        (dockerTech:Technology {name: 'Docker'}),


        // ------------------------------------------------------------
        // PROJECTS
        // ------------------------------------------------------------

        (apiProject:Project {
            name: 'REST API Project',
            difficulty: 'Intermediate',
            description: 'Build a production-style REST API with authentication and database integration.'
        }),

        (urlProject:Project {
            name: 'URL Shortener',
            difficulty: 'Intermediate',
            description: 'Build a scalable URL shortening service with caching and containerization.'
        }),

        (dashboard:Project {
            name: 'Analytics Dashboard',
            difficulty: 'Intermediate',
            description: 'Build an interactive analytics dashboard using SQL, Python and business statistics.'
        }),

        (frontendProject:Project {
            name: 'Frontend Dashboard',
            difficulty: 'Beginner',
            description: 'Build a responsive dashboard using React and modern JavaScript.'
        }),

        (salesProject:Project {
            name: 'Sales Analytics Pipeline',
            difficulty: 'Advanced',
            description: 'Build an end-to-end data pipeline for cleaning, transforming and analyzing sales data.'
        }),

        (churnProject:Project {
            name: 'Customer Churn Analysis',
            difficulty: 'Advanced',
            description: 'Analyze customer behavior and identify patterns associated with customer churn.'
        })
        """)

        # ============================================================
        # 3. ROLE → SKILL RELATIONSHIPS
        # ============================================================

        # ------------------------------------------------------------
        # Backend Developer
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (r:Role {name: 'Backend Developer'}),
            (python:Skill {name: 'Python'}),
            (sql:Skill {name: 'SQL'}),
            (docker:Skill {name: 'Docker'}),
            (api:Skill {name: 'REST APIs'}),
            (git:Skill {name: 'Git'}),
            (database:Skill {name: 'Database Design'})

        CREATE
            (r)-[:REQUIRES]->(python),
            (r)-[:REQUIRES]->(sql),
            (r)-[:REQUIRES]->(docker),
            (r)-[:REQUIRES]->(api),
            (r)-[:REQUIRES]->(git),
            (r)-[:REQUIRES]->(database)
        """)

        # ------------------------------------------------------------
        # Frontend Developer
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (r:Role {name: 'Frontend Developer'}),
            (react:Skill {name: 'React'}),
            (js:Skill {name: 'JavaScript'}),
            (git:Skill {name: 'Git'})

        CREATE
            (r)-[:REQUIRES]->(react),
            (r)-[:REQUIRES]->(js),
            (r)-[:REQUIRES]->(git)
        """)

        # ------------------------------------------------------------
        # Data Analyst
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (r:Role {name: 'Data Analyst'}),
            (sql:Skill {name: 'SQL'}),
            (stats:Skill {name: 'Statistics'}),
            (python:Skill {name: 'Python'}),
            (database:Skill {name: 'Database Design'})

        CREATE
            (r)-[:REQUIRES]->(sql),
            (r)-[:REQUIRES]->(stats),
            (r)-[:REQUIRES]->(python),
            (r)-[:REQUIRES]->(database)
        """)

        # ============================================================
        # 4. PROJECT → SKILL RELATIONSHIPS
        # ============================================================

        # ------------------------------------------------------------
        # REST API Project
        # Skills: Python, REST APIs, SQL, Database Design
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'REST API Project'}),
            (api:Skill {name: 'REST APIs'}),
            (python:Skill {name: 'Python'}),
            (sql:Skill {name: 'SQL'}),
            (database:Skill {name: 'Database Design'})

        CREATE
            (p)-[:TEACHES]->(api),
            (p)-[:TEACHES]->(python),
            (p)-[:TEACHES]->(sql),
            (p)-[:TEACHES]->(database)
        """)

        # ------------------------------------------------------------
        # URL Shortener
        # Skills: Docker, REST APIs, Python
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'URL Shortener'}),
            (docker:Skill {name: 'Docker'}),
            (api:Skill {name: 'REST APIs'}),
            (python:Skill {name: 'Python'})

        CREATE
            (p)-[:TEACHES]->(docker),
            (p)-[:TEACHES]->(api),
            (p)-[:TEACHES]->(python)
        """)

        # ------------------------------------------------------------
        # Analytics Dashboard
        # Skills: SQL, Statistics, Python, Database Design
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'Analytics Dashboard'}),
            (sql:Skill {name: 'SQL'}),
            (stats:Skill {name: 'Statistics'}),
            (python:Skill {name: 'Python'}),
            (database:Skill {name: 'Database Design'})

        CREATE
            (p)-[:TEACHES]->(sql),
            (p)-[:TEACHES]->(stats),
            (p)-[:TEACHES]->(python),
            (p)-[:TEACHES]->(database)
        """)

        # ------------------------------------------------------------
        # Frontend Dashboard
        # Skills: React, JavaScript, Git
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'Frontend Dashboard'}),
            (react:Skill {name: 'React'}),
            (js:Skill {name: 'JavaScript'}),
            (git:Skill {name: 'Git'})

        CREATE
            (p)-[:TEACHES]->(react),
            (p)-[:TEACHES]->(js),
            (p)-[:TEACHES]->(git)
        """)

        # ------------------------------------------------------------
        # Sales Analytics Pipeline
        # Skills: Python, SQL, Statistics, Database Design
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'Sales Analytics Pipeline'}),
            (python:Skill {name: 'Python'}),
            (sql:Skill {name: 'SQL'}),
            (stats:Skill {name: 'Statistics'}),
            (database:Skill {name: 'Database Design'})

        CREATE
            (p)-[:TEACHES]->(python),
            (p)-[:TEACHES]->(sql),
            (p)-[:TEACHES]->(stats),
            (p)-[:TEACHES]->(database)
        """)

        # ------------------------------------------------------------
        # Customer Churn Analysis
        # Skills: Python, SQL, Statistics
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'Customer Churn Analysis'}),
            (python:Skill {name: 'Python'}),
            (sql:Skill {name: 'SQL'}),
            (stats:Skill {name: 'Statistics'})

        CREATE
            (p)-[:TEACHES]->(python),
            (p)-[:TEACHES]->(sql),
            (p)-[:TEACHES]->(stats)
        """)

        # ============================================================
        # 5. PROJECT → TECHNOLOGY RELATIONSHIPS
        # ============================================================

        # ------------------------------------------------------------
        # REST API Project → Flask + PostgreSQL
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'REST API Project'}),
            (flask:Technology {name: 'Flask'}),
            (postgres:Technology {name: 'PostgreSQL'})

        CREATE
            (p)-[:USES]->(flask),
            (p)-[:USES]->(postgres)
        """)

        # ------------------------------------------------------------
        # URL Shortener → Redis + Docker
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'URL Shortener'}),
            (redis:Technology {name: 'Redis'}),
            (docker:Technology {name: 'Docker'})

        CREATE
            (p)-[:USES]->(redis),
            (p)-[:USES]->(docker)
        """)

        # ------------------------------------------------------------
        # Analytics Dashboard → Power BI + PostgreSQL + Pandas
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'Analytics Dashboard'}),
            (powerbi:Technology {name: 'Power BI'}),
            (postgres:Technology {name: 'PostgreSQL'}),
            (pandas:Technology {name: 'Pandas'})

        CREATE
            (p)-[:USES]->(powerbi),
            (p)-[:USES]->(postgres),
            (p)-[:USES]->(pandas)
        """)

        # ------------------------------------------------------------
        # Frontend Dashboard → React
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'Frontend Dashboard'}),
            (reactTech:Technology {name: 'React'})

        CREATE
            (p)-[:USES]->(reactTech)
        """)

        # ------------------------------------------------------------
        # Sales Analytics Pipeline → Pandas + PostgreSQL
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'Sales Analytics Pipeline'}),
            (pandas:Technology {name: 'Pandas'}),
            (postgres:Technology {name: 'PostgreSQL'})

        CREATE
            (p)-[:USES]->(pandas),
            (p)-[:USES]->(postgres)
        """)

        # ------------------------------------------------------------
        # Customer Churn Analysis → Pandas + PostgreSQL
        # ------------------------------------------------------------

        session.run("""
        MATCH
            (p:Project {name: 'Customer Churn Analysis'}),
            (pandas:Technology {name: 'Pandas'}),
            (postgres:Technology {name: 'PostgreSQL'})

        CREATE
            (p)-[:USES]->(pandas),
            (p)-[:USES]->(postgres)
        """)

    print("========================================")
    print(" CareerGraph database seeded successfully")
    print("========================================")
    print("Roles:         3")
    print("Skills:        9")
    print("Technologies:  7")
    print("Projects:      6")
    print("========================================")


if __name__ == "__main__":
    seed()