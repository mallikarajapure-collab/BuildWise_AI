from pathlib import Path

path = Path("vite.config.js")
source = path.read_text(encoding="utf-8-sig")
if "127.0.0.1:8000" not in source:
    source = source.replace(
        "plugins: [react()],",
        """plugins: [react()],
  server: {
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },""",
        1
    )
path.write_text(source, encoding="utf-8")
print("Vite API proxy configured.")
