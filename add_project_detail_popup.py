from pathlib import Path
import re
import shutil

front = Path("frontend/src")
app = front / "App.jsx"
css = front / "App.css"

if not app.exists() or not css.exists():
    raise SystemExit("ERROR: frontend/src/App.jsx or App.css was not found.")

code = app.read_text(encoding="utf-8")
styles = css.read_text(encoding="utf-8")

# Avoid applying the patch twice.
if "BuildWise AI — project detail popup" in code:
    print("Project Detail Popup is already installed.")
    raise SystemExit(0)

# Confirm expected code exists before making changes.
state_marker = 'const [expanded, setExpanded] = useState(null);'
card_marker = '<article className="project-card" key={project.id}>'

if state_marker not in code or card_marker not in code:
    raise SystemExit(
        "ERROR: Expected code was not found. No files changed. "
        "Please share the latest App.jsx."
    )

# Back up the real frontend files.
shutil.copy2(app, front / "App.jsx.before-detail-popup")
shutil.copy2(css, front / "App.css.before-detail-popup")

code = code.replace(
    state_marker,
    state_marker + '\n  const [detailProject, setDetailProject] = useState(null);',
    1
)

code = code.replace(
    card_marker,
    '<article className="project-card" id={`project-card-${project.id}`} key={project.id}>',
    1
)

# Add a details button without removing the existing roadmap button.
pattern = (
    r'(<div className="project-card-bottom">.*?)(<button className="text-button" '
    r'onClick=\{\(\) => setExpanded\(expanded === project\.id \? null : project\.id\)\})'
)
replacement = (
    r'\1<button className="detail-button" '
    r'onClick={() => setDetailProject(project)}>View details <span>↗</span></button>'
    r'\2'
)
code, count = re.subn(pattern, replacement, code, count=1, flags=re.S)

if count != 1:
    raise SystemExit(
        "ERROR: Could not locate the project card button. "
        "Original files remain backed up; no popup code was saved."
    )

# Add the popup inside the main app container.
modal = r'''
      {/* BuildWise AI — project detail popup */}
      {detailProject && (() => {
        const completed = roadmapProgress[detailProject.id] || [];
        const progress = Math.round(
          (completed.length / detailProject.steps.length) * 100
        );

        return (
          <div
            className="project-detail-overlay"
            onClick={() => setDetailProject(null)}
          >
            <section
              className="project-detail-modal"
              role="dialog"
              aria-modal="true"
              aria-labelledby="project-detail-title"
              onClick={(event) => event.stopPropagation()}
            >
              <button
                className="detail-close"
                onClick={() => setDetailProject(null)}
                aria-label="Close project details"
              >×</button>

              <div className="detail-eyebrow">
                <span>{detailProject.icon}</span> PROJECT DEEP DIVE
              </div>

              <h2 id="project-detail-title">{detailProject.name}</h2>
              <p className="detail-description">{detailProject.description}</p>

              <div className="detail-stats">
                <div>
                  <span>DIFFICULTY</span>
                  <strong>{detailProject.level}</strong>
                </div>
                <div>
                  <span>ESTIMATED TIME</span>
                  <strong>{detailProject.time}</strong>
                </div>
                <div>
                  <span>CORE SKILLS</span>
                  <strong>{detailProject.skills.length} skills</strong>
                </div>
              </div>

              <h3>Skills you'll work with</h3>
              <div className="detail-skill-list">
                {detailProject.skills.map((skill) => (
                  <span key={skill}>{skill}</span>
                ))}
              </div>

              <div className="detail-roadmap-heading">
                <div>
                  <h3>Your learning roadmap</h3>
                  <p>Small steps, real progress.</p>
                </div>
                <strong>{progress}%</strong>
              </div>

              <div className="detail-progress-track">
                <div style={{ width: `${progress}%` }} />
              </div>

              <div className="detail-steps">
                {detailProject.steps.map((step, index) => (
                  <label
                    className={`detail-step ${
                      completed.includes(index) ? "completed" : ""
                    }`}
                    key={`${detailProject.id}-${index}`}
                  >
                    <input
                      type="checkbox"
                      checked={completed.includes(index)}
                      onChange={() => toggleRoadmapStep(detailProject.id, index)}
                    />
                    <span className="detail-step-number">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <span className="detail-step-text">{step}</span>
                  </label>
                ))}
              </div>

              {progress === 100 && (
                <p className="detail-complete-message">
                  ✨ Amazing! You've completed every roadmap step.
                </p>
              )}

              <button
                className="detail-primary-button"
                onClick={() => {
                  const projectId = detailProject.id;
                  setExpanded(projectId);
                  setActiveTab("Discover");
                  setDetailProject(null);
                  setTimeout(() => {
                    document.getElementById(`project-card-${projectId}`)
                      ?.scrollIntoView({ behavior: "smooth", block: "center" });
                  }, 100);
                }}
              >
                Continue with project <span>↗</span>
              </button>
            </section>
          </div>
        );
      })()}
'''

return_start = code.rfind("  return (")
return_end = code.find("\n  );", return_start)
closing_div = code.rfind("</div>", return_start, return_end)

if return_start == -1 or return_end == -1 or closing_div == -1:
    raise SystemExit(
        "ERROR: Could not safely locate the main app container. "
        "No updated App.jsx was saved."
    )

code = code[:closing_div] + modal + "\n    " + code[closing_div:]

popup_css = r'''

/* BuildWise AI — project detail popup */
.project-card-bottom {
  flex-wrap: wrap;
}

.detail-button {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 9px 12px;
  border: 1px solid rgba(151, 126, 255, .32);
  border-radius: 10px;
  color: #c5b5ff;
  background: rgba(125, 91, 255, .09);
  font: inherit;
  font-size: 12px;
  font-weight: 650;
  cursor: pointer;
  transition: background .2s, border-color .2s, transform .2s;
}

.detail-button:hover {
  background: rgba(125, 91, 255, .19);
  border-color: rgba(170, 145, 255, .65);
  transform: translateY(-1px);
}

.project-detail-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 22px;
  overflow-y: auto;
  background: rgba(5, 7, 22, .78);
  backdrop-filter: blur(12px);
  animation: detailFadeIn .2s ease;
}

.project-detail-modal {
  position: relative;
  width: min(100%, 650px);
  max-height: min(88vh, 900px);
  overflow-y: auto;
  padding: clamp(22px, 4vw, 38px);
  border: 1px solid rgba(161, 137, 255, .32);
  border-radius: 24px;
  color: #f2f0ff;
  background:
    radial-gradient(ellipse at 100% 0%, rgba(112, 76, 255, .20), transparent 42%),
    linear-gradient(145deg, #15162f, #0d1021 72%);
  box-shadow: 0 30px 100px rgba(0, 0, 0, .48);
  animation: detailSlideIn .25s ease;
}

.detail-close {
  position: absolute;
  top: 17px;
  right: 18px;
  width: 38px;
  height: 38px;
  border: 1px solid rgba(255, 255, 255, .12);
  border-radius: 12px;
  color: #e5e0ff;
  background: rgba(255, 255, 255, .06);
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
}

.detail-eyebrow {
  display: flex;
  align-items: center;
  gap: 9px;
  margin: 2px 45px 14px 0;
  color: #b9a5ff;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1.7px;
}

.detail-eyebrow span {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border: 1px solid rgba(163, 132, 255, .3);
  border-radius: 10px;
  background: rgba(132, 96, 255, .13);
  font-size: 17px;
}

.project-detail-modal h2 {
  margin: 0 0 12px;
  color: #fff;
  font-size: clamp(25px, 4vw, 35px);
  line-height: 1.18;
  letter-spacing: -.9px;
}

.detail-description {
  margin: 0;
  color: #aaaec9;
  font-size: 14px;
  line-height: 1.8;
}

.detail-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin: 25px 0;
}

.detail-stats > div {
  min-width: 0;
  padding: 15px 12px;
  border: 1px solid rgba(157, 145, 217, .16);
  border-radius: 14px;
  background: rgba(255, 255, 255, .035);
}

.detail-stats span {
  display: block;
  margin-bottom: 8px;
  color: #858aaa;
  font-size: 9px;
  font-weight: 750;
  letter-spacing: 1px;
}

.detail-stats strong {
  color: #e5ddff;
  font-size: 13px;
  overflow-wrap: anywhere;
}

.project-detail-modal h3 {
  margin: 24px 0 13px;
  color: #f2f0ff;
  font-size: 15px;
  letter-spacing: -.2px;
}

.detail-skill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.detail-skill-list span {
  padding: 8px 11px;
  border: 1px solid rgba(131, 111, 255, .25);
  border-radius: 9px;
  color: #c9bdff;
  background: rgba(119, 91, 255, .1);
  font-size: 12px;
}

.detail-roadmap-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 15px;
  margin-top: 28px;
}

.detail-roadmap-heading h3 {
  margin: 0 0 5px;
}

.detail-roadmap-heading p {
  margin: 0;
  color: #8e93b2;
  font-size: 12px;
}

.detail-roadmap-heading > strong {
  color: #bcaaff;
  font-size: 22px;
}

.detail-progress-track {
  height: 6px;
  margin: 15px 0 18px;
  overflow: hidden;
  border-radius: 99px;
  background: rgba(255, 255, 255, .09);
}

.detail-progress-track > div {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #7861ff, #bd8bff);
  transition: width .25s ease;
}

.detail-steps {
  display: grid;
  gap: 9px;
}

.detail-step {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px;
  border: 1px solid rgba(150, 145, 200, .13);
  border-radius: 12px;
  background: rgba(255, 255, 255, .025);
  cursor: pointer;
  transition: border-color .2s, background .2s;
}

.detail-step:hover {
  border-color: rgba(153, 126, 255, .4);
  background: rgba(132, 101, 255, .06);
}

.detail-step input {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  accent-color: #9677ff;
  cursor: pointer;
}

.detail-step-number {
  color: #8e82c5;
  font-size: 11px;
  font-weight: 800;
}

.detail-step-text {
  color: #d9d9ee;
  font-size: 13px;
  line-height: 1.5;
}

.detail-step.completed .detail-step-text {
  color: #9297b1;
  text-decoration: line-through;
}

.detail-complete-message {
  padding: 12px 14px;
  border: 1px solid rgba(119, 220, 180, .22);
  border-radius: 11px;
  color: #a7f0cf;
  background: rgba(70, 190, 140, .08);
  font-size: 13px;
}

.detail-primary-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  width: 100%;
  margin-top: 24px;
  padding: 15px 18px;
  border: 0;
  border-radius: 12px;
  color: #fff;
  background: linear-gradient(105deg, #7657f5, #985cf5);
  box-shadow: 0 8px 25px rgba(119, 81, 245, .2);
  font: inherit;
  font-size: 13px;
  font-weight: 750;
  cursor: pointer;
  transition: filter .2s, transform .2s;
}

.detail-primary-button:hover {
  filter: brightness(1.12);
  transform: translateY(-1px);
}

@keyframes detailFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes detailSlideIn {
  from { opacity: 0; transform: translateY(12px) scale(.99); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

@media (max-width: 520px) {
  .project-detail-overlay {
    padding: 10px;
  }

  .project-detail-modal {
    max-height: 94vh;
    padding: 22px 17px;
    border-radius: 19px;
  }

  .detail-stats {
    gap: 7px;
  }

  .detail-stats > div {
    padding: 12px 8px;
  }

  .detail-stats span {
    font-size: 8px;
  }

  .detail-stats strong {
    font-size: 11px;
  }
}
'''

if "BuildWise AI — project detail popup" not in styles:
    styles += "\n" + popup_css

app.write_text(code, encoding="utf-8")
css.write_text(styles, encoding="utf-8")

print("SUCCESS: Project Detail Popup installed.")
print("Backup files: App.jsx.before-detail-popup and App.css.before-detail-popup")
print("Refresh http://localhost:5174")
print("Test: click View details, tick roadmap steps, close popup, and reopen it.")
