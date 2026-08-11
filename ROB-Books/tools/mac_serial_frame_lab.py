#!/usr/bin/env python3
"""Offline ROB message lab for a Mac Terminal.

This teaching program builds and checks text frames. It never opens a serial
device and therefore cannot command ROB.
"""

import argparse


FIELD_NAMES = (
    "left brake",
    "left speed",
    "right brake",
    "right speed",
    "flipper brake",
    "flipper speed",
    "linear actuator speed",
)


def encode_value(value):
    """Return one signed, five-character field such as +0100 or -0025."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("each field must be an integer")
    if not -9999 <= value <= 9999:
        raise ValueError("a five-character signed field holds -9999 to +9999")
    return f"{value:+05d}"


def build_frame(values):
    """Build the historical seven-field, 42-character ROB text frame."""
    if len(values) != len(FIELD_NAMES):
        raise ValueError("ROB frames require exactly seven values")
    frame = "~" + ",".join(encode_value(value) for value in values)
    assert len(frame) == 42
    return frame


def parse_frame(frame):
    """Validate a frame completely before returning its named values."""
    if len(frame) != 42 or not frame.startswith("~"):
        raise ValueError("a frame must start with ~ and contain 42 characters")

    fields = frame[1:].split(",")
    if len(fields) != len(FIELD_NAMES):
        raise ValueError("a frame must contain seven comma-separated fields")

    values = []
    for field in fields:
        if len(field) != 5 or field[0] not in "+-" or not field[1:].isdigit():
            raise ValueError(f"invalid field: {field!r}")
        values.append(int(field))
    return dict(zip(FIELD_NAMES, values))


def argument_parser():
    parser = argparse.ArgumentParser(
        description=(
            "Build or inspect ROB's historical 42-character text frame. "
            "This offline teaching tool never opens a serial device."
        )
    )
    parser.add_argument(
        "frame",
        nargs="?",
        help="an existing frame to validate, for example '~+0000,+0000,...'",
    )
    parser.add_argument("--left-brake", type=int, default=None)
    parser.add_argument("--left-speed", type=int, default=None)
    parser.add_argument("--right-brake", type=int, default=None)
    parser.add_argument("--right-speed", type=int, default=None)
    parser.add_argument("--flipper-brake", type=int, default=None)
    parser.add_argument("--flipper-speed", type=int, default=None)
    parser.add_argument("--actuator-speed", type=int, default=None)
    return parser


def main():
    parser = argument_parser()
    arguments = parser.parse_args()
    overrides = (
        arguments.left_brake,
        arguments.left_speed,
        arguments.right_brake,
        arguments.right_speed,
        arguments.flipper_brake,
        arguments.flipper_speed,
        arguments.actuator_speed,
    )

    if arguments.frame is not None and any(value is not None for value in overrides):
        parser.error("pass either an existing frame or named field options, not both")

    if arguments.frame is not None:
        frame = arguments.frame
    else:
        frame = build_frame([0 if value is None else value for value in overrides])

    try:
        decoded = parse_frame(frame)
    except (TypeError, ValueError) as error:
        raise SystemExit(f"invalid frame: {error}") from error

    print("frame:", frame)
    print("length:", len(frame))
    for name, value in decoded.items():
        print(f"{name:23} {value:+d}")


if __name__ == "__main__":
    main()
