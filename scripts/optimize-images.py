#!/usr/bin/env python3
"""Build high-quality web copies in opt/ from the original images."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPT = ROOT / "opt"
INDEX = ROOT / "index.html"
MAX_EDGE = "3200"
JPEG_QUALITY = "85"
SKIP_EXT = {".svg", ".gif", ".mp4", ".webm", ".mov", ".pdf"}
IMG_RE = re.compile(r"""['"]([^'"]+\.(?:jpe?g|png|webp|gif|JPE?G|PNG|WEBP|GIF))['"]""")
SPECIAL_SOURCES = {
    "alexa_20264803-2-hero.jpg": ROOT / "alexa_20264803 2.jpg",
}


def referenced_originals() -> list[Path]:
    text = INDEX.read_text(encoding="utf-8", errors="replace")
    found = []
    for raw in IMG_RE.findall(text):
        p = raw.replace("%20", " ").replace("%2B", "+").lstrip("./")
        if p.startswith(("http://", "https://", "videos/")):
            continue
        if p.startswith("opt/"):
            p = p[4:]
        path = ROOT / p
        if path.is_file():
            found.append(path)
    seen = set()
    out = []
    for p in found:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def original_for_opt(dest: Path) -> Path | None:
    rel = dest.relative_to(OPT)
    special = SPECIAL_SOURCES.get(rel.as_posix()) or SPECIAL_SOURCES.get(rel.name)
    if special and special.is_file():
        return special
    src = ROOT / rel
    if src.is_file() and src != dest:
        return src
    return None


def run_sips(args: list[str]) -> bool:
    result = subprocess.run(["sips", *args], capture_output=True)
    return result.returncode == 0


def pixel_size(path: Path) -> tuple[int, int]:
    result = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        capture_output=True,
        text=True,
    )
    width = height = 0
    for line in result.stdout.splitlines():
        if "pixelWidth" in line:
            width = int(line.split()[-1])
        elif "pixelHeight" in line:
            height = int(line.split()[-1])
    return width, height


def optimize(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    src_size = src.stat().st_size

    if ext in SKIP_EXT or ext == ".gif":
        dest.write_bytes(src.read_bytes())
        return

    width, height = pixel_size(src)
    max_edge = max(width, height)
    needs_resize = max_edge > int(MAX_EDGE)

    if ext in {".jpg", ".jpeg"}:
        if not needs_resize:
            dest.write_bytes(src.read_bytes())
            return
        ok = run_sips(
            [
                "-Z",
                MAX_EDGE,
                "-s",
                "format",
                "jpeg",
                "-s",
                "formatOptions",
                JPEG_QUALITY,
                str(src),
                "--out",
                str(dest),
            ]
        )
        if not ok:
            dest.write_bytes(src.read_bytes())
        return

    # Keep real PNGs/WebPs instead of swapping in JPEG bytes.
    if not needs_resize:
        dest.write_bytes(src.read_bytes())
        return
    ok = run_sips(["-Z", MAX_EDGE, str(src), "--out", str(dest)])
    if not ok or not dest.exists():
        dest.write_bytes(src.read_bytes())
        return
    if dest.stat().st_size > src_size:
        dest.write_bytes(src.read_bytes())


def main() -> None:
    OPT.mkdir(exist_ok=True)
    jobs: list[tuple[Path, Path]] = []
    seen_dest = set()

    for src in referenced_originals():
        dest = OPT / src.relative_to(ROOT)
        jobs.append((src, dest))
        seen_dest.add(dest)

    for dest in OPT.rglob("*"):
        if not dest.is_file():
            continue
        if dest in seen_dest:
            continue
        src = original_for_opt(dest)
        if src:
            jobs.append((src, dest))
            seen_dest.add(dest)

    for dest_name, src in SPECIAL_SOURCES.items():
        dest = OPT / dest_name
        if src.is_file():
            jobs.append((src, dest))

    print(f"optimizing {len(jobs)} images into opt/ at {MAX_EDGE}px q{JPEG_QUALITY}")
    for i, (src, dest) in enumerate(jobs, 1):
        optimize(src, dest)
        if i % 25 == 0 or i == len(jobs):
            print(f"  {i}/{len(jobs)}  {dest.name}")
    print("done")


if __name__ == "__main__":
    main()
