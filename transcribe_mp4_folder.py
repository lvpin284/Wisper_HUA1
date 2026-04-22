#!/usr/bin/env python3
"""Batch transcribe audio/video files to TXT using Whisper.

Supports two layouts:

  Classic layout  (original behaviour):
      python transcribe_mp4_folder.py <input_dir> [--output-dir <output_dir>]
      Reads *.mp4 from <input_dir>, writes *.txt to <output_dir>.

  New layout  (use --new-layout):
      python transcribe_mp4_folder.py <base_dir> --new-layout
      Reads audio files from  <base_dir>/audio/
      Writes TXT files to     <base_dir>/audio/text/
"""
from __future__ import annotations

import argparse
from pathlib import Path

AUDIO_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".mp4", ".mkv"}


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
            lines.append(f"{start}\t{end}\t0\t{text}")

    output_file.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch transcribe audio/video files in a folder to TXT with Whisper."
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help=(
            "Classic layout: path to the folder containing MP4 files. "
            "New layout (--new-layout): base directory that contains audio/ and video/ sub-folders."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Path to output TXT files (default: same as input_dir). Ignored when --new-layout is used.",
    )
    parser.add_argument(
        "--new-layout",
        action="store_true",
        help=(
            "Use the new directory layout: read audio files from <input_dir>/audio/ "
            "and write TXT files to <input_dir>/audio/text/."
        ),
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

    if args.new_layout:
        base_dir = args.input_dir
        input_dir = base_dir / "audio"
        output_dir = base_dir / "audio" / "text"
    else:
        input_dir = args.input_dir
        output_dir = args.output_dir or input_dir

    if not input_dir.exists() or not input_dir.is_dir():
        raise SystemExit(f"Input directory does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    if args.new_layout:
        audio_files = sorted(
            f for f in input_dir.iterdir()
            if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS
        )
    else:
        audio_files = sorted(input_dir.glob("*.mp4"))

    if not audio_files:
        raise SystemExit(f"No audio/video files found in: {input_dir}")

    try:
        import whisper
    except ImportError as exc:
        raise SystemExit(
            "Cannot import whisper. Make sure the 'whisper/' package directory is present in the repo "
            "and all dependencies are installed: pip install -r requirements.txt"
        ) from exc

    model = whisper.load_model(str(Path(args.model).expanduser()))

    for audio_file in audio_files:
        output_file = output_dir / f"{audio_file.stem}.txt"
        transcribe_file(model, audio_file, output_file, args.language)
        print(f"Done: {audio_file.name} -> {output_file}")


if __name__ == "__main__":
    main()
