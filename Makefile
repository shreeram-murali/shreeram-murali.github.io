PY ?= .venv/bin/python
PELICAN ?= .venv/bin/pelican

.PHONY: html serve publish images clean

html:        ## Build the site into output/
	$(PELICAN) content

serve:       ## Build, watch for changes, serve on http://localhost:8000
	$(PELICAN) --autoreload --listen

publish:     ## Build with production settings (what CI runs)
	$(PELICAN) content -s publishconf.py

images:      ## Resize/compress photos in content/images
	$(PY) scripts/resize_images.py

clean:
	rm -rf output
