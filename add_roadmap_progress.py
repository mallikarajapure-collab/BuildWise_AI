from pathlib import Path
import re
import shutil

root = Path(".")
app = root / "src" / "App.jsx"
css = root / "src" / "App.css"
front = root / "frontend" / "src"

# Back up files before editing
shutil.copy2(app, root / "src" / "App.jsx.before-roadmap")
shutil.copy2(css, root / "src" / "App.css.before-roadmap")

code = app.read_text(encoding="utf-8")

# Add persistent roadmap progress state and toggle function
anchor = "  const toggleSaved = (projectId) => {"
addition = '''  const [roadmapProgress, setRoadmapProgress] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("buildwise-roadmap-progress") || "{}");
    } catch {
      return {};
    }
  });

  const toggleRoadmapStep = (projectId, stepIndex) => {
    setRoadmapProgress((current) => {
      const completed = current[projectId] || [];
      const nextCompleted = completed.includes(stepIndex)
        ? completed.filter((step) => step !== stepIndex)
        : [...completed, stepIndex];
      const updated = { ...current, [projectId]: nextCompleted };
      localStorage.setItem("buildwise-roadmap-progress", JSON.stringify(updated));
      return updated;
    });
  };

'''
if "const [roadmapProgress, setRoadmapProgress]" not in code:
    if anchor not in code:
        raise SystemExit("STOP: Could not locate the saved-project function. No roadmap changes made.")
    code = code.replace(anchor, addition + anchor, 1)

# Replace the existing roadmap with a trackable version
pattern = re.compile(
    r'\{expanded === project\.id && <div className="roadmap">.*?'
    r'<div className="roadmap-footer">Career goal:\s*<strong>\{goal\}</strong></div></div>\}',
    re.DOTALL
)

replacement = '''{expanded === project.id && (() => {
                      const completedSteps = roadmapProgress[project.id] || [];
                      const progressPercent = Math.round((completedSteps.length / project.steps.length) * 100);
                      return (
                        <div className="roadmap">
                          <div className="roadmap-title">YOUR PROJECT ROADMAP <span>{project.steps.length} STEPS</span></div>
                          <div className="roadmap-progress-heading">
                            <span>YOUR PROGRESS</span><strong>{progressPercent}% complete</strong>
                          </div>
                          <div className="roadmap-progress-track">
                            <div className="roadmap-progress-fill" style={{ width: `${progressPercent}%` }} />
                          </div>
                          <div className="roadmap-checklist">
                            {project.steps.map((step, i) => {
                              const isComplete = completedSteps.includes(i);
                              return (
                                <label className={`roadmap-step ${isComplete ? "step-complete" : ""}`} key={step}>
                                  <input
                                    type="checkbox"
                                    checked={isComplete}
                                    onChange={() => toggleRoadmapStep(project.id, i)}
                                    aria-label={`Mark step ${i + 1} complete`}
                                  />
                                  <span>{String(i + 1).padStart(2, "0")}</span>
                                  <p>{step}</p>
                                </label>
                              );
                            })}
                          </div>
                          <div className="roadmap-footer">
                            {completedSteps.length === project.steps.length && project.steps.length > 0
                              ? "🎉 Roadmap completed! Career goal: "
                              : "Career goal: "}
                            <strong>{goal}</strong>
                          </div>
                        </div>
                      );
                    })()}'''

code, count = pattern.subn(lambda _: replacement, code, count=1)
if count != 1:
    raise SystemExit("STOP: The existing roadmap layout did not match. Restore backup if needed; no updated app was copied.")

app.write_text(code, encoding="utf-8")

# Add roadmap styling without replacing existing styles
styles = r"""

/* BuildWise AI — interactive roadmap progress */
.roadmap-progress-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin: 18px 0 9px;
  color: #b9c4df;
  font-size: 11px;
  letter-spacing: .7px;
}
.roadmap-progress-heading strong {
  color: #b9a0ff;
  font-size: 12px;
  letter-spacing: 0;
}
.roadmap-progress-track {
  height: 7px;
  overflow: hidden;
  border-radius: 99px;
  background: rgba(148, 163, 184, .16);
  margin-bottom: 14px;
}
.roadmap-progress-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #6675ff, #b36bff);
  transition: width .25s ease;
}
.roadmap-checklist {
  display: grid;
  gap: 8px;
}
.roadmap-step {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid rgba(148, 163, 184, .14);
  border-radius: 12px;
  cursor: pointer;
  transition: background .2s ease, border-color .2s ease;
}
.roadmap-step:hover {
  background: rgba(113, 97, 255, .08);
  border-color: rgba(151, 126, 255, .4);
}
.roadmap-step input[type="checkbox"] {
  width: 17px;
  height: 17px;
  flex: 0 0 17px;
  accent-color: #8b72ff;
  cursor: pointer;
}
.roadmap-step > span {
  color: #9d8aff;
  font-size: 11px;
  font-weight: 700;
}
.roadmap-step p {
  margin: 0;
  color: #e1e6f5;
  font-size: 13px;
}
.roadmap-step.step-complete p {
  color: #9da9bf;
  text-decoration: line-through;
}
.roadmap-step.step-complete {
  background: rgba(112, 93, 255, .07);
}
"""

css_code = css.read_text(encoding="utf-8")
if "BuildWise AI — interactive roadmap progress" not in css_code:
    css.write_text(css_code + styles, encoding="utf-8")

# Sync the actual frontend files used by the website
shutil.copy2(app, front / "App.jsx")
shutil.copy2(css, front / "App.css")

print("SUCCESS: Interactive roadmap added and synced to frontend.")
print("Refresh http://localhost:5174")
print("Test: open a project, tick a step, check progress, then refresh the page.")
