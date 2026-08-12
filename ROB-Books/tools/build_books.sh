#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/opt/node@22/bin:/opt/homebrew/bin:$PATH"

project_root="$(cd "$(dirname "$0")/.." && pwd)"
source_dir="$project_root/source"
build_dir="$project_root/tmp/pdfs"
output_dir="$project_root/output/pdf"

mkdir -p "$build_dir" "$output_dir" "$project_root/tmp/cache" "$project_root/tmp/texmf-var" "$project_root/tmp/texmf-cache"

export XDG_CACHE_HOME="$project_root/tmp/cache"
export TEXMFVAR="$project_root/tmp/texmf-var"
export TEXMFCACHE="$project_root/tmp/texmf-cache"

books=(
  volume-1-meet-rob.tex
  volume-2-circuits-and-signals.tex
  volume-3-motion-workshop.tex
  volume-4-mission-control.tex
  volume-5-ai-robotics-with-codex.tex
  volume-6-amber-dual-arm-robotics.tex
  complete-builders-field-manual.tex
)

cd "$source_dir"

for book_source in "${books[@]}"; do
  latex_options=(-g -xelatex -interaction=nonstopmode -halt-on-error -file-line-error)
  # The Markdown package invokes its bundled local converter for Volumes 5 and 6.
  # Keep shell escape disabled for the hand-authored TeX books.
  if [[ "$book_source" == "volume-5-ai-robotics-with-codex.tex" \
      || "$book_source" == "volume-6-amber-dual-arm-robotics.tex" ]]; then
    latex_options+=(-shell-escape)
  fi
  latexmk "${latex_options[@]}" \
    -outdir="$build_dir" "$book_source"
  book_name="${book_source%.tex}"
  cp "$build_dir/$book_name.pdf" "$output_dir/$book_name.pdf"
done

echo "Built ${#books[@]} print PDFs in $output_dir"
