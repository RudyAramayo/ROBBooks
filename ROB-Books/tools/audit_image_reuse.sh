#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "$0")/.." && pwd)"
source_dir="$project_root/source"
work_dir="$project_root/tmp/image-audit"
mkdir -p "$work_dir"

volume_map="$work_dir/numbered-volume-images.txt"
: > "$volume_map"

for volume in 1 2 3 4 5 6 7 8; do
  for source_path in "$source_dir"/volume-"$volume"-*.tex; do
    [[ -f "$source_path" ]] || continue
    rg -o '[A-Za-z0-9][A-Za-z0-9._-]+\.(jpg|png)' "$source_path" || true
  done | sort -u | sed "s#^#volume-$volume #" >> "$volume_map"
done

duplicates="$work_dir/cross-volume-duplicates.txt"
awk '
  { count[$2]++; owners[$2] = owners[$2] " " $1 }
  END { for (image in count) if (count[image] > 1) print image owners[image] }
' "$volume_map" | sort > "$duplicates"

allowed_duplicates=(
  "2022-chassis-wiring-overhead.jpg volume-1 volume-2"
)

failure=0
while IFS= read -r duplicate; do
  [[ -n "$duplicate" ]] || continue
  allowed=0
  for exception in "${allowed_duplicates[@]}"; do
    if [[ "$duplicate" == "$exception" ]]; then
      allowed=1
      break
    fi
  done
  if [[ "$allowed" -eq 0 ]]; then
    echo "ERROR: unapproved cross-volume image reuse: $duplicate"
    failure=1
  fi
done < "$duplicates"

manual_images="$work_dir/manual-images.txt"
numbered_images="$work_dir/all-numbered-images.txt"
manual_overlap="$work_dir/manual-overlap.txt"
rg -o '[A-Za-z0-9][A-Za-z0-9._-]+\.(jpg|png)' \
  "$source_dir/complete-builders-field-manual.tex" | sort -u > "$manual_images"
awk '{ print $2 }' "$volume_map" | sort -u > "$numbered_images"
comm -12 "$manual_images" "$numbered_images" > "$manual_overlap"

echo "Numbered-volume image sets:"
for volume in 1 2 3 4 5 6 7 8; do
  count="$(awk -v owner="volume-$volume" '$1 == owner { count++ } END { print count + 0 }' "$volume_map")"
  echo "  volume-$volume: $count unique image file(s)"
done
echo "Approved numbered-volume overlaps: $(wc -l < "$duplicates" | tr -d ' ')"
echo "Field-manual evidence overlaps (reported exception): $(wc -l < "$manual_overlap" | tr -d ' ')"
echo "Reports: $work_dir"

exit "$failure"
