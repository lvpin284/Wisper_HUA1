#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def format_timestamp(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    total_secs, ms = divmod(milliseconds, 1000)
    return f"{total_secs}.{ms:03d}"


def transcribe_file(model, input_file: Path, output_file: Path, language: str) -> None:
    result = model.transcribe(str(input_file), language=language)
    segments = result.get("segments", [])

    lines = []
    for segment in segments:
        start = format_timestamp(float(segment.get("start", 0.0)))
        end = format_timestamp(float(segment.get("end", 0.0)))
        text = str(segment.get("text", "")).strip()
        if text:
            lines.append(f"{start} {end} 0 {text}")

    output_file.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch transcribe MP4 files in a folder to TXT with Whisper."
    )
    parser.add_argument("input_dir", type=Path, help="Path to the folder containing MP4 files")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Path to output TXT files (default: same as input_dir)",
    )
    parser.add_argument(
        "--model",
        default="base",
        help="Whisper model name, e.g. tiny/base/small/medium/large",
    )
    parser.add_argument(
        "--language",
        default="ru",
        help="Language code for transcription (default: ru)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir or input_dir

    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Input directory does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    mp4_files = sorted(input_dir.glob("*.mp4"))
    if not mp4_files:
        raise SystemExit(f"No .mp4 files found in: {input_dir}")

    try:
        import whisper
    except ImportError as exc:
        raise SystemExit(
            "Cannot import whisper. Make sure the 'whisper/' package directory is present in the repo "
            "and all dependencies are installed: pip install -r requirements.txt"
        ) from exc

    model = whisper.load_model(str(Path(args.model).expanduser()))

    for mp4_file in mp4_files:
        output_file = output_dir / f"{mp4_file.stem}.txt"
        transcribe_file(model, mp4_file, output_file, args.language)
        print(f"Done: {mp4_file.name} -> {output_file}")


if __name__ == "__main__":
    main()
