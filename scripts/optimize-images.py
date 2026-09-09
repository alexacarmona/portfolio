#!/usr/bin/env python3
"""Build web-sized copies in opt/ for every image the site references."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPT = ROOT / "opt"
INDEX = ROOT / "index.html"
MAX_EDGE = "1800"
JPEG_QUALITY = "70"
SKIP_EXT = {".svg", ".gif", ".mp4", ".webm", ".mov", ".pdf"}
IMG_RE = re.compile(r"""['"]([^'"]+\.(?:jpe?g|png|webp|gif|JPE?G|PNG|WEBP|GIF))['"]""")


def referenced_paths() -> list[Path]:
    text = INDEX.read_text(encoding="utf-8", errors="replace")
    found = []
    for raw in IMG_RE.findall(text):
        p = raw.replace("%20", " ").replace("%2B", "+").lstrip("./")
        if p.startswith(("http://", "https://", "opt/", "videos/")):
            continue
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


def run_sips(args: list[str]) -> bool:
    result = subprocess.run(["sips", *args], capture_output=True)
    return result.returncode == 0


def optimize(src: Path) -> None:
    rel = src.relative_to(ROOT)
    dest = OPT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    src_size = src.stat().st_size

    if ext in SKIP_EXT or ext == ".gif":
        if not dest.exists() or dest.stat().st_size != src_size:
            dest.write_bytes(src.read_bytes())
        return

    if dest.exists() and 20_000 < dest.stat().st_size <= 500_000 and dest.stat().st_size < src_size:
        return

    tmp_args = ["-Z", MAX_EDGE]
    if ext in {".jpg", ".jpeg"} or src_size > 500_000:
        tmp_args += ["-s", "format", "jpeg", "-s", "formatOptions", JPEG_QUALITY]
        out = dest if ext in {".jpg", ".jpeg"} else dest.with_suffix(".jpg")
        ok = run_sips([*tmp_args, str(src), "--out", str(out)])
        if ok and ext == ".png" and out.exists():
            # Keep the filename the site expects.
            dest.write_bytes(out.read_bytes())
            if out != dest:
                out.unlink(missing_ok=True)
        return

    run_sips(["-Z", MAX_EDGE, str(src), "--out", str(dest)])


def main() -> None:
    OPT.mkdir(exist_ok=True)
    paths = referenced_paths()
    print(f"optimizing {len(paths)} referenced images into opt/")
    for i, src in enumerate(paths, 1):
        optimize(src)
        if i % 25 == 0 or i == len(paths):
            print(f"  {i}/{len(paths)}  {src.name}")
    print("done")


if __name__ == "__main__":
    main()
