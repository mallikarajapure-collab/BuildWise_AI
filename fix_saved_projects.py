from pathlib import Path

path = Path("src/App.jsx")
code = path.read_text(encoding="utf-8")

old_state = '''  const [search, setSearch] = useState("");'''
new_state = '''  const [search, setSearch] = useState("");
  const [savedProjects, setSavedProjects] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("buildwise-saved-projects") || "[]");
    } catch {
      return [];
    }
  });

  const toggleSaved = (projectId) => {
    setSavedProjects((current) => {
      const updated = current.includes(projectId)
        ? current.filter((id) => id !== projectId)
        : [...current, projectId];
      localStorage.setItem("buildwise-saved-projects", JSON.stringify(updated));
      return updated;
    });
  };'''

old_heart = '''<button className="save-button" title="Save project" onClick={(e) => e.currentTarget.classList.toggle("saved")}>♡</button>'''
new_heart = '''<button className={`save-button ${savedProjects.includes(project.id) ? "saved" : ""}`} title={savedProjects.includes(project.id) ? "Remove saved project" : "Save project"} aria-label={savedProjects.includes(project.id) ? "Remove saved project" : "Save project"} onClick={() => toggleSaved(project.id)}>{savedProjects.includes(project.id) ? "♥" : "♡"}</button>'''

old_placeholder = '''            <p>{activeTab === "Saved" ? "Use the heart icon on a project to mark it for later." : "Open a project's roadmap to explore its milestones."}</p>'''
new_placeholder = '''            {activeTab === "Saved" ? (
              savedProjects.length === 0 ? (
                <p>No saved projects yet. Go back to discovery and tap a project's heart icon.</p>
              ) : (
                <div className="saved-project-list">
                  {PROJECTS.filter((project) => savedProjects.includes(project.id)).map((project) => (
                    <article className="project-card" key={project.id}>
                      <div className="project-card-top">
                        <div className={`project-icon ${project.color}`}>{project.icon}</div>
                        <div className="project-title-wrap">
                          <div className="project-tags"><span>{project.category}</span></div>
                          <h3>{project.name}</h3>
                        </div>
                        <button className="save-button saved" title="Remove saved project" aria-label="Remove saved project" onClick={() => toggleSaved(project.id)}>♥</button>
                      </div>
                      <p className="project-description">{project.description}</p>
                      <div className="project-skills">{project.skills.map((skill) => <span key={skill}>{skill}</span>)}</div>
                      <button className="text-button" onClick={() => { setActiveTab("Discover"); setExpanded(project.id); }}>Explore project ↗</button>
                    </article>
                  ))}
                </div>
              )
            ) : (
              <p>Open a project's roadmap to explore its milestones.</p>
            )}'''

for old, new, label in [
    (old_state, new_state, "saved-project state"),
    (old_heart, new_heart, "heart button"),
    (old_placeholder, new_placeholder, "saved-project display"),
]:
    if old not in code:
        raise SystemExit(f"STOP: Could not find the expected {label}. Original file has not been changed.")
    code = code.replace(old, new, 1)

path.write_text(code, encoding="utf-8")
print("Saved Projects fix applied successfully.")
