#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/opt/node@22/bin:/opt/homebrew/bin:$PATH"
magick_bin="$(command -v magick)"

project_root="$(cd "$(dirname "$0")/.." && pwd)"
workspace_root="$(cd "$project_root/../.." && pwd)"
photo_out="$project_root/assets/photos"
slide_out="$project_root/assets/slides"

mkdir -p "$photo_out" "$slide_out"

expected_photos=(
    2019-rob-front-corner.jpg
    2019-rob-side-profile.jpg
    2020-rob-front.jpg
    2020-rob-overhead.jpg
    2021-cable-loop-and-arm.jpg
    2021-open-electronics-bay.jpg
    2021-shoulder-gear-and-cable.jpg
    2021-wiring-closeup.jpg
    2022-arm-controller-board.jpg
    2022-bracket-assembly-front.jpg
    2022-bracket-fit-check.jpg
    2022-chain-sprocket-interior.jpg
    2022-chassis-wiring-overhead.jpg
    2022-drilling-metal-rail.jpg
    2022-drive-assembly-rear.jpg
    2022-fanless-computer-and-serial.jpg
    2022-medium-duty-bracket-package.jpg
    2022-mounted-clamp-and-bracket.jpg
    2022-oakd-depth-camera.jpg
    2022-rob-front-arms-raised.jpg
    2022-tracked-base-front.jpg
    2024-base-actuator-between-treads.jpg
    2024-batteries-and-power-leads.jpg
    2024-caliper-tread-measurement.jpg
    2024-central-linear-actuator.jpg
    2024-chain-drive-closeup.jpg
    2024-dense-internal-routing.jpg
    2024-hengdrive-motor-label.jpg
    2024-nearly-assembled-base.jpg
    2024-open-tracked-base.jpg
    2024-power-cable-pass-through.jpg
    2024-sprocket-machined-opening.jpg
    2024-voltage-gauge.jpg
    2025-detached-articulated-arm.jpg
    2025-emergency-stop-and-arm.jpg
    2025-emergency-stop-bench-layout.jpg
    2025-intermeshing-shoulder-gears.jpg
    2025-labeled-cables.jpg
    2025-neck-gear-train.jpg
    2025-rear-electronics-bay.jpg
    2025-rob-face-portrait.jpg
    2025-rob-side-full-body.jpg
    2026-rob-lightsabers-front.jpg
    2026-rob-lightsabers-overhead.jpg
    2026-rob-lightsabers-portrait.jpg
    2026-rob-lightsabers-side.jpg
)

expected_slides=(
    rob-v3-page-23.jpg
    rob-v3-page-41.jpg
    rob-v3-page-47.jpg
    rob-v3-page-54.jpg
    rob-v3-page-55.jpg
    rob-v3-page-61.jpg
    rob-v3-page-72.jpg
    rob-v3-page-74.jpg
)

assert_exact_allowlist() {
    asset_dir="$1"
    shift
    expected_names=("$@")
    unexpected=0

    while IFS= read -r -d '' asset_path; do
        asset_name="${asset_path##*/}"
        allowed=0
        for expected_name in "${expected_names[@]}"; do
            if [[ "$asset_name" == "$expected_name" ]]; then
                allowed=1
                break
            fi
        done
        if [[ "$allowed" -eq 0 ]]; then
            echo "ERROR: unlisted publishable asset is present: $asset_path" >&2
            unexpected=1
        fi
    done < <(find "$asset_dir" -mindepth 1 -maxdepth 1 -print0)

    for expected_name in "${expected_names[@]}"; do
        if [[ ! -f "$asset_dir/$expected_name" ]]; then
            echo "ERROR: expected publishable asset is missing: $asset_dir/$expected_name" >&2
            unexpected=1
        fi
    done

    if [[ "$unexpected" -ne 0 ]]; then
        return 1
    fi
}

convert_photo() {
    source_path="$1"
    output_name="$2"
    "$magick_bin" "$source_path" \
        -auto-orient \
        -resize '3200x3200>' \
        -colorspace sRGB \
        -strip \
        -quality 93 \
        "$photo_out/$output_name"
}

gallery="$workspace_root/ORobotics/media/gallery-originals"
lightsaber_gallery="$workspace_root/BlueGreen Lightsaber Pics ROB"

convert_photo "$gallery/2019/IMG_0029.HEIC" "2019-rob-front-corner.jpg"
convert_photo "$gallery/2019/IMG_1308.jpg" "2019-rob-side-profile.jpg"
convert_photo "$gallery/2020/IMG_0996.HEIC" "2020-rob-front.jpg"
convert_photo "$gallery/2020/IMG_0998.HEIC" "2020-rob-overhead.jpg"
convert_photo "$gallery/2021/IMG_1420.JPG" "2021-open-electronics-bay.jpg"
convert_photo "$gallery/2021/IMG_1423.JPG" "2021-wiring-closeup.jpg"
convert_photo "$gallery/2021/IMG_1426.JPG" "2021-cable-loop-and-arm.jpg"
convert_photo "$gallery/2021/IMG_1432.JPG" "2021-shoulder-gear-and-cable.jpg"
convert_photo "$gallery/2022/66943629991__1F58B14B-5A6E-49E2-9E92-A7390E280F13.HEIC" "2022-fanless-computer-and-serial.jpg"
convert_photo "$gallery/2022/IMG_0062.HEIC" "2022-rob-front-arms-raised.jpg"
convert_photo "$gallery/2022/IMG_0142.HEIC" "2022-chassis-wiring-overhead.jpg"
convert_photo "$gallery/2022/IMG_0146.HEIC" "2022-drive-assembly-rear.jpg"
convert_photo "$gallery/2022/IMG_0191.HEIC" "2022-arm-controller-board.jpg"
convert_photo "$gallery/2022/IMG_0211.HEIC" "2022-medium-duty-bracket-package.jpg"
convert_photo "$gallery/2022/IMG_0212.HEIC" "2022-bracket-fit-check.jpg"
convert_photo "$gallery/2022/IMG_0214.HEIC" "2022-drilling-metal-rail.jpg"
convert_photo "$gallery/2022/IMG_0217.HEIC" "2022-mounted-clamp-and-bracket.jpg"
convert_photo "$gallery/2022/IMG_0218.HEIC" "2022-bracket-assembly-front.jpg"
convert_photo "$gallery/2022/IMG_0220.HEIC" "2022-chain-sprocket-interior.jpg"
convert_photo "$gallery/2022/IMG_0227.HEIC" "2022-tracked-base-front.jpg"
convert_photo "$gallery/2022/IMG_1555.JPG" "2022-oakd-depth-camera.jpg"
convert_photo "$gallery/2024/IMG_4330.HEIC" "2024-chain-drive-closeup.jpg"
convert_photo "$gallery/2024/IMG_4334.HEIC" "2024-sprocket-machined-opening.jpg"
convert_photo "$gallery/2024/IMG_4359.HEIC" "2024-caliper-tread-measurement.jpg"
convert_photo "$gallery/2024/IMG_4362.HEIC" "2024-base-actuator-between-treads.jpg"
convert_photo "$gallery/2024/IMG_4363.HEIC" "2024-dense-internal-routing.jpg"
convert_photo "$gallery/2024/IMG_4366.HEIC" "2024-hengdrive-motor-label.jpg"
convert_photo "$gallery/2024/IMG_4367.HEIC" "2024-batteries-and-power-leads.jpg"
convert_photo "$gallery/2024/IMG_4368.HEIC" "2024-open-tracked-base.jpg"
convert_photo "$gallery/2024/IMG_4370.HEIC" "2024-power-cable-pass-through.jpg"
convert_photo "$gallery/2024/IMG_4371.HEIC" "2024-central-linear-actuator.jpg"
convert_photo "$gallery/2024/IMG_4372.HEIC" "2024-voltage-gauge.jpg"
convert_photo "$gallery/2024/IMG_4373.HEIC" "2024-nearly-assembled-base.jpg"
convert_photo "$gallery/2025/IMG_5980.HEIC" "2025-emergency-stop-and-arm.jpg"
convert_photo "$gallery/2025/IMG_6004.HEIC" "2025-intermeshing-shoulder-gears.jpg"
convert_photo "$gallery/2025/IMG_6022.HEIC" "2025-labeled-cables.jpg"
convert_photo "$gallery/2025/IMG_6023.HEIC" "2025-rear-electronics-bay.jpg"
convert_photo "$gallery/2025/IMG_6026.HEIC" "2025-emergency-stop-bench-layout.jpg"
convert_photo "$gallery/2025/IMG_6031.HEIC" "2025-detached-articulated-arm.jpg"
convert_photo "$gallery/2025/IMG_6045.HEIC" "2025-rob-face-portrait.jpg"
convert_photo "$gallery/2025/IMG_6056.HEIC" "2025-neck-gear-train.jpg"
convert_photo "$gallery/2025/IMG_6150.HEIC" "2025-rob-side-full-body.jpg"
convert_photo "$lightsaber_gallery/IMG_6296.HEIC" "2026-rob-lightsabers-front.jpg"
convert_photo "$lightsaber_gallery/IMG_6325.HEIC" "2026-rob-lightsabers-overhead.jpg"
convert_photo "$lightsaber_gallery/IMG_6318.HEIC" "2026-rob-lightsabers-portrait.jpg"
convert_photo "$lightsaber_gallery/IMG_6303.HEIC" "2026-rob-lightsabers-side.jpg"

cp "$dev_root/ORobotics/static/images/Orbitus_horizontal_logo.png" "$project_root/assets/orbitus-horizontal-logo.png"

source_pdf="$workspace_root/Presentation/ROB_v3.pdf"
for page in 23 41 47 54 55 61 72 74; do
    pdftoppm -f "$page" -l "$page" -singlefile -jpeg -r 120 "$source_pdf" "$slide_out/rob-v3-page-$page"
done

# Never delete unknown files automatically: they may be user work. Fail closed
# instead, so the owner can review and move every extra entry deliberately.
assert_exact_allowlist "$photo_out" "${expected_photos[@]}"
assert_exact_allowlist "$slide_out" "${expected_slides[@]}"

echo "Prepared $(find "$photo_out" -type f | wc -l | tr -d ' ') photos and $(find "$slide_out" -type f | wc -l | tr -d ' ') slide images."
