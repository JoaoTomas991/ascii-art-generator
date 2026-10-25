"""
Where is the running code coming from, and is it up to date?

A regular (non-editable) `pip install .` / `uv tool install .` copies the
sources into site-packages, so the installed command keeps running that
snapshot while the project folder moves on. This module answers "which code is
this?" for `--version`, and detects the stale-copy case so the entry point can
warn about it. Everything here is best effort: any failure just means "no
information", never an exception.
"""

import subprocess
from importlib import metadata
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import unquote, urlparse
from urllib.request import url2pathname
import json
import sys

from . import __version__

DIST_NAME = "ascii-art-generator"
PACKAGE_DIR = Path(__file__).resolve().parent


def _direct_url(dist: "metadata.Distribution") -> Optional[dict]:
    """The PEP 610 record of how the distribution was installed, if any."""
    try:
        text = dist.read_text("direct_url.json")
        return json.loads(text) if text else None
    except (OSError, ValueError):
        return None


def _source_dir(direct_url: Optional[dict]) -> Optional[Path]:
    """Project folder a local install was made from."""
    if not direct_url:
        return None
    parsed = urlparse(direct_url.get("url", ""))
    if parsed.scheme != "file":
        return None
    path = Path(url2pathname(unquote(parsed.path)))
    return path if path.is_dir() else None


def _install_time(dist: "metadata.Distribution") -> Optional[float]:
    """When the copy was installed: mtime of its direct_url.json."""
    for file in dist.files or []:
        if file.name == "direct_url.json":
            try:
                return Path(dist.locate_file(file)).stat().st_mtime
            except OSError:
                return None
    return None


def _newest_source_mtime(source_dir: Path) -> Optional[float]:
    files = list((source_dir / "ascii_art_generator").glob("*.py"))
    files.append(source_dir / "run.py")
    times = []
    for f in files:
        try:
            times.append(f.stat().st_mtime)
        except OSError:
            pass
    return max(times) if times else None


def _git(source_dir: Path, *args: str) -> Optional[str]:
    try:
        out = subprocess.run(
            ["git", "-C", str(source_dir), *args],
            capture_output=True, text=True, timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() or None if out.returncode == 0 else None


def describe() -> Dict[str, Optional[str]]:
    """Facts about the running code, for `--version`."""
    info: Dict[str, Optional[str]] = {
        "version": __version__,
        "code": str(PACKAGE_DIR),
        "mode": "source checkout",
        "source": None,
        "branch": None,
        "commit": None,
    }
    if getattr(sys, "frozen", False):
        info["mode"] = "standalone executable"
        return info

    source = None
    try:
        dist = metadata.distribution(DIST_NAME)
    except metadata.PackageNotFoundError:
        dist = None
    if dist is not None:
        direct_url = _direct_url(dist)
        source = _source_dir(direct_url)
        if direct_url and direct_url.get("dir_info", {}).get("editable"):
            info["mode"] = "editable install"
        elif not (PACKAGE_DIR.parent / "setup.py").exists():
            info["mode"] = "installed copy"
    info["source"] = str(source) if source else None

    git_dir = source if source else PACKAGE_DIR.parent
    if (git_dir / ".git").exists():
        info["branch"] = _git(git_dir, "branch", "--show-current")
        info["commit"] = _git(git_dir, "rev-parse", "--short", "HEAD")
    return info


def stale_copy_warning() -> Optional[str]:
    """A warning when this is an installed copy older than its source folder."""
    if getattr(sys, "frozen", False):
        return None
    try:
        dist = metadata.distribution(DIST_NAME)
        direct_url = _direct_url(dist)
        if not direct_url or direct_url.get("dir_info", {}).get("editable"):
            return None
        source = _source_dir(direct_url)
        if source is None or source in PACKAGE_DIR.parents:
            return None  # not a local-folder install, or running the folder itself
        installed = _install_time(dist)
        newest = _newest_source_mtime(source)
        if installed is None or newest is None or newest <= installed:
            return None
    except Exception:
        return None
    return (
        f"Warning: this installed copy is older than the source folder "
        f"({source}).\n"
        f"         Reinstall to pick up the changes: "
        f"uv tool install --force --editable ."
    )
