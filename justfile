# Usage: just <recipe>. Run `just` to list recipes.
port := "8000"

default:
    @just --list

# Regenerate all pages, SEO files (and images with `just images`)
build:
    python3 tools/build.py

# Re-optimise photos from photos/ and re-render icons and og-image
images:
    python3 tools/images.py

# Re-download self-hosted fonts
fonts:
    python3 tools/fetch_fonts.py

# Serve the site locally (never via file://)
serve: build
    python3 -m http.server {{port}}

# Desktop and phone screenshots (light and dark) into shots/
shot: build
    python3 tools/shots.py

# Same screenshots in Docker, if local Chrome is unavailable
shot-docker: build
    docker build -t alina-shots -f tools/Dockerfile .
    docker run --rm -v "$PWD":/site alina-shots

# Sanity checks: links, hreflang, JSON-LD, horizontal scroll
check: build
    python3 tools/check.py
