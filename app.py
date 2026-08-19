from flask import Flask, render_template, request, jsonify
from database import run_query

app = Flask(__name__)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# HEALTH CHECK
# Useful for deployment / debugging
# ============================================================

@app.route("/api/health")
def health():

    try:
        result = run_query("""
            RETURN 1 AS status
        """)

        if result:
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "service": "CareerGraph API"
            })

        return jsonify({
            "status": "unhealthy",
            "database": "unavailable",
            "service": "CareerGraph API"
        }), 503

    except Exception as error:

        print("Health check error:", error)

        return jsonify({
            "status": "unhealthy",
            "database": "unavailable",
            "service": "CareerGraph API"
        }), 503


# ============================================================
# GET ALL CAREER ROLES
# ============================================================

@app.route("/api/roles")
def roles():

    result = run_query("""
        MATCH (r:Role)
        RETURN r.name AS name
        ORDER BY name
    """)

    return jsonify(result)


# ============================================================
# CAREER RECOMMENDATIONS
#
# Graph path:
#
# Role
#   ↓ REQUIRES
# Skill
#   ↑ TEACHES
# Project
#   ↓ USES
# Technology
#
# The query finds projects that teach skills required by
# the selected role and the technologies those projects use.
# ============================================================

@app.route("/api/recommendations")
def recommendations():

    role = request.args.get("role", "").strip()

    if not role:
        return jsonify({
            "error": "Role is required"
        }), 400

    result = run_query("""
        MATCH (r:Role {name: $role})
              -[:REQUIRES]->(s:Skill)

        OPTIONAL MATCH (p:Project)
              -[:TEACHES]->(s)

        OPTIONAL MATCH (p)
              -[:USES]->(t:Technology)

        RETURN
            r.name AS role,
            s.name AS skill,
            collect(DISTINCT p.name) AS projects,
            collect(DISTINCT t.name) AS technologies

        ORDER BY skill
    """, role=role)

    if not result:
        return jsonify({
            "error": f"No career data found for role: {role}"
        }), 404

    return jsonify(result)


# ============================================================
# CAREER GRAPH
#
# Returns a frontend-friendly graph structure:
#
# nodes:
#   Role
#   Skill
#   Project
#   Technology
#
# relationships:
#   Role     -REQUIRES-> Skill
#   Project  -TEACHES-> Skill
#   Project  -USES-> Technology
#
# Only the graph connected to the selected role is returned.
# ============================================================

@app.route("/api/graph")
def graph():

    role = request.args.get("role", "").strip()

    if not role:
        return jsonify({
            "error": "Role is required"
        }), 400

    rows = run_query("""
        MATCH (r:Role {name: $role})
              -[:REQUIRES]->(s:Skill)

        OPTIONAL MATCH (p:Project)
              -[:TEACHES]->(s)

        OPTIONAL MATCH (p)
              -[:USES]->(t:Technology)

        RETURN
            r.name AS role,
            s.name AS skill,
            p.name AS project,
            t.name AS technology
    """, role=role)

    if not rows:
        return jsonify({
            "nodes": [],
            "relationships": []
        })

    nodes = {}
    relationships = {}

    # --------------------------------------------------------
    # Add node safely without duplicates
    # --------------------------------------------------------

    def add_node(node_id, label, node_type):

        if not node_id or not label:
            return

        if node_id not in nodes:

            nodes[node_id] = {
                "id": node_id,
                "label": label,
                "type": node_type
            }

    # --------------------------------------------------------
    # Add relationship safely without duplicates
    # --------------------------------------------------------

    def add_relationship(source, target, rel_type):

        if not source or not target:
            return

        relationship_id = f"{source}-{rel_type}-{target}"

        if relationship_id not in relationships:

            relationships[relationship_id] = {
                "id": relationship_id,
                "source": source,
                "target": target,
                "type": rel_type
            }

    # --------------------------------------------------------
    # Build graph
    # --------------------------------------------------------

    for row in rows:

        role_name = row.get("role")
        skill_name = row.get("skill")
        project_name = row.get("project")
        technology_name = row.get("technology")

        # ====================================================
        # ROLE
        # ====================================================

        role_id = f"role:{role_name}"

        add_node(
            role_id,
            role_name,
            "Role"
        )

        # ====================================================
        # SKILL
        # ====================================================

        skill_id = None

        if skill_name:

            skill_id = f"skill:{skill_name}"

            add_node(
                skill_id,
                skill_name,
                "Skill"
            )

            add_relationship(
                role_id,
                skill_id,
                "REQUIRES"
            )

        # ====================================================
        # PROJECT
        # ====================================================

        project_id = None

        if project_name:

            project_id = f"project:{project_name}"

            add_node(
                project_id,
                project_name,
                "Project"
            )

            if skill_id:

                add_relationship(
                    project_id,
                    skill_id,
                    "TEACHES"
                )

        # ====================================================
        # TECHNOLOGY
        # ====================================================

        if technology_name and project_id:

            technology_id = f"technology:{technology_name}"

            add_node(
                technology_id,
                technology_name,
                "Technology"
            )

            add_relationship(
                project_id,
                technology_id,
                "USES"
            )

    return jsonify({
        "nodes": list(nodes.values()),
        "relationships": list(relationships.values())
    })


# ============================================================
# CAREER STATISTICS
#
# Returns authoritative statistics for the selected role.
#
# skills:
#   Number of required skills
#
# projects:
#   Number of unique projects connected to those skills
#
# technologies:
#   Number of unique technologies used by those projects
#
# connections:
#   Actual number of unique graph relationships
# ============================================================

@app.route("/api/stats")
def stats():

    role = request.args.get("role", "").strip()

    if not role:
        return jsonify({
            "error": "Role is required"
        }), 400

    # --------------------------------------------------------
    # Count unique nodes
    # --------------------------------------------------------

    result = run_query("""
        MATCH (r:Role {name: $role})
              -[:REQUIRES]->(s:Skill)

        OPTIONAL MATCH (p:Project)
              -[:TEACHES]->(s)

        OPTIONAL MATCH (p)
              -[:USES]->(t:Technology)

        RETURN
            count(DISTINCT s) AS skills,
            count(DISTINCT p) AS projects,
            count(DISTINCT t) AS technologies

    """, role=role)

    if not result:

        return jsonify({
            "skills": 0,
            "projects": 0,
            "technologies": 0,
            "connections": 0
        })

    data = result[0]

    skills = data.get("skills", 0) or 0
    projects = data.get("projects", 0) or 0
    technologies = data.get("technologies", 0) or 0

    # --------------------------------------------------------
    # Count actual relationships
    #
    # Role    -> Skill
    # Project -> Skill
    # Project -> Technology
    #
    # DISTINCT prevents duplicate rows from inflating counts.
    # --------------------------------------------------------

    edge_result = run_query("""
        MATCH (r:Role {name: $role})
              -[rs:REQUIRES]->(s:Skill)

        OPTIONAL MATCH (p:Project)
              -[tp:TEACHES]->(s)

        OPTIONAL MATCH (p)
              -[ut:USES]->(t:Technology)

        RETURN
            count(DISTINCT rs) +
            count(DISTINCT tp) +
            count(DISTINCT ut) AS connections

    """, role=role)

    connections = 0

    if edge_result:

        connections = edge_result[0].get(
            "connections",
            0
        ) or 0

    return jsonify({
        "skills": skills,
        "projects": projects,
        "technologies": technologies,
        "connections": connections
    })


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):

    print("Application error:", error)

    return jsonify({
        "error": "An internal server error occurred."
    }), 500


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )