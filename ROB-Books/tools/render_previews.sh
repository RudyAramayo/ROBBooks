#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/opt/node@22/bin:/opt/homebrew/bin:$PATH"
magick_bin="$(command -v magick)"
montage_font="/System/Library/Fonts/Helvetica.ttc"

project_root="$(cd "$(dirname "$0")/.." && pwd)"
pdf_dir="$project_root/output/pdf"
render_root="$project_root/tmp/pdfs/rendered"
preview_dir="$project_root/output/previews"

mkdir -p "$render_root" "$preview_dir"

for pdf_path in "$pdf_dir"/*.pdf; do
  book_name="$(basename "$pdf_path" .pdf)"
  book_render="$render_root/$book_name"
  mkdir -p "$book_render"
  # Rendered pages are disposable build products. Remove only this book's
  # known page-image pattern so a shorter revision cannot retain stale pages.
  find "$book_render" -mindepth 1 -maxdepth 1 -type f -name 'page-*.jpg' -delete
  pdftoppm -jpeg -r 72 "$pdf_path" "$book_render/page"
  "$magick_bin" montage "$book_render"/page-*.jpg \
    -font "$montage_font" -thumbnail 204x264 -tile 5x -geometry +8+8 \
    "$preview_dir/$book_name-contact-sheet.jpg"
done

echo "Rendered contact sheets in $preview_dir"
