# Installation and running

How to install the ASCII Art Generator, run it from a clone, and use the standalone executables.
For what you can type once it runs, see [usage.md](usage.md).

## Requirements

- Python 3.12+ (needed because `cli.py` uses a backslash inside an f-string
  expression, a syntax only legal since PEP 701)
- Standard library only, with one deliberate exception: image-to-ASCII
  conversion (`convert image ...`) needs [Pillow](https://pypi.org/project/Pillow/)
  to decode image files. Everything else has no external dependencies.
- Optional: [pyfiglet](https://pypi.org/project/pyfiglet/) for proper FIGlet
  fonts in text-to-ASCII (`write ...`). Without it, `write` still works using
  the simpler built-in fonts.

## Install from source

Works the same on Windows, Linux, and macOS. If you only want to try it
without installing Python, grab a standalone executable instead (see
[Standalone executables](#standalone-executables-no-python-needed)).

The recommended way to install from source is [pipx](https://pipx.pypa.io/)
(or `uv`), which puts the command on your `PATH` in its own isolated
environment and works even where the system Python is locked down.

One step, straight from GitHub:

```bash
pipx install "ascii-art-generator[all] @ git+https://github.com/JoaoTomas991/ascii-art-generator.git"
# or: uv tool install "ascii-art-generator[all] @ git+https://github.com/JoaoTomas991/ascii-art-generator.git"
```

Or from a clone, which is also what you want if you plan to change the code:

```bash
git clone https://github.com/JoaoTomas991/ascii-art-generator.git
cd ascii-art-generator
pipx install ".[all]"             # or: uv tool install ".[all]"
```

That installs an `ascii-art-generator` command on your `PATH`, a native launcher
on each platform (`ascii-art-generator.exe` on Windows), so you never have to work
out which Python binary to call. The shorter `ascii-generator` also works as an
alias. `[all]` also enables image-to-ASCII
conversion (Pillow) and FIGlet text fonts (pyfiglet). Use `".[images]"` or
`".[fonts]"` for only one of them, or plain `"."` for neither.

Getting pipx: `sudo apt install pipx` (Debian/Ubuntu), `brew install pipx`
(macOS), `pip install pipx` (Windows).

For development, use an editable install inside a virtual environment:

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[all]"
```

On Debian, Ubuntu, and Homebrew Python, a plain `pip install` outside a
virtual environment fails with `externally-managed-environment`. Use pipx or
a venv as above. On Debian, `python3 -m venv` may also need
`sudo apt install python3-venv`.

Other ways to get the same dependencies:

```bash
pip install -r requirements.txt
# or
make install
# or, on Debian/Ubuntu (no pip needed)
sudo apt install python3-pil python3-pyfiglet
```

Nothing has to be installed to use shapes, text, patterns, or animations. You
can always run the scripts in place instead (see
[Running without installing](#running-without-installing) below).

## Running without installing

`run.py` is the same entry point and works straight from a clone. The catch is
that the interpreter has a different name per platform, so no single
command works everywhere:

```bash
python3 run.py "draw a heart"   # Linux, macOS
python run.py "draw a heart"    # Windows
```

On Windows, a bare `python3` is usually the Microsoft Store stub, which prints
an install prompt instead of running anything. This is the reason
the installed `ascii-art-generator` command (see [Install from source](#install-from-source)) is the recommended path.

## Unix-only shortcuts

The `Makefile` and `start.sh` are conveniences for Linux and macOS; `make` is
not available on Windows by default, and `start.sh` needs a POSIX shell. The
`Makefile` calls `python3`, overridable with `make run PYTHON=python`;
`start.sh` probes `python3`, `python`, and `py` and uses the first one that is
actually 3.12+.

```bash
make run               # menu mode
make intelligent       # intelligent mode
make command-draw      # draw a rectangle 10x5
make command-circle    # make a circle with radius 8
make command-heart     # draw a heart
make command-tree      # create a tree with height 10
make command-banner    # make a banner with text ASCII ART
make command-text      # write HELLO with font banner
```

`./start.sh` opens a small startup menu (menu mode, intelligent mode, direct
command, or help).

## Running on Windows

The generator itself is plain Python and runs natively on Windows; only the
`start.sh` and `Makefile` helpers need a Unix shell. Use the `py` launcher
(installed with Python from [python.org](https://www.python.org/downloads/windows/))
in PowerShell or Command Prompt instead:

```powershell
git clone https://github.com/JoaoTomas991/ascii-art-generator.git
cd ascii-art-generator

# optional: image-to-ASCII and FIGlet fonts
py -m pip install -r requirements.txt

py run.py                                   # menu mode
py run.py --intelligent                     # intelligent mode
py run.py "draw a heart size 2 color red"   # direct command
```

Notes:

- If `py` isn't found, use `python` instead (`python run.py ...`).
- Colors and Unicode emojis work best in
  [Windows Terminal](https://aka.ms/terminal) (the default on Windows 11).
  The generator also enables ANSI color support in the classic
  `cmd.exe`/PowerShell console on Windows 10+.
- Words taught with `teach` are saved to
  `%USERPROFILE%\.config\ascii_generator\learned_words.json`.
- For `start.sh` / `make` shortcuts, use WSL or Git Bash, or just run the
  equivalent `py run.py ...` command shown above.

macOS works the same as Linux (`python3 run.py`, `make`, `./start.sh`). For
true-color image output (`convert image ... color`), use a terminal with
24-bit color support such as iTerm2.

## Standalone executables (no Python needed)

A GitHub Actions workflow
([`.github/workflows/build-executables.yml`](../.github/workflows/build-executables.yml))
uses [PyInstaller](https://pyinstaller.org/) to build a single-file
executable for Windows, macOS and Linux, with Pillow and the FIGlet fonts
bundled in. Each build is smoke-tested before it's published.

To get a build:

- For a released version, push a tag like `v1.0.0`. That attaches the three
  executables to the tag's page under *Releases*.
- For any commit, open the *Actions* tab, then *Build executables* → *Run
  workflow*. When it finishes, download the executables from the run's
  *Artifacts* section (they come zipped).

To run it:

```powershell
# Windows: double-click for the menu, or from PowerShell / cmd:
.\ascii-art-generator-windows.exe "draw a heart size 2 color red"
```

```bash
# macOS / Linux: mark it executable first
chmod +x ascii-art-generator-linux
./ascii-art-generator-linux "draw a heart size 2 color red"
```

Notes:

- The executables aren't code-signed. Windows SmartScreen or antivirus
  software may warn about them (choose *More info* → *Run anyway*). On
  macOS, run `xattr -d com.apple.quarantine ascii-art-generator-macos` once, or
  allow it under *System Settings → Privacy & Security*.
- The macOS build targets Apple Silicon (M1 and later).
- A single-file build unpacks itself on each launch, so it takes a second
  or two to start.
