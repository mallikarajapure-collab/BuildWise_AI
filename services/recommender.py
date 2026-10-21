def recommend_projects(projects, interests, level, available_time, skills):
    level_order = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }

    matches = []

    for project in projects:
        if level_order[project["level"]] > level_order[level]:
            continue

        if available_time != "Any" and project["time"] != available_time:
            continue

        category = project["category"]
        interest_match = (
            not interests
            or category in interests
            or (
                category == "Generative AI"
                and "AI / ML" in interests
            )
        )

        if interest_match:
            project_copy = project.copy()
            project_copy["skill_gaps"] = [
                skill for skill in project["skills"]
                if skill not in skills
            ]
            project_copy["matched_skills"] = [
                skill for skill in project["skills"]
                if skill in skills
            ]
            matches.append(project_copy)

    matches.sort(
        key=lambda project: len(project["matched_skills"]),
        reverse=True
    )

    return matches
