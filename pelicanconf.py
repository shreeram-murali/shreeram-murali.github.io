"""Pelican settings for local development.

`pelican` (with no arguments) reads this file. The production build uses
publishconf.py, which imports everything here and overrides a few values.
"""

# --- Site ---------------------------------------------------------------

AUTHOR = "Shreeram Murali"
SITENAME = "Shreeram Murali"
SITEDESCRIPTION = (
    "PhD student at Aalto University working on safe, lightweight "
    "learning-based control. Also photography and filmmaking."
)
SITEURL = ""  # empty = relative links for local preview
TIMEZONE = "Europe/Helsinki"
DEFAULT_LANG = "en"

PATH = "content"
THEME = "theme"

# Image used for link previews (Open Graph). Path is relative to the site root.
OG_IMAGE = "images/portrait.jpg"

# --- Look & feel --------------------------------------------------------
# Palette: "rose" (dusty pink / charcoal), "plain" (neutral), "sand" (the old
# imml colours) all have light + dark modes and a theme button in the header.
# "paper" (warm, serif) is light only; "dark" is dark only.
THEME_PALETTE = "rose"

# Fonts: "auto" (palette default), "sans", "serif", "mono" (system fonts, no
# download), or any Google Fonts family, optionally with a fallback stack:
#   THEME_FONT_BODY = "Source Serif 4, serif"
#   THEME_FONT_HEADING = "Inter, sans"
THEME_FONT_HEADING = "auto"
THEME_FONT_BODY = "auto"

# Weights/styles requested for Google Fonts. Most text families have these;
# drop ";1,400" if a family has no italic.
THEME_GOOGLE_FONT_AXES = "ital,wght@0,400;0,700;1,400"

# --- Navigation ---------------------------------------------------------
# (label, path relative to the site root). Add ("Film", "film/") once
# content/pages/film.md exists.
NAV_LINKS = [
    ("Home", ""),
    ("Publications", "publications/"),
    ("CV", "cv/"),
    ("Blog", "blog/"),
    ("Photography", "photography/"),
]
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

# --- Content & URLs -----------------------------------------------------

PAGE_PATHS = ["pages"]
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

# Blog posts: Markdown files in content/blog/, listed at /blog/.
ARTICLE_PATHS = ["blog"]
ARTICLE_URL = "blog/{slug}/"
ARTICLE_SAVE_AS = "blog/{slug}/index.html"
INDEX_SAVE_AS = "blog/index.html"  # the home page owns /index.html
DEFAULT_DATE_FORMAT = "%-d %B %Y"  # 5 March 2026
DIRECT_TEMPLATES = ["index"]

# Generated pages we don't need.
TAGS_SAVE_AS = TAG_SAVE_AS = ""
CATEGORIES_SAVE_AS = CATEGORY_SAVE_AS = ""
AUTHORS_SAVE_AS = AUTHOR_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

STATIC_PATHS = ["images", "files", "extra"]
EXTRA_PATH_METADATA = {
    "extra/favicon.svg": {"path": "favicon.svg"},
}

# --- Markdown -----------------------------------------------------------
# "extra" bundles md_in_html (Markdown inside <div markdown="1">), attr_list
# ({: .class }), tables, footnotes, fenced code, etc.
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.extra": {},
        "markdown.extensions.md_in_html": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {},
        "markdown.extensions.smarty": {},
    },
    "output_format": "html5",
}

DEFAULT_PAGINATION = False
RELATIVE_URLS = True
