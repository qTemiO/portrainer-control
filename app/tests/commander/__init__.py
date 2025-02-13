import sys
from pathlib import Path

app_path = str(Path.cwd().joinpath("app"))
if app_path not in sys.path:
    sys.path.append(app_path)
