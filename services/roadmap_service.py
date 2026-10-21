def create_roadmap(project):
    return [
        {
            "week": index,
            "task": task,
            "deliverable": (
                "A working, testable project component"
                if index < len(project.get("steps", []))
                else "Final integrated project and README"
            )
        }
        for index, task in enumerate(project.get("steps", []), start=1)
    ]
