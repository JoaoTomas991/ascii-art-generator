#!/usr/bin/env python3
"""
Build the static browser version of the ASCII Generator into _site/.

The page (web/) runs the real Python package inside Pyodide, so the build only
has to copy the page, zip the package next to it, and bake the startup logo
into the HTML. Standard library only (pyfiglet is used for the logo when it is
installed, exactly as in the terminal).

    python3 scripts/build_web.py            # writes _site/
    python3 scripts/build_web.py --serve    # ...and serves it on http://localhost:8000
"""

import argparse
import html
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "ascii_art_generator"
WEB = ROOT / "web"
LOGO_PLACEHOLDER = "<!--BANNER_LOGO-->"


def build(out: Path) -> None:
    # Fail before touching the output directory if the page cannot take the logo.
    if LOGO_PLACEHOLDER not in (WEB / "index.html").read_text(encoding="utf-8"):
        raise SystemExit(f"{LOGO_PLACEHOLDER} not found in web/index.html")

    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(WEB, out)

    # The package, zipped the way Pyodide's unpackArchive expects it.
    with zipfile.ZipFile(out / "ascii_art_generator.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE.rglob("*.py")):
            archive.write(path, path.relative_to(ROOT).as_posix())

    # The same logo the terminal menu shows.
    sys.path.insert(0, str(ROOT))
    from ascii_art_generator.intro import title_lines

    page = out / "index.html"
    logo = html.escape("\n".join(title_lines()))
    page.write_text(page.read_text(encoding="utf-8").replace(LOGO_PLACEHOLDER, logo), encoding="utf-8")

    (out / ".nojekyll").write_text("", encoding="utf-8")   # serve files as they are
    print(f"Built {out} ({sum(1 for _ in out.rglob('*') if _.is_file())} files)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=ROOT / "_site", help="output directory (default: _site)")
    parser.add_argument("--serve", action="store_true", help="serve the result on http://localhost:8000")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    build(args.out)

    if args.serve:
        import functools
        import http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(args.out))
        with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
            print(f"Serving on http://localhost:{args.port}  (Ctrl+C to stop)")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print()


if __name__ == "__main__":
    main()
