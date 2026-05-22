import os
import site
import sys

# Build dynamic path based on Python version
custom_path = os.path.join(
    r"D:\PythonLibs",
    f"Python{sys.version_info.major}{sys.version_info.minor}",
    "site-packages"
)

# Add to sys.path if not already present
if os.path.isdir(custom_path) and custom_path not in sys.path:
    site.addsitedir(custom_path)
