"""Rebuild tracked static pages using the editorial sources; run from any folder."""
import subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent
for script in ['generate_pages.py','build-resident-guide.py','inject_parts.py','build_sitemap.py']:
 subprocess.run([sys.executable,'-X','utf8',str(R/'scripts'/script)],cwd=R,check=True)
subprocess.run(['node',str(R/'scripts/build-search-index.mjs')],cwd=R,check=True)
