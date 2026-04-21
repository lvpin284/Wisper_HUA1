#!/usr/bin/env python3
"""Extract audio from video files.

Directory layout expected (new format):
    <base_dir>/
        video/   <- input video files (MP4, MKV, AVI, MOV, …)
        audio/   <- extracted WAV files are written here

Usage example:
    python extract_audio.py /data/fc702acbf33048f493d046821f22655a/ru_test_0417
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".ts", ".m4v"}


def extract_audio(video_file: Path, audio_file: Path) -> None:
    """Extract audio from *video_file* and write it to *audio_file* (WAV)."""
    cmd = [
        "ffmpeg",
        "-y",                  # overwrite output without asking
        "-i", str(video_file),
        "-vn",                 # no video
        "-acodec", "pcm_s16le",
        "-ar", "16000",        # 16 kHz – optimal sample rate for Whisper
        "-ac", "1",            # mono
        str(audio_file),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ffmpeg failed for {video_file.name}:\n{result.stderr.strip()}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract audio from video files in <base_dir>/video/ to <base_dir>/audio/."
    )
    parser.add_argument(
        "base_dir",
        type=Path,
        help="Base directory that contains the 'video/' sub-folder "
             "(e.g. /data/.../ru_test_0417)",
    )
    parser.add_argument(
        "--video-dir",
        type=Path,
        default=None,
        help="Override the video input directory (default: <base_dir>/video)",
    )
    parser.add_argument(
        "--audio-dir",
        type=Path,
        default=None,
        help="Override the audio output directory (default: <base_dir>/audio)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    base_dir: Path = args.base_dir
    video_dir: Path = args.video_dir or base_dir / "video"
    audio_dir: Path = args.audio_dir or base_dir / "audio"

    if not video_dir.exists() or not video_dir.is_dir():
        raise SystemExit(f"Video directory does not exist: {video_dir}")

    audio_dir.mkdir(parents=True, exist_ok=True)

    video_files = sorted(
        f for f in video_dir.iterdir()
        if f.is_file() and f.suffix.lower() in VIDEO_EXTENSIONS
    )
    if not video_files:
        raise SystemExit(f"No video files found in: {video_dir}")

    # Check that ffmpeg is available
    check = subprocess.run(["ffmpeg", "-version"], capture_output=True)
    if check.returncode != 0:
        raise SystemExit(
            "ffmpeg is not installed or not in PATH. "
            "Install it with: sudo apt install ffmpeg  (Ubuntu/Debian) "
            "or brew install ffmpeg  (macOS)"
        )

    for video_file in video_files:
        audio_file = audio_dir / f"{video_file.stem}.wav"
        print(f"Extracting: {video_file.name} -> {audio_file.name} ...", end=" ", flush=True)
        try:
            extract_audio(video_file, audio_file)
            print("OK")
        except RuntimeError as exc:
            print(f"FAILED\n{exc}", file=sys.stderr)

    print(f"\nAudio files written to: {audio_dir}")


if __name__ == "__main__":
    main()
