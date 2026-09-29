# shreeram-murali.github.io

Personal academic website built with [Pelican](https://getpelican.com) and a small hand-written theme. All content is Markdown. Source lives on the `dev` branch; pushing to `dev` builds the site and publishes it to `main`, which GitHub Pages serves.

```
content/
  pages/        one Markdown file per page (home, publications, cv, photography, 404)
  blog/         blog posts, one Markdown file each
  images/       photos and images (run the resize script before committing)
  files/        PDFs and other downloads (cv.pdf, posters)
  extra/        favicon.svg (published at the site root)
theme/
  templates/    Jinja2 templates: base, page, photography, article, index
  static/css/   tokens.css (all design values), base.css, photography.css
scripts/
  resize_images.py
pelicanconf.py  local settings: site info, palette, fonts, nav
publishconf.py  production overrides (absolute URLs), used by CI
```

## Setup

Requires Python 3.10 or newer.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Preview locally

```sh
pelican --autoreload --listen
```

Open <http://localhost:8000>. The site rebuilds whenever you save a file. Just refresh the browser.

To do a one-off build into `output/`, run `pelican content`. The `Makefile` has shortcuts for these (`make serve`, `make html`, `make publish`, `make images`), and they work even without activating the venv.

## Editing content

Each page is a Markdown file in `content/pages/` with a metadata header:

```markdown
Title: Publications
Summary: Used for the page description and link previews.

Page content in Markdown...
```

- **Home** (`home.md`) is saved as the site's `index.html` because of `Save_as: index.html`. `Hide_title: true` keeps its heading visible only to screen readers, since your name is already in the header.
- **Links between pages** look like `[text]({filename}publications.md)`. **Links to images and files** look like `![alt]({static}/images/x.jpg)` or `[CV]({static}/files/cv.pdf)`. Pelican rewrites these to the correct URLs.
- **CV:** replace `content/files/cv.pdf`. The file name must stay the same, or you need to update the links.
- **Portrait:** replace `content/images/portrait.jpg`. It is cropped to 4:5 on the home page.

### Publications

Posters and talks are a plain bullet list. Papers use the structured format below.

Each entry is a block with four lines separated by blank lines: title, authors, venue/year, and links.

```markdown
<div class="pub" markdown="1">
Paper title

**S. Murali**, A. Coauthor, and B. Coauthor

*Venue*, 2026

[PDF]({static}/files/paper.pdf) · [Code](https://github.com/...)
</div>
```

Leave out the last line if there are no links. Every entry has the same shape, so a `.bib` → Markdown script can generate this file later.

### Images

Always write alt text: `![A foggy harbour at dawn]({static}/images/harbour.jpg)`. Images scale to fit the column automatically. To lazy-load an image further down a page, add attributes: `![alt](...){: loading="lazy" }`.

Before committing new photos, shrink them:

```sh
python scripts/resize_images.py                    # everything in content/images
python scripts/resize_images.py path/to/photo.jpg  # specific files or folders
python scripts/resize_images.py --dry-run --max 1600 --quality 80
```

The script caps the long edge at 2000 px, applies the camera's rotation, strips metadata (including GPS), and re-compresses the file. It overwrites files in place and skips any it can't make smaller.

## Two-column layouts

Any Markdown file can contain column blocks. Each **direct child** of a `.columns` div becomes one column. Wrap text columns in `<div markdown="1">`, and add blank lines around the inner Markdown:

```markdown
<div class="columns" markdown="1">

<div markdown="1">
### Left
Some **Markdown** here.
</div>

<div markdown="1">
### Right
More Markdown here.
</div>

</div>
```

Variants:

| Class                  | Layout                                                 |
|------------------------|--------------------------------------------------------|
| `columns`              | two equal columns                                      |
| `columns three`        | three equal columns                                    |
| `columns narrow-first` | narrow first column (photo/sidebar), wide second one   |

An image written on its own line (as in `home.md`) also counts as one column. All variants stack into a single column on screens narrower than about 640 px.

### Text wrapping around an image

To let text flow beside an image and then continue underneath it (as on the home page), add a class to the image:

```markdown
![Alt text]({static}/images/photo.jpg){: .float-left }

Paragraphs that follow wrap around the image...
```

Use `.float-right` to put the image on the right. The image is 11rem wide (`--portrait-width`). The next `##` heading, `---` rule or column block always starts below it. On small screens the image sits on its own line instead.

## Palettes and fonts

All colours, fonts, sizes, spacing and the column width are defined in `theme/static/css/tokens.css`. To switch the look, change one setting in `pelicanconf.py`:

```python
THEME_PALETTE = "rose"    # "rose" | "plain" | "sand" | "paper" | "dark"
```

| Palette | Description |
|---------|-------------|
| `rose`  | dusty pink, near-black serif body text, sans headings, coral accents; dark mode is charcoal with pale-green text and salmon links (the old site's dark colours) |
| `plain` | neutral white/grey with blue links, plus a matching dark mode |
| `sand`  | the beige/terracotta colours from the previous site, plus its dark mode |
| `paper` | warm off-white, rust links, serif body text; light only |
| `dark`  | always dark |

**Light/dark button.** `rose`, `plain` and `sand` have both modes. They follow the visitor's system setting, and a small button in the header lets visitors switch. Their choice is saved in their browser. If they switch back to the mode that matches their system, the saved choice is cleared and the site follows the system again. The button only appears for these three palettes, and it's the only JavaScript on the site. In `tokens.css`, each colour of a two-mode palette is written as `light-dark(LIGHT, DARK)`.

**Block quotes** (`> text` in Markdown) render as pull quotes: large bold heading type with an accent-coloured bar.

Fonts:

```python
THEME_FONT_BODY = "auto"      # "auto" = the palette's choice
THEME_FONT_HEADING = "auto"
```

Each setting accepts:

- `"sans"`, `"serif"` or `"mono"`: system fonts, which load instantly with nothing to download.
- Any [Google Fonts](https://fonts.google.com) family, with an optional fallback: `"Source Serif 4, serif"` or `"Inter, sans"`. The Google Fonts stylesheet is only added to the page when you choose one. By default it requests regular, bold and italic (`THEME_GOOGLE_FONT_AXES`). If a family doesn't have all three, remove the parts it lacks.

To create a new palette, copy one of the `[data-palette="..."]` blocks in `tokens.css`, rename it, and set `THEME_PALETTE` to the new name. For a palette with both modes, copy a `light-dark()` block and add its name to `dual_palettes` at the top of `theme/templates/base.html` so the button appears. Keep link and muted colours at a contrast ratio of at least 4.5:1 against the background.

The column width is `--measure` in `tokens.css`.

## Adding a page to the nav (e.g. Film)

1. Create `content/pages/film.md`:

   ```markdown
   Title: Film
   Template: photography
   Summary: Short films and videos.

   One line about the films.
   ```

   `Template: photography` gives the page the wide, visual layout. Leave that line out for an ordinary text page.

2. Add it to `NAV_LINKS` in `pelicanconf.py`:

   ```python
   NAV_LINKS = [
       ("Home", ""),
       ("Publications", "publications/"),
       ("CV", "cv/"),
       ("Photography", "photography/"),
       ("Film", "film/"),
   ]
   ```

The page URL is its file name: `film.md` becomes `/film/`.

## Photography page

`photography.md` uses `theme/templates/photography.html` and loads the extra stylesheet `theme/static/css/photography.css`. The academic pages never load that stylesheet, so you can make the gallery full-bleed, dark, or anything else without affecting them. The template contains an empty `<div class="gallery" id="gallery">` for the images.

## Blog

Posts are Markdown files in `content/blog/`. The file name becomes the URL, so `content/blog/my-post.md` is published at `/blog/my-post/`:

```markdown
Title: My post
Date: 2026-10-01
Summary: One line, used for link previews.

Post content in Markdown...
```

`/blog/` lists every post with its date, newest first. Add `Status: draft` to a post's header to leave it out of the build. Tag, category, author and archive pages and feeds are turned off in `pelicanconf.py`. The date format is `DEFAULT_DATE_FORMAT`.

## Branches and deployment

- **`dev`** holds the source: content, theme and settings. This is the branch you work on and push.
- **`main`** holds only the built site, i.e. the contents of `output/`. GitHub Pages serves it. **Don't edit `main` by hand**; every deploy replaces its contents.

`.github/workflows/deploy.yml` runs on every push to `dev`, and you can also start it from the Actions tab. It:

1. installs `requirements.txt`,
2. builds with `pelican content -s publishconf.py` (absolute URLs for `https://shreeram-murali.github.io`),
3. commits `output/` to `main` (adding a `.nojekyll` file so GitHub serves the files as they are).

Day to day:

```sh
git switch dev
# edit content, preview with `pelican --autoreload --listen`
git add -A && git commit -m "Update publications"
git push          # the site updates about a minute later
```

GitHub Pages setting (one time): **Settings → Pages → Build and deployment → Source: Deploy from a branch → `main` / `(root)`**.

`output/` and `.venv/` are git-ignored on `dev`. You never commit built HTML there.
