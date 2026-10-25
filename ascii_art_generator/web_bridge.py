"""
Run a command and get its output back as text, without a terminal.

The browser build (see web/ and scripts/build_web.py) runs this package inside
Pyodide and calls run_command() for every command typed on the page. The CLI
prints its results, so the output is captured and returned as one string with
its ANSI colour codes intact; the page turns those into HTML.

Standard library only. One ASCIIArtCLI is kept for the whole session so that
`teach <word> as <mood>` sticks until the page is closed.
"""

import contextlib
import io
from typing import Optional

from .cli import ASCIIArtCLI

_cli: Optional[ASCIIArtCLI] = None

# The terminal trusts the user with any size; a browser tab would freeze on a
# 100000x100000 rectangle, so the page refuses sizes beyond this.
MAX_DIMENSION = 300
_SIZE_KEYS = ('width', 'height', 'radius', 'size')
_LEAVE_WORDS = {'q', 'quit', 'exit', 'menu', 'm'}


def _get_cli() -> ASCIIArtCLI:
    global _cli
    if _cli is None:
        _cli = ASCIIArtCLI()
        _cli.intelligent_mode = True
    return _cli


def _too_big(parsed: dict) -> bool:
    """True when any size parameter (also inside compound commands) is unreasonably large."""
    for part in parsed.get('parts', []) or [parsed]:
        params = part.get('params', {})
        if any(isinstance(params.get(key), int) and params[key] > MAX_DIMENSION for key in _SIZE_KEYS):
            return True
    return False


def run_command(text: str) -> str:
    """Run one English command; return everything it printed (ANSI codes included)."""
    text = text.strip()
    if not text:
        return ''

    cli = _get_cli()
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        try:
            if text.lower() in _LEAVE_WORDS:
                print("There is nothing to quit here - just close the tab.")
            elif text.lower().startswith('teach '):
                cli._handle_teach_command(text)
            else:
                parsed = cli.parser.parse_command(text)
                if parsed and _too_big(parsed):
                    print(f"That size is too big for the browser. Keep every number at {MAX_DIMENSION} or below.")
                elif not parsed:
                    print("Could not understand. Try this:")
                    cli._suggest_commands(text)
                elif parsed.get('command') == 'quit':
                    print("There is nothing to quit here - just close the tab.")
                else:
                    cli.execute_parsed_command(parsed)
        except SystemExit:
            print("That command is not available in the browser.")
        except Exception as error:   # never let one bad command break the page
            print(f"Error: {error}")
    return buffer.getvalue()
