#!/usr/bin/env python3
"""Convert ROB's print-oriented LaTeX into semantic, Pandoc-readable sources.

The print books use custom full-page photo, colored callout, and TikZ diagram
macros. Pandoc intentionally ignores those presentation macros. This module
replaces them with ordinary LaTeX structures so EPUB output retains the live
text, figures, captions, callout meaning, and diagram relationships.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from html import escape
from pathlib import Path
from typing import Callable


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "source"

BOX_LABELS = {
    "missionbox": "Mission",
    "buildbox": "Make it",
    "safetybox": "Safety check",
    "fieldnotebox": "From ROB's build log",
    "placeholderbox": "Builder input needed",
    "conceptbox": "Computer science connection",
    "advancedbox": "Advanced channel",
    "tcolorbox": "Note",
}

STATUS_TEXT = {
    "Implemented": "Implemented",
    "Commanded": "Commanded",
    "Experimental": "Experimental / optional",
    "Legacy": "Legacy",
    "Planned": "Planned",
    "Unverified": "Builder verification needed",
}

DIAGRAMS = {
    "ROBSimpleSystemDiagram": (
        "System feedback loop",
        "Sense (camera, infrared sensors, and IMU) leads to Think (Mac mini and applications), "
        "which leads to Act (motors and arms). Feedback from the action changes the next sensed "
        "input and choice.",
    ),
    "ROBControlStackDiagram": (
        "Robot control stack",
        "Operator intent from an iPhone, Apple Watch, or Vision Pro controller passes through an "
        "authenticated session with pairing, TLS or QUIC, roles, sequence checks, and applicable "
        "freshness checks. Cerebro on macOS coordinates the robot, then sends a fixed base-command "
        "frame over a USB serial heartbeat. The Arduino base controller drives PWM, direction, "
        "brakes, the actuator, IMU, and infrared interfaces, which affect the physical treads, "
        "flippers, linear actuator, batteries, and mechanics.",
    ),
    "ROBStopChainDiagram": (
        "Stop chain",
        "Releasing input or issuing a manual stop leads through the controller-specific lease or "
        "watchdog, Cerebro's 0.6-second freshness gate, the Arduino serial deadman, and a commanded "
        "stop whose physical result must be tested. A required physical emergency stop uses an "
        "independent contactor or controller stop path that does not depend on software.",
    ),
    "ROBPowerArchitectureDiagram": (
        "Builder-reported power architecture",
        "Four reported 20 Ah LiFePO4 packs feed per-pack protection and a disconnect, then a 12 V "
        "base bus. The base bus supplies base loads and a reported 12-to-24 V boost path. The 24 V "
        "torso bus supplies 24 V peripherals, a 24-to-12 V computer and camera path, and a 24-to-48 V "
        "arm path. The charger returns through the protected pack path. Verify topology, polarity, "
        "battery-management compatibility, protection, conductor ampacity, converters, charger "
        "interlocks, and measured loads before energizing.",
    ),
    "ROBUSBNETDiagram": (
        "Builder-reported USB and network architecture",
        "The M4 Mac connects to a powered USB hub. One branch passes USB and 24 V through the rotary "
        "link to a base hub serving the Arduino and lidar network adapter. A second branch serves the "
        "Tic stepper controller, Maestro servo controller, speakers, and service peripherals. A "
        "backpack router and Ethernet switch connect the Mac, AMBER Ubuntu computer, and Insta360 "
        "camera. Measure every USB power budget and resolve shutdown faults rather than bypassing them.",
    ),
    "ROBArduinoWiringDiagram": (
        "As-written Arduino base interface map",
        "The Mac communicates with an Arduino Mega at 250,000 baud. Right drive uses D2, D3, and D25; "
        "left drive uses D4, D5, and D27; flipper outputs use D6, D7, and D29; and the Pololu linear-"
        "actuator controller uses D22 receive and D23 transmit at 19,200 baud. Six infrared inputs use "
        "A5 through A0. The MPU9250 uses I2C on D20 and D21. Speed-feedback comments conflict over D18, "
        "D19, and D20 and are not implemented. Verify the harness, levels, grounds, polarity, and safe "
        "boot state on the robot.",
    ),
    "ROBCANPhysicalDiagram": (
        "Conceptual AMBER CAN physical path",
        "The Ubuntu SocketCAN host connects through a USB or SLCAN adapter and CAN transceiver to "
        "twisted-pair CANH and CANL, reference ground, and the arm actuator nodes. Verify connector "
        "pins, isolation, shield bonding, built-in termination, and two 120-ohm end terminations on "
        "each physical bus. ROB uses separate can10 left and can11 right buses.",
    ),
}

TIKZ_DESCRIPTIONS = {
    "volume-1-meet-rob.tex": [
        ("Iterative engineering cycle", "Ask, then sketch, build, test, and learn. What you learn starts the next question."),
    ],
    "volume-1-deep-dive.tex": [
        ("Goal-directed feedback loop", "Set a goal, compare it with sensed results, act, sense the result, and compare again."),
    ],
    "volume-2-circuits-and-signals.tex": [
        ("Twenty-five percent PWM duty cycle", "A repeating digital signal stays on for one quarter of each period and off for three quarters: short on time, long off time."),
    ],
    "volume-2-deep-dive.tex": [
        ("Signal shapes over time", "A digital signal switches between two levels, while an analog signal varies continuously. PWM is a repeating digital pulse pattern whose on-time fraction carries a command."),
    ],
    "volume-4-mission-control.tex": [
        ("Separate control and video paths", "A paired controller sends small urgent robctl/2 control messages to Cerebro and exchanges large, droppable robvideo/1 media on a separate path."),
        ("Bounded AI action path", "Perceive and converse, propose a bounded high-level action, validate capability and human policy, execute deterministically, then report a measured terminal result."),
    ],
    "volume-4-deep-dive.tex": [
        ("Control-authority state machine", "A valid request moves authority from inactive to requested; acceptance moves it to active; a stop, rejection, or fault moves it to stopping; completion returns it to inactive."),
    ],
    "complete-builders-field-manual.tex": [
        ("H.264 media pipeline", "A CMSampleBuffer is converted to NV12 and letterboxed, encoded as H.264 with VideoToolbox, framed as RVID or RBVD, checked by a stream validator, and delivered to a sample renderer."),
    ],
}

SERIES_MAP = r"""
\section*{The Building R.O.B. library}
\begin{description}
\item[Volume 1] \textit{Meet ROB: A Robot Is a Team of Systems} --- ages 8--12.
\item[Volume 2] \textit{Circuits and Signals with ROB} --- ages 10--14.
\item[Volume 3] \textit{Motion Workshop: Treads, Gears, and Fabrication} --- ages 10--15.
\item[Volume 4] \textit{Mission Control: Arduino, Mac, Networks, and Vision} --- ages 12--16.
\item[Volume 5] \textit{AI, Robotics, and Codex} --- advanced makers.
\item[Volume 6] \textit{Dual-Arm Robotics} --- advanced makers.
\item[Volume 7] \textit{Engineering ROBControllerVision} --- Swift developers.
\item[Volume 8] \textit{Engineering Cerebro} --- software engineers.
\item[Manual] \textit{Building R.O.B.: The Complete Maker's Field Manual} --- advanced builders.
\end{description}
"""

ARDUINO_STATUS = (
    r"\subsection*{One current Arduino, three historical sketches}" "\n"
    "The ROBArduino archive preserves Base, Torso, and Head sketches from an earlier three-Arduino "
    "design. The builder reports that present-day ROB uses only the Base sketch. This book treats Base "
    "behavior as the current low-level firmware reference and labels Torso and Head behavior as retired "
    "historical evidence. Source files cannot prove which binary is flashed today; record the board "
    "identity, firmware hash, build environment, and upload date before operation.\n"
)

AMBER_STATUS = (
    r"\subsection*{Two AMBER B1 arms, one documented control chain}" "\n"
    "ROB carries two seven-joint AMBER B1 arms. The repository snapshot separates their Ubuntu-side "
    "cores as L-10 and R-11. Network clients use UDP or LCM, each core binds a stable CAN interface, "
    "and CAN carries commands and feedback between that core and its arm actuators. AmberHomeFolder is "
    "evidence from one Ubuntu machine, not a deployable image; never copy its credentials, logs, virtual "
    "environment, or machine-specific identifiers.\n"
)

SOURCE_ROOT = (
    r"\subsection*{How to find the files}" "\n"
    r"Open the public repositories at \url{https://github.com/RudyAramayo/ROBBooks}, "
    r"\url{https://github.com/RudyAramayo/ROBArduino}, \url{https://github.com/RudyAramayo/Cerebro}, "
    r"\url{https://github.com/RudyAramayo/ROBController}, "
    r"\url{https://github.com/RudyAramayo/ROBControllerVision}, "
    r"\url{https://github.com/RudyAramayo/Amber-HomeFolder}, and "
    r"\url{https://github.com/RudyAramayo/ROBTrainingGames}. The website source is at "
    r"\url{https://github.com/OrbitusRoboticsWebSite/ORobotics}. A named archival item without a "
    "verified public repository is labeled as evidence rather than given an invented URL.\n"
)


def extract_group(text: str, start: int, opener: str = "{", closer: str = "}") -> tuple[str, int]:
    if start >= len(text) or text[start] != opener:
        raise ValueError(f"expected {opener!r} at offset {start}")
    depth = 1
    pos = start + 1
    while pos < len(text):
        char = text[pos]
        if char == "\\":
            pos += 2
            continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return text[start + 1 : pos], pos + 1
        pos += 1
    raise ValueError(f"unterminated {opener}{closer} group at offset {start}")


def replace_command(
    text: str,
    name: str,
    argument_count: int,
    handler: Callable[[list[str], str | None], str],
    *,
    optional: bool = False,
) -> str:
    token = "\\" + name
    pieces: list[str] = []
    cursor = 0
    while True:
        found = text.find(token, cursor)
        if found < 0:
            pieces.append(text[cursor:])
            break
        after_name = found + len(token)
        if after_name < len(text) and text[after_name].isalpha():
            pieces.append(text[cursor:after_name])
            cursor = after_name
            continue
        pieces.append(text[cursor:found])
        pos = after_name
        while pos < len(text) and text[pos].isspace():
            pos += 1
        option: str | None = None
        if optional and pos < len(text) and text[pos] == "[":
            option, pos = extract_group(text, pos, "[", "]")
            while pos < len(text) and text[pos].isspace():
                pos += 1
        arguments: list[str] = []
        try:
            for _ in range(argument_count):
                argument, pos = extract_group(text, pos)
                arguments.append(argument)
                while pos < len(text) and text[pos].isspace():
                    pos += 1
        except ValueError:
            pieces.append(token)
            cursor = after_name
            continue
        pieces.append(handler(arguments, option))
        cursor = pos
    return "".join(pieces)


def replace_tikz(text: str, source_name: str) -> str:
    descriptions = list(TIKZ_DESCRIPTIONS.get(source_name, []))
    token = r"\begin{tikzpicture}"
    end_token = r"\end{tikzpicture}"
    count = 0
    while token in text:
        start = text.index(token)
        end = text.find(end_token, start)
        if end < 0:
            raise ValueError(f"unterminated tikzpicture in {source_name}")
        if count >= len(descriptions):
            raise ValueError(f"missing semantic description for TikZ diagram {count + 1} in {source_name}")
        title, description = descriptions[count]
        replacement = f"\n\\subsection*{{Diagram: {title}}}\n{description}\n"
        text = text[:start] + replacement + text[end + len(end_token) :]
        count += 1
    if count != len(descriptions):
        raise ValueError(f"unused TikZ descriptions for {source_name}: expected {len(descriptions)}, found {count}")
    return text


def expand_inputs(path: Path, markdown_markers: dict[str, Path]) -> str:
    text = replace_tikz(path.read_text(encoding="utf-8"), path.name)

    def tex_input(arguments: list[str], _: str | None) -> str:
        child = (path.parent / arguments[0]).resolve()
        return expand_inputs(child, markdown_markers)

    def markdown_input(arguments: list[str], _: str | None) -> str:
        child = (path.parent / arguments[0]).resolve()
        marker = f"ROBMARKDOWNINPUT{len(markdown_markers):03d}"
        markdown_markers[marker] = child
        return f"\n\n{marker}\n\n"

    text = replace_command(text, "input", 1, tex_input)
    text = replace_command(text, "markdownInput", 1, markdown_input)
    return text


def caption_map() -> dict[str, str]:
    captions: dict[str, list[str]] = {}
    for path in SOURCE.glob("*.tex"):
        text = path.read_text(encoding="utf-8")

        def one(arguments: list[str], _: str | None) -> str:
            captions.setdefault(arguments[0], []).append(arguments[1])
            return ""

        def two(arguments: list[str], _: str | None) -> str:
            captions.setdefault(arguments[0], []).append(arguments[1])
            captions.setdefault(arguments[2], []).append(arguments[3])
            return ""

        replace_command(text, "ROBPhoto", 2, one, optional=True)
        replace_command(text, "ROBPhotoTwo", 4, two)
    return {name: max(values, key=len) for name, values in captions.items()}


def option_title(option: str | None, fallback: str) -> str:
    if not option:
        return fallback
    match = re.search(r"title\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", option)
    return match.group(1) if match else fallback


def replace_environment(text: str, name: str, label: str) -> str:
    begin_token = f"\\begin{{{name}}}"
    end_token = f"\\end{{{name}}}"
    while begin_token in text:
        start = text.rfind(begin_token, 0, text.find(end_token))
        if start < 0:
            break
        begin_end = start + len(begin_token)
        pos = begin_end
        while pos < len(text) and text[pos].isspace():
            pos += 1
        option = None
        if pos < len(text) and text[pos] == "[":
            option, pos = extract_group(text, pos, "[", "]")
        end = text.find(end_token, pos)
        if end < 0:
            raise ValueError(f"unterminated {name} environment")
        title = option_title(option, label)
        body = text[pos:end].strip()
        replacement = f"\n\\subsection*{{{title}}}\n\\begin{{quote}}\n{body}\n\\end{{quote}}\n"
        text = text[:start] + replacement + text[end + len(end_token) :]
    return text


def generic_figures(text: str, captions: dict[str, str]) -> str:
    pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}")

    def replace(match: re.Match[str]) -> str:
        filename = match.group(1)
        caption = captions.get(filename, f"ROB publication image: {Path(filename).stem.replace('-', ' ')}.")
        return f"\\begin{{figure}}\n\\centering\n\\includegraphics{{{filename}}}\n\\caption{{{caption}}}\n\\end{{figure}}"

    return pattern.sub(replace, text)


def prepare_latex(path: Path) -> tuple[str, dict[str, Path]]:
    markdown_markers: dict[str, Path] = {}
    text = expand_inputs(path.resolve(), markdown_markers)
    begin = text.find(r"\begin{document}")
    end = text.rfind(r"\end{document}")
    if begin >= 0 and end > begin:
        text = text[begin + len(r"\begin{document}") : end]

    captions = caption_map()
    text = generic_figures(text, captions)

    text = replace_command(
        text,
        "ROBTitle",
        5,
        lambda a, _: (
            f"\\chapter*{{{a[1]}}}\n\\textbf{{{a[0]}}}\\par\n"
            f"\\emph{{{a[2]}}}\\par\n{a[3]}\\par\n"
            f"\\begin{{figure}}\\centering\\includegraphics{{{a[4]}}}"
            f"\\caption{{Cover image for {a[1]}: {a[2]}}}\\end{{figure}}\n"
        ),
    )
    text = replace_command(
        text,
        "ROBFrontMatter",
        3,
        lambda a, _: (
            f"\\chapter*{{{a[0]}}}\n\\emph{{{a[1]}}}\\par\n{a[2]}\n"
            "Copyright \\copyright\\ 2026 Rodolfo Aramayo / Orbitus Robotics. Photographs are from "
            "the private ROB build archive unless otherwise noted. Generated covers, frontispieces, "
            "story scenes, and conceptual teaching plates are original project illustrations derived "
            "from or inspired by ROB reference photographs. They are illustrations, not documentary "
            "photographs, technical drawings, or evidence of the as-built configuration. Source-code "
            "licenses remain separate and repository-specific.\n"
        ),
    )
    text = replace_command(
        text,
        "ROBSeriesMap",
        1,
        lambda a, _: SERIES_MAP + f"\n\\subsection*{{How to use this book}}\n{a[0]}\n",
    )

    def photo(arguments: list[str], _: str | None) -> str:
        filename, caption = arguments
        return f"\n\\begin{{figure}}\\centering\\includegraphics{{{filename}}}\\caption{{{caption}}}\\end{{figure}}\n"

    def photo_two(arguments: list[str], _: str | None) -> str:
        return photo(arguments[:2], None) + photo(arguments[2:], None)

    def chapter_photo(arguments: list[str], _: str | None) -> str:
        label, title, filename = arguments
        caption = captions.get(filename, f"Chapter image for {title}.")
        return (
            f"\n\\chapter*{{{label}: {title}}}\n"
            f"\\begin{{figure}}\\centering\\includegraphics{{{filename}}}\\caption{{{caption}}}\\end{{figure}}\n"
        )

    text = replace_command(text, "ROBPhoto", 2, photo, optional=True)
    text = replace_command(text, "ROBPhotoTwo", 4, photo_two)
    text = replace_command(text, "ROBChapterPhoto", 3, chapter_photo)
    text = replace_command(
        text,
        "ROBSourceNow",
        2,
        lambda a, _: f"\n\\subsection*{{Source trail --- analyzing now}}\n\\textbf{{File:}} \\nolinkurl{{{a[0]}}}\\par\n\\textbf{{Why it is here:}} {a[1]}\n",
    )
    text = replace_command(text, "ROBFact", 2, lambda a, _: f"\\textbf{{{a[0]}}}: {a[1]}")
    text = replace_command(text, "ROBSource", 1, lambda a, _: f"\n\\emph{{Source trail: {a[0]}}}\n")
    text = replace_command(
        text,
        "ROBPlaceholder",
        1,
        lambda a, _: f"\n\\subsection*{{Builder input needed}}\n\\begin{{quote}}{a[0]}\\end{{quote}}\n",
    )
    text = replace_command(text, "ROBArduinoStatus", 0, lambda _a, _o: ARDUINO_STATUS)
    text = replace_command(text, "ROBAmberStatus", 0, lambda _a, _o: AMBER_STATUS)
    text = replace_command(text, "ROBSourceRoot", 0, lambda _a, _o: SOURCE_ROOT)
    for name, (title, description) in DIAGRAMS.items():
        text = replace_command(
            text,
            name,
            0,
            lambda _a, _o, title=title, description=description: f"\n\\subsection*{{Diagram: {title}}}\n{description}\n",
        )
    for name, value in STATUS_TEXT.items():
        text = replace_command(text, name, 0, lambda _a, _o, value=value: f"\\textbf{{{value}}}")

    for environment, label in BOX_LABELS.items():
        text = replace_environment(text, environment, label)

    text = re.sub(r"\\begin\{center\}|\\end\{center\}", "", text)
    text = re.sub(r"\\begin\{multicols\}\{[^{}]*\}|\\end\{multicols\}", "", text)
    text = re.sub(r"\\(?:tableofcontents|clearpage|mainmatter|frontmatter|newpage)\b", "", text)
    text = re.sub(r"\\(?:SetROBAccent|SetROBChapterPrefix)\{[^{}]*\}", "", text)
    text = replace_command(text, "SetROBVolume", 2, lambda _a, _o: "")
    text = re.sub(r"\\(?:RaggedRight|raggedright|sloppy)\b", "", text)
    text = re.sub(r"\\color\{[^{}]*\}", "", text)
    text = re.sub(r"\\vspace\*?\{[^{}]*\}|\\hfill\b", "", text)
    text = re.sub(r"\\allowbreak\b", "", text)
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = text.replace(
        r"I = \frac{5\,\mathrm{V}-2\,\mathrm{V}}{220\,\Omega} \approx 0.014\,\mathrm{A} = 14\,\mathrm{mA}.",
        r"I = (5 - 2) / 220 = 0.014\;\mathrm{A} = 14\;\mathrm{mA}.",
    )
    text = text.replace(
        r"\text{ratio} = \frac{\text{driven teeth}}{\text{driver teeth}} = \frac{40}{10}=4",
        r"r = 40 / 10 = 4",
    )

    unresolved = sorted(set(re.findall(r"\\(ROB[A-Za-z]+|SetROB[A-Za-z]+)", text)))
    if unresolved:
        raise ValueError(f"unresolved ROB publication macros in {path.name}: {', '.join(unresolved)}")
    return text, markdown_markers


def prepare_manual_markdown(path: Path) -> str:
    latex, markers = prepare_latex(path)
    with tempfile.TemporaryDirectory(prefix="rob-semantic-manual-") as temporary:
        semantic = Path(temporary) / "manual.tex"
        converted = Path(temporary) / "manual.md"
        semantic.write_text(latex, encoding="utf-8")
        subprocess.run(
            ["pandoc", str(semantic), "--from=latex", "--to=gfm", "--wrap=none", "-o", str(converted)],
            cwd=PROJECT,
            check=True,
        )
        markdown = converted.read_text(encoding="utf-8")
    figure_pattern = re.compile(
        r'(<figure>\s*<img src="[^"]+")\s*/>\s*<figcaption>(.*?)</figcaption>',
        re.DOTALL,
    )

    def add_alt(match: re.Match[str]) -> str:
        plain_caption = re.sub(r"<[^>]+>", "", match.group(2))
        plain_caption = " ".join(plain_caption.split())
        return f'{match.group(1)} alt="{escape(plain_caption, quote=True)}" />\n<figcaption>{match.group(2)}</figcaption>'

    markdown = figure_pattern.sub(add_alt, markdown)
    for marker, child in markers.items():
        if marker not in markdown:
            raise ValueError(f"Pandoc dropped embedded Markdown marker {marker}")
        markdown = markdown.replace(marker, child.read_text(encoding="utf-8"))
    return markdown
