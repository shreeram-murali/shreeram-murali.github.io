"""Production settings, used by the GitHub Actions build."""

import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: E402,F403

SITEURL = "https://shreeram-murali.github.io"
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True
