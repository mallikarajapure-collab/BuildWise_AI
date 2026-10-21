from pathlib import Path

app_path = Path("frontend/src/App.jsx")
app = app_path.read_text(encoding="utf-8-sig")

if 'import ChatWidget from "./ChatWidget";' not in app:
    app = app.replace(
        'import "./App.css";',
        'import "./App.css";\nimport ChatWidget from "./ChatWidget";',
        1
    )

# Place the widget inside the existing root element, before its final closing div.
if "<ChatWidget />" not in app:
    end = app.rfind("export default App;")
    if end < 0:
        raise SystemExit("Could not find export default App; no widget inserted.")
    close = app.rfind("</div>", 0, end)
    if close < 0:
        raise SystemExit("Could not find the app's closing div; no widget inserted.")
    app = app[:close] + "      <ChatWidget />\n    " + app[close:]

app_path.write_text(app, encoding="utf-8")
print("React chatbot component connected to App.jsx.")
