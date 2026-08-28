"""Legacy French launcher for the same unified app.

Opens the bilingual dashboard with French pre-selected. Visitors can switch
back to English in the sidebar. Prefer: streamlit run app.py
"""

import os

os.environ.setdefault("SLEEP_APP_LANG", "fr")

from app import main

main()
