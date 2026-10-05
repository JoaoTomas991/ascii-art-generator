# 0004. Make a stale installed copy visible instead of silently running old code

Date: 2026-10-05
Status: Accepted

## Context

The `ascii-generator` command is installed with `uv tool install .` (or
`pip install .`). A regular install copies the sources into the tool's own
environment, so the command keeps running that snapshot while the project
folder moves on. In practice this produced confusing reports: after removing
a menu item and changing "Random Art", the installed command still showed the
old menu, and it looked like the change had not worked.

Two related problems surfaced while fixing it:

- An orphaned `ascii-generator.exe` from an earlier install failed with
  `ModuleNotFoundError: No module named 'run'`.
- Reinstalling failed with "Access denied" on Windows while the program was
  still running, because the OS locks a running `.exe`. The tool cannot
  replace itself.

## Decision

Detect and report the problem; do not try to fix it automatically.

- A new module, `ascii_art_generator/install_info.py`, works out where the
  running code comes from (editable install, installed copy, source checkout,
  standalone executable) using the PEP 610 `direct_url.json` that the
  installer records.
- `ascii-generator --version` prints the version, that mode, the code path,
  the source folder and the git branch and commit.
- On start-up, an installed copy whose source folder has `.py` files newer
  than the install prints a warning to stderr with the reinstall command
  and then carries on running.
- The documented way to develop is an editable install
  (`uv tool install --editable .`), where the command reads the project
  folder directly and cannot go stale.

## Alternatives considered

- Reinstalling automatically when stale would fail on Windows, where the
  running `.exe` cannot be replaced, and it would change the user's
  environment without being asked.
- Refusing to start when stale turns a harmless mismatch into an outage.
- Embedding the git commit at build time and comparing would need build
  tooling and still could not see the source folder moving on.
- Doing nothing and documenting it would repeat the original problem:
  nothing told the user which code was running.

## Consequences

- "Which code am I running?" has a one-command answer, and the usual
  stale-copy case announces itself.
- The warning goes to stderr, so redirected or piped output is unchanged.
- The check is best effort and silent on failure. It only works for installs
  made from a local folder, and it compares modification times, so it does
  nothing if the folder was moved or deleted.
- With an editable install the command follows whichever branch is checked
  out in the project folder.
- Re-install still has to be done by the user, with the program closed on
  Windows.
