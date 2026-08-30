#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/opt/node@22/bin:/opt/homebrew/bin:$PATH"

project_root="$(cd "$(dirname "$0")/.." && pwd)"
pdf_dir="$project_root/output/pdf"
build_dir="$project_root/tmp/pdfs"
validation_dir="$project_root/tmp/pdfs/validation"
source_dir="$project_root/source"
asset_dir="$project_root/assets"
preview_dir="$project_root/output/previews"

mkdir -p "$validation_dir"

failure=0

echo "===== private-path publication guard ====="
if private_source_matches="$(rg -n '/Users/[^/]+/' \
  "$project_root"/*.md "$source_dir" \
  --glob '*.md' --glob '*.tex' --glob '*.sty' 2>/dev/null)"; then
  echo "ERROR: private macOS user path appears in publishable book source:"
  printf '%s\n' "$private_source_matches"
  failure=1
else
  echo "No private macOS user paths detected in publishable book source."
fi

if ! bash "$project_root/tools/audit_image_reuse.sh"; then
  failure=1
fi

if ! python3 "$project_root/tools/audit_publication_assets.py" --ocr; then
  failure=1
fi

books=(
  volume-1-meet-rob
  volume-2-circuits-and-signals
  volume-3-motion-workshop
  volume-4-mission-control
  volume-5-ai-robotics-with-codex
  volume-6-amber-dual-arm-robotics
  volume-7-engineering-robcontrollervision
  volume-8-engineering-cerebro
  rob-and-the-lost-yellow-ball
  complete-builders-field-manual
)

retired_names=(
  2022-coding-workstation.jpg
  2024-ethernet-controller-board.jpg
  2024-maker-faire-demonstration.jpg
  2025-code-logs-and-status.jpg
  2025-rob-and-chessboard.jpg
  2025-rob-camera-head-front.jpg
  2025-rob-full-front.jpg
  2025-vision-software-monitor.jpg
)

check_retired_paths() {
  scope_label="$1"
  shift
  for retired_name in "${retired_names[@]}"; do
    while IFS= read -r -d '' retired_path; do
      echo "ERROR: retired asset appears in $scope_label: $retired_path"
      failure=1
    done < <(find "$@" -type f -name "$retired_name" -print0)
  done
}

check_retired_text() {
  scope_label="$1"
  shift
  rg_args=()
  for retired_name in "${retired_names[@]}"; do
    rg_args+=( -e "$retired_name" )
  done
  if retired_matches="$(rg -a -l -F "${rg_args[@]}" -- "$@" 2>/dev/null)"; then
    echo "ERROR: retired asset name appears in $scope_label:"
    printf '%s\n' "$retired_matches"
    failure=1
  fi
}

echo "===== retired-asset publication guard ====="
# Deliberately exclude tmp/private-review-do-not-publish: it is the quarantine,
# not a publishable source. The validator itself is also outside these scopes.
check_retired_paths "publishable assets or output" "$asset_dir" "$pdf_dir" "$preview_dir"
check_retired_text "TeX source" "$source_dir"
check_retired_text "PDF or preview output" "$pdf_dir" "$preview_dir"

for book_name in "${books[@]}"; do
  pdf_path="$pdf_dir/$book_name.pdf"
  source_path="$source_dir/$book_name.tex"
  log_path="$build_dir/$book_name.log"
  echo "===== $book_name ====="

  if [[ ! -f "$pdf_path" ]]; then
    echo "ERROR: expected PDF is missing: $pdf_path"
    failure=1
    continue
  fi

  stale=0
  for dependency in "$source_path" "$source_dir/robbook.sty" "$source_dir"/*-deep-dive.tex "$source_dir/adult-learning-and-commissioning.tex"; do
    if [[ "$dependency" -nt "$pdf_path" ]]; then
      echo "ERROR: PDF is stale; dependency is newer: $dependency"
      stale=1
    fi
  done

  markdown_path="$source_dir/$book_name.md"
  if [[ -f "$markdown_path" && "$markdown_path" -nt "$pdf_path" ]]; then
    echo "ERROR: PDF is stale; Markdown manuscript is newer: $markdown_path"
    failure=1
  fi

  while IFS= read -r -d '' asset_path; do
    asset_name="${asset_path##*/}"
    if rg -Fq -- "$asset_name" "$source_path" && [[ "$asset_path" -nt "$pdf_path" ]]; then
      echo "ERROR: PDF is stale; referenced asset is newer: $asset_path"
      stale=1
    fi
  done < <(find "$asset_dir" -type f -print0)

  if [[ "$stale" -ne 0 ]]; then
    failure=1
  fi

  pdfinfo "$pdf_path" | awk '/^Pages:|^Page size:|^File size:|^Encrypted:/'
  pdftotext -layout "$pdf_path" "$validation_dir/$book_name.txt"
  if rg -q '/Users/[^/]+/' "$validation_dir/$book_name.txt"; then
    echo "ERROR: private macOS user path appears in extracted PDF text"
    rg -n '/Users/[^/]+/' "$validation_dir/$book_name.txt"
    failure=1
  fi
  if ! rg -q "R\.O\.B\.|ROB" "$validation_dir/$book_name.txt"; then
    echo "ERROR: expected ROB text was not extracted"
    failure=1
  fi
  if [[ ! -f "$log_path" ]]; then
    echo "ERROR: expected LaTeX build log is missing: $log_path"
    failure=1
  elif rg -q "^!|LaTeX Error|Undefined control sequence|undefined references|There were undefined references|Missing character" "$log_path"; then
    echo "ERROR: serious LaTeX warning found"
    rg -n "^!|LaTeX Error|Undefined control sequence|undefined references|There were undefined references|Missing character" "$log_path"
    failure=1
  fi
  if [[ -f "$log_path" ]]; then
    rg -n "Overfull" "$log_path" || true
  fi
done

check_retired_text "extracted PDF text" "$validation_dir"

echo "===== prepared-photo privacy check ====="
metadata_dump="$validation_dir/prepared-photo-metadata.txt"
exiv2 -pa "$project_root/assets/photos"/*.jpg > "$metadata_dump"
if rg -q "Exif\.GPSInfo|Exif\.Image\.Make|Exif\.Image\.Model|Xmp\.exif\.GPS" "$metadata_dump"; then
  echo "ERROR: private camera metadata remains in prepared photos"
  failure=1
else
  echo "No GPS or camera make/model tags detected in prepared photos."
fi

echo "===== source placeholder count ====="
if placeholder_matches="$(rg -n "ROBPlaceholder" "$project_root/source"/*.tex 2>/dev/null)"; then
  printf '%s\n' "$placeholder_matches"
  echo "ERROR: unresolved manuscript placeholders remain"
  failure=1
else
  echo "0"
fi

exit "$failure"
