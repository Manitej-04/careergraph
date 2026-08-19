// ============================================================
// CareerGraph - Graph Queries
// ============================================================
// Graph model:
//
// (Role)-[:REQUIRES]->(Skill)
// (Project)-[:TEACHES]->(Skill)
// (Project)-[:USES]->(Technology)
//
// The application uses these relationships to:
// 1. Explore career roles
// 2. Identify required skills
// 3. Recommend projects
// 4. Rank projects by skill coverage
// 5. Explore project technologies
// 6. Visualize multi-hop career paths
// ============================================================



// ============================================================
// 1. GET ALL CAREER ROLES
// ============================================================

MATCH (r:Role)
RETURN
    r.name AS role,
    r.category AS category
ORDER BY role;



// ============================================================
// 2. GET SKILLS REQUIRED FOR A ROLE
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (s:Skill)

RETURN
    r.name AS role,
    s.name AS skill
ORDER BY skill;



// ============================================================
// 3. RANK PROJECTS BY SKILL COVERAGE
// ============================================================
// This is one of the most important queries.
//
// A project receives a score based on how many skills it teaches
// that are required by the selected role.
//
// Example:
//
// Data Analyst requires:
// Python, SQL, Statistics, Database Design
//
// Analytics Dashboard teaches all 4.
//
// Therefore:
// skillCoverage = 4
// coveragePercent = 100
//
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (s:Skill)
      <-[:TEACHES]-
      (p:Project)

WITH
    r,
    p,
    count(DISTINCT s) AS matchingSkills

MATCH (r)-[:REQUIRES]->(required:Skill)

WITH
    r,
    p,
    matchingSkills,
    count(DISTINCT required) AS totalSkills

RETURN
    p.name AS project,
    p.difficulty AS difficulty,
    p.description AS description,
    matchingSkills,
    totalSkills,
    round(
        (toFloat(matchingSkills) / totalSkills) * 100
    ) AS coveragePercent

ORDER BY
    coveragePercent DESC,
    matchingSkills DESC,
    project;



// ============================================================
// 4. PROJECTS WITH THE SKILLS THEY COVER
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (s:Skill)
      <-[:TEACHES]-
      (p:Project)

WITH
    p,
    collect(DISTINCT s.name) AS matchingSkills

RETURN
    p.name AS project,
    matchingSkills,
    size(matchingSkills) AS skillCount

ORDER BY
    skillCount DESC,
    project;



// ============================================================
// 5. PROJECT → TECHNOLOGY EXPLORATION
// ============================================================
// Multi-hop traversal:
//
// Role
//   ↓ REQUIRES
// Skill
//   ↑ TEACHES
// Project
//   ↓ USES
// Technology
//
// This demonstrates why the graph is useful.
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (s:Skill)
      <-[:TEACHES]-
      (p:Project)
      -[:USES]->
      (t:Technology)

RETURN DISTINCT
    p.name AS project,
    t.name AS technology

ORDER BY
    project,
    technology;



// ============================================================
// 6. COMPLETE CAREER PATH
// ============================================================
// Returns the full path:
//
// Role → Skill ← Project → Technology
//
// Useful for the visual career-path section of the UI.
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (s:Skill)
      <-[:TEACHES]-
      (p:Project)
      -[:USES]->
      (t:Technology)

RETURN DISTINCT
    r.name AS role,
    s.name AS skill,
    p.name AS project,
    t.name AS technology

ORDER BY
    skill,
    project,
    technology;



// ============================================================
// 7. COUNT CONNECTED PROJECTS
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (s:Skill)
      <-[:TEACHES]-
      (p:Project)

RETURN
    r.name AS role,
    count(DISTINCT p) AS connectedProjects;



// ============================================================
// 8. ROLE GRAPH STATISTICS
// ============================================================
// Gives the UI useful summary information.
//
// Example:
//
// Data Analyst
// Required Skills: 4
// Connected Projects: 5
// Graph Connections: 17
//
// ============================================================

MATCH (r:Role {name: $role})

OPTIONAL MATCH (r)-[:REQUIRES]->(s:Skill)

WITH
    r,
    count(DISTINCT s) AS requiredSkills

OPTIONAL MATCH
    (r)-[:REQUIRES]->(skill:Skill)
    <-[:TEACHES]-(p:Project)

WITH
    r,
    requiredSkills,
    count(DISTINCT p) AS connectedProjects

OPTIONAL MATCH
    (r)-[:REQUIRES]->(:Skill)
    <-[:TEACHES]-(project:Project)
    -[:USES]->(technology:Technology)

RETURN
    r.name AS role,
    requiredSkills,
    connectedProjects,
    count(DISTINCT technology) AS connectedTechnologies;



// ============================================================
// 9. SKILL → PROJECT → TECHNOLOGY PATHS
// ============================================================
// Useful for explaining WHY a project is recommended.
//
// Instead of simply saying:
// "Analytics Dashboard is recommended"
//
// The application can explain:
//
// SQL → Analytics Dashboard → PostgreSQL
// Python → Analytics Dashboard → Pandas
// Statistics → Analytics Dashboard → Power BI
//
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (s:Skill)
      <-[:TEACHES]-
      (p:Project)
      -[:USES]->
      (t:Technology)

RETURN DISTINCT
    s.name AS skill,
    p.name AS project,
    t.name AS technology

ORDER BY
    skill,
    project;



// ============================================================
// 10. BEST PROJECT FOR EACH REQUIRED SKILL
// ============================================================
// Finds projects connected to each required skill.
//
// This is useful for a "Skill Development Roadmap" feature.
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (s:Skill)
      <-[:TEACHES]-
      (p:Project)

RETURN
    s.name AS requiredSkill,
    collect(DISTINCT p.name) AS recommendedProjects

ORDER BY
    requiredSkill;



// ============================================================
// 11. FIND PROJECTS THAT COVER MOST ROLE SKILLS
// ============================================================
// Strong recommendation query.
//
// Projects are ranked according to the number of role skills
// they cover.
//
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (requiredSkill:Skill)

WITH
    r,
    collect(requiredSkill) AS requiredSkills

MATCH (p:Project)
OPTIONAL MATCH (p)-[:TEACHES]->(skill:Skill)

WITH
    r,
    p,
    requiredSkills,
    collect(
        CASE
            WHEN skill IN requiredSkills
            THEN skill.name
        END
    ) AS matchedSkills

WITH
    r,
    p,
    [skill IN matchedSkills WHERE skill IS NOT NULL] AS skills

RETURN
    p.name AS project,
    p.difficulty AS difficulty,
    p.description AS description,
    skills,
    size(skills) AS matchingSkills,
    size(requiredSkills) AS totalSkills,
    round(
        (toFloat(size(skills)) / size(requiredSkills)) * 100
    ) AS coveragePercent

ORDER BY
    coveragePercent DESC,
    matchingSkills DESC;



// ============================================================
// 12. FIND TECHNOLOGIES USED BY PROJECTS FOR A ROLE
// ============================================================

MATCH (r:Role {name: $role})
      -[:REQUIRES]->
      (s:Skill)
      <-[:TEACHES]-
      (p:Project)
      -[:USES]->
      (t:Technology)

RETURN DISTINCT
    t.name AS technology,
    count(DISTINCT p) AS projectCount

ORDER BY
    projectCount DESC,
    technology;