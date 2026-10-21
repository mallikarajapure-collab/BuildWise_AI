import { useMemo, useState } from "react";
import "./App.css";

const PROJECTS = [
  {
    id: 1,
    name: "AI Project Discovery Assistant",
    category: "AI / ML",
    level: "Beginner",
    time: "1–2 weeks",
    icon: "✦",
    color: "violet",
    description: "Build an intelligent assistant that helps developers discover projects based on their interests, skills and career goals.",
    skills: ["Python", "React", "FastAPI"],
    steps: ["Define project requirements", "Build the React interface", "Create recommendation APIs", "Connect frontend and backend", "Test and document the project"],
    popular: true,
  },
  {
    id: 2,
    name: "ML Model Performance Auditor",
    category: "AI / ML",
    level: "Advanced",
    time: "3–5 weeks",
    icon: "◈",
    color: "blue",
    description: "Analyze machine-learning evaluation results and flag potential data leakage, suspicious metrics and unreliable model performance.",
    skills: ["Python", "Pandas", "Scikit-learn"],
    steps: ["Prepare sample datasets", "Calculate evaluation metrics", "Build data-leakage checks", "Create an analysis dashboard", "Test against known cases"],
    popular: true,
  },
  {
    id: 3,
    name: "GitHub Portfolio Analyzer",
    category: "Developer Tools",
    level: "Intermediate",
    time: "2–3 weeks",
    icon: "⌘",
    color: "cyan",
    description: "Evaluate public repositories, programming activity and project evidence to identify portfolio strengths and skill gaps.",
    skills: ["Python", "REST API", "React"],
    steps: ["Connect to the GitHub API", "Collect repository data", "Calculate portfolio indicators", "Display skill evidence", "Test with different profiles"],
    popular: false,
  },
  {
    id: 4,
    name: "AI Document Question Answering",
    category: "Generative AI",
    level: "Advanced",
    time: "3–5 weeks",
    icon: "▤",
    color: "pink",
    description: "Create a document assistant that retrieves relevant information and answers questions using supplied documents.",
    skills: ["Python", "LLMs", "Embeddings"],
    steps: ["Accept document uploads", "Extract and split text", "Create document embeddings", "Retrieve relevant passages", "Generate grounded answers"],
    popular: true,
  },
  {
    id: 5,
    name: "Smart Study Planner",
    category: "Productivity",
    level: "Beginner",
    time: "1–2 weeks",
    icon: "◷",
    color: "orange",
    description: "Organize subjects, deadlines and available study hours into a practical study schedule with progress tracking.",
    skills: ["Python", "Basic Logic", "React"],
    steps: ["Create a subject form", "Add deadlines and priorities", "Generate a weekly schedule", "Display study progress", "Test scheduling rules"],
    popular: false,
  },
  {
    id: 6,
    name: "Personal Expense Dashboard",
    category: "Data Analytics",
    level: "Beginner",
    time: "1–2 weeks",
    icon: "▥",
    color: "green",
    description: "Explore spending patterns through category summaries, monthly comparisons and interactive financial visualizations.",
    skills: ["Python", "Pandas", "Data Visualization"],
    steps: ["Prepare expense data", "Categorize transactions", "Calculate monthly totals", "Build visual summaries", "Validate calculations"],
    popular: false,
  },
];

const INTERESTS = ["AI / ML", "Generative AI", "Developer Tools", "Productivity", "Data Analytics"];
const SKILLS = ["Python", "Java", "SQL", "React", "FastAPI", "Pandas", "Scikit-learn", "REST API", "LLMs", "Git"];

function App() {
  const [interests, setInterests] = useState(["AI / ML", "Generative AI"]);
  const [level, setLevel] = useState("Intermediate");
  const [time, setTime] = useState("Any");
  const [goal, setGoal] = useState("Get an internship");
  const [skills, setSkills] = useState(["Python"]);
  const [searched, setSearched] = useState(false);
  const [activeTab, setActiveTab] = useState("Discover");
  const [expanded, setExpanded] = useState(null);
  const [search, setSearch] = useState("");
  const [savedProjects, setSavedProjects] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("buildwise-saved-projects") || "[]");
    } catch {
      return [];
    }
  });

  const [roadmapProgress, setRoadmapProgress] = useState(() => {
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

  const toggleSaved = (projectId) => {
    setSavedProjects((current) => {
      const updated = current.includes(projectId)
        ? current.filter((id) => id !== projectId)
        : [...current, projectId];
      localStorage.setItem("buildwise-saved-projects", JSON.stringify(updated));
      return updated;
    });
  };

  const results = useMemo(() => {
    const levels = { Beginner: 1, Intermediate: 2, Advanced: 3 };
    let list = PROJECTS.filter((p) => {
      const interestMatch = interests.length === 0 ||
        interests.includes(p.category) ||
        (p.category === "Generative AI" && interests.includes("AI / ML"));
      const levelMatch = levels[p.level] <= levels[level];
      const timeMatch = time === "Any" || p.time === time;
      const searchMatch = `${p.name} ${p.description} ${p.category} ${p.skills.join(" ")}`
        .toLowerCase().includes(search.toLowerCase());
      return interestMatch && levelMatch && timeMatch && searchMatch;
    });

    if (list.length === 0 && searched) {
      list = PROJECTS.filter((p) =>
        levels[p.level] <= levels[level] &&
        `${p.name} ${p.description} ${p.category}`.toLowerCase().includes(search.toLowerCase())
      );
    }

    return [...list].sort((a, b) =>
      b.skills.filter((s) => skills.includes(s)).length -
      a.skills.filter((s) => skills.includes(s)).length
    );
  }, [interests, level, time, skills, search, searched]);

  const toggleInterest = (item) => {
    setInterests((old) =>
      old.includes(item) ? old.filter((x) => x !== item) : [...old, item]
    );
  };

  const toggleSkill = (item) => {
    setSkills((old) =>
      old.includes(item) ? old.filter((x) => x !== item) : [...old, item]
    );
  };

  const discover = () => {
    setSearched(true);
    setActiveTab("Discover");
    document.getElementById("recommendations")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#top">
          <span className="brand-mark">B<span>✦</span></span>
          <span className="brand-copy">BuildWise<span>AI</span><small>PROJECT INTELLIGENCE</small></span>
        </a>

        <div className="side-label">WORKSPACE</div>
        <nav className="side-nav">
          <button className={activeTab === "Discover" ? "nav-item active" : "nav-item"} onClick={() => setActiveTab("Discover")}>
            <span>✳</span> Discover projects <span className="nav-arrow">↗</span>
          </button>
          <button className={activeTab === "Saved" ? "nav-item active" : "nav-item"} onClick={() => setActiveTab("Saved")}>
            <span>♡</span> Saved projects
          </button>
          <button className={activeTab === "Roadmap" ? "nav-item active" : "nav-item"} onClick={() => setActiveTab("Roadmap")}>
            <span>⌁</span> Learning roadmap
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <div className="upgrade-icon">✦</div>
            <strong>Build something<br />remarkable.</strong>
            <p>Turn your skills into projects that matter.</p>
            <span className="upgrade-tag">YOUR NEXT CHAPTER ↗</span>
          </div>
          <div className="profile">
            <div className="avatar">B</div>
            <div><strong>Project workspace</strong><small>Personal edition</small></div>
            <span className="online-dot" />
          </div>
        </div>
      </aside>

      <main className="main-content" id="top">
        <header className="topbar">
          <div className="breadcrumb">Workspace <span>/</span> <strong>{activeTab}</strong></div>
          <div className="top-actions">
            <span className="status-pill"><i /> Discovery workspace</span>
            <button className="icon-button" title="Notifications">♧</button>
            <div className="mini-avatar">M</div>
          </div>
        </header>

        {activeTab === "Discover" ? (
          <>
            <section className="hero">
              <div className="hero-glow glow-one" />
              <div className="hero-glow glow-two" />
              <div className="hero-content">
                <div className="eyebrow"><span className="sparkle">✦</span> YOUR PERSONAL PROJECT INTELLIGENCE</div>
                <h1>Big ideas start<br />with <span>the right project.</span></h1>
                <p>Discover meaningful projects matched to your skills, interests and career ambitions.</p>
                <div className="hero-actions">
                  <button className="primary-button" onClick={discover}>Find my next project <span>↗</span></button>
                  <span className="hero-note"><span className="tiny-check">✓</span> Personalized for your goals</span>
                </div>
              </div>
              <div className="hero-art" aria-hidden="true">
                <div className="orbit orbit-one" />
                <div className="orbit orbit-two" />
                <div className="art-core"><span>✦</span></div>
                <div className="float-card float-top"><span className="float-icon purple">✳</span><div><strong>Ideas to build</strong><small>Discover your potential</small></div></div>
                <div className="float-card float-bottom"><span className="float-icon blue">↗</span><div><strong>Skills in motion</strong><small>One project at a time</small></div></div>
                <span className="art-star star-one">✧</span><span className="art-star star-two">✦</span>
              </div>
              <div className="hero-bottom"><span>01 <i /> DISCOVER</span><span>02 <i /> BUILD</span><span>03 <i /> GROW</span></div>
            </section>

            <section className="stats-row">
              <div className="stat-block"><span className="stat-icon violet-bg">✦</span><div><strong>06</strong><small>Curated project ideas</small></div></div>
              <div className="stat-block"><span className="stat-icon blue-bg">⌘</span><div><strong>05</strong><small>Skill categories</small></div></div>
              <div className="stat-block"><span className="stat-icon pink-bg">↗</span><div><strong>01</strong><small>Next step starts here</small></div></div>
              <div className="stat-note"><span className="pulse-dot" /> A little progress adds up.</div>
            </section>

            <section className="discovery-layout">
              <div className="preferences-panel">
                <div className="section-heading"><div><span className="section-kicker">LET'S PERSONALIZE</span><h2>Tell us about you.</h2></div><span className="step-count">01 / 02</span></div>
                <p className="panel-intro">A few details help us find projects worth your time.</p>

                <div className="field-group">
                  <label>01 <span>What interests you?</span></label>
                  <div className="interest-grid">
                    {INTERESTS.map((item, i) => (
                      <button key={item} className={`interest-chip ${interests.includes(item) ? "selected" : ""}`} onClick={() => toggleInterest(item)}>
                        <span>{["✦", "◈", "⌘", "◷", "▥"][i]}</span>{item}
                        {interests.includes(item) && <b>✓</b>}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="field-group">
                  <label>02 <span>Your coding level</span></label>
                  <div className="level-options">
                    {["Beginner", "Intermediate", "Advanced"].map((item, i) => (
                      <button key={item} className={`level-option ${level === item ? "selected" : ""}`} onClick={() => setLevel(item)}>
                        <span className="level-symbol">{["◌", "◉", "✳"][i]}</span><strong>{item}</strong><small>{["Getting started", "Building confidence", "Ready to go deeper"][i]}</small>
                      </button>
                    ))}
                  </div>
                </div>

                <div className="field-row">
                  <div className="field-group">
                    <label>03 <span>Available time</span></label>
                    <select value={time} onChange={(e) => setTime(e.target.value)}>
                      <option>Any</option><option>1–2 weeks</option><option>2–3 weeks</option><option>3–5 weeks</option>
                    </select>
                  </div>
                  <div className="field-group">
                    <label>04 <span>Main goal</span></label>
                    <select value={goal} onChange={(e) => setGoal(e.target.value)}>
                      <option>Get an internship</option><option>Build a portfolio</option><option>Learn a new skill</option><option>Prepare for placements</option>
                    </select>
                  </div>
                </div>

                <div className="field-group">
                  <label>05 <span>Skills you already know</span><small>Choose any that apply</small></label>
                  <div className="skill-chips">
                    {SKILLS.map((item) => <button key={item} className={skills.includes(item) ? "skill-chip selected" : "skill-chip"} onClick={() => toggleSkill(item)}>{skills.includes(item) ? "✓" : "+"} {item}</button>)}
                  </div>
                </div>

                <button className="primary-button discover-button" onClick={discover}>Discover my projects <span>↗</span></button>
                <p className="privacy-note">✧ Your selections personalize these recommendations.</p>
              </div>

              <div className="results-panel" id="recommendations">
                <div className="results-heading">
                  <div><span className="section-kicker">CURATED FOR YOUR JOURNEY</span><h2>{searched ? "Your project matches." : "Ideas worth exploring."}</h2></div>
                  <span className="match-count">{results.length} IDEAS</span>
                </div>
                <div className="search-box"><span>⌕</span><input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search projects or skills..." /><kbd>/</kbd></div>
                <div className="results-caption"><span>PROJECT COLLECTION</span><span>Sorted by skill match ↕</span></div>

                {results.length === 0 ? (
                  <div className="empty-state"><span>✧</span><h3>No exact matches yet</h3><p>Try selecting more interests or a different time range.</p><button className="secondary-button" onClick={() => {setInterests([]);setTime("Any");setSearch("");}}>Show more projects</button></div>
                ) : results.map((project, index) => {
                  const matched = project.skills.filter((s) => skills.includes(s));
                  const missing = project.skills.filter((s) => !skills.includes(s));
                  return (
                    <article className="project-card" key={project.id}>
                      <div className="project-card-top">
                        <div className={`project-icon ${project.color}`}>{project.icon}</div>
                        <div className="project-title-wrap"><div className="project-tags"><span>{project.category}</span>{index === 0 && <span className="best-match">✦ BEST MATCH</span>}</div><h3>{project.name}</h3></div>
                        <button className={`save-button ${savedProjects.includes(project.id) ? "saved" : ""}`} title={savedProjects.includes(project.id) ? "Remove saved project" : "Save project"} aria-label={savedProjects.includes(project.id) ? "Remove saved project" : "Save project"} onClick={() => toggleSaved(project.id)}>{savedProjects.includes(project.id) ? "♥" : "♡"}</button>
                      </div>
                      <p className="project-description">{project.description}</p>
                      <div className="project-meta"><span><i>◉</i> {project.level}</span><span><i>◷</i> {project.time}</span><span><i>⌁</i> {project.skills.length} core skills</span></div>
                      <div className="project-skills">{project.skills.map((s) => <span key={s} className={skills.includes(s) ? "matched-skill" : ""}>{skills.includes(s) && "✓ "}{s}</span>)}</div>
                      <div className="project-card-bottom"><span className="match-label"><span className="match-dot" /> {matched.length} matched · {missing.length} to explore</span><button className="text-button" onClick={() => setExpanded(expanded === project.id ? null : project.id)}>{expanded === project.id ? "Hide roadmap" : "Explore project"} <span>{expanded === project.id ? "↑" : "↗"}</span></button></div>
                      {expanded === project.id && (() => {
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
                    })()}
                    </article>
                  );
                })}
                <div className="more-note"><span>✦</span> Your next great project is a few steps away.</div>
              </div>
            </section>
          </>
        ) : (
          <section className="placeholder-page">
            <div className="placeholder-symbol">{activeTab === "Saved" ? "♡" : "⌁"}</div>
            <span className="section-kicker">BUILDWISE WORKSPACE</span>
            <h1>{activeTab === "Saved" ? "Your saved projects." : "Your learning roadmap."}</h1>
            {activeTab === "Saved" ? (
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
            )}
            <button className="primary-button" onClick={() => setActiveTab("Discover")}>Back to discovery ↗</button>
          </section>
        )}

        <footer className="footer"><a className="footer-brand" href="#top">B✦ BuildWise AI</a><span>Made for curious minds and ambitious builders.</span><span>PROJECT DISCOVERY · 2026</span></footer>
      </main>
    </div>
  );
}

export default App;
