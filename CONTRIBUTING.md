# Contributing to ASCII Art Generator

Thank you for your interest in contributing to **ASCII Art Generator**.

This is a personal project maintained by a single contributor. External contributions are welcome, but all changes should be proposed through issues and pull requests to keep the project organized.

## Getting Started

1. Fork the repository.
2. Clone your fork:

   ```bash
   git clone https://github.com/YOUR_USERNAME/ascii-art-generator.git
   cd ascii-art-generator
   ```

3. Add the original repository as `upstream`:

   ```bash
   git remote add upstream https://github.com/JoaoTomas991/ascii-art-generator.git
   ```

4. Create a virtual environment and install the dependencies:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

   On Windows, activate the environment with:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

## Technical Requirements

- Python **3.12 or newer**
- `pip`
- Pillow, installed through `requirements.txt`, when using image-to-ASCII conversion
- pyfiglet, also in `requirements.txt` (optional), for the FIGlet fonts of `write`

## Issues

Before starting a significant change, open an issue describing the proposal. This helps avoid duplicated work and allows the solution to be discussed before implementation.

When opening an issue:

- Use a clear and specific title.
- Explain the problem or proposed improvement.
- Include reproduction steps when reporting a bug.
- Add example commands and expected results.
- Specify the Python version being used.

## Branches

The main branch is `main`. External contributions should not be made directly to this branch.

Create a descriptive branch from `main`:

```bash
git fetch upstream
git checkout main
git rebase upstream/main
git checkout -b type/change-name
```

Recommended branch naming conventions:

- `feature/new-feature`
- `fix/bug-fix`
- `docs/documentation-update`
- `test/add-tests`
- `refactor/code-improvement`

## Development

The main source code is located in `ascii_art_generator/`. Before submitting changes, run:

```bash
make test
```

You should also manually test commands related to your change. For example:

```bash
python3 run.py "draw a rectangle 10x5"
python3 run.py "write HELLO"
```

If you modify image conversion, test it with a real image and confirm that Pillow is installed.

## Code Standards

- Use Python 3.12+.
- Follow PEP 8 conventions.
- Use clear names for variables, functions, and classes.
- Keep functions focused and reasonably simple.
- Add docstrings to public functions and classes.
- Do not add external dependencies without discussing them in an issue first.
- Update the README or documentation when project behavior changes.
- Preserve compatibility with existing functionality unless the change is explicitly breaking.

When appropriate, use formatting, linting, and type-checking tools on the modified code. The project must continue to pass all existing tests.

## Pull Requests

All changes must be submitted through a pull request targeting the `main` branch.

A pull request should:

- Have a clear title.
- Explain what was changed and why.
- Reference the related issue, for example `Closes #12`.
- Include the tests that were performed.
- Update the documentation when necessary.
- Contain one coherent change and avoid unrelated modifications.

Suggested pull request description:

```markdown
## Summary
Briefly describe the change.

## Related Issue
Closes #12

## Testing
- [ ] `make test`
- [ ] Manual testing completed
- [ ] Documentation updated, if applicable

## Notes
Mention limitations, decisions, or possible impacts.
```

### Review and Approval

Code review is the process of examining a pull request before it is merged into `main`. The review may cover:

- Correctness of the implementation.
- Code quality and readability.
- Sufficient and relevant tests.
- Compatibility with Python 3.12+.
- Avoidance of unnecessary changes.
- Documentation updates.

Because the project is currently maintained by one person, there is no fixed minimum number of reviewers. The maintainer may review and approve a pull request alone. If the project gains more collaborators, this policy may be changed to require approval from another contributor before merging.

Do not merge a pull request while important changes remain unresolved or tests are failing.

## Commits

Use **Conventional Commits** for commit messages:

```text
<type>(<scope>): <description>
```

Recommended types:

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `test`: tests
- `refactor`: internal change without a behavior change
- `chore`: maintenance or configuration
- `perf`: performance improvement

Examples:

```text
feat(shapes): add pentagon drawing support
fix(cli): handle quoted command arguments
docs: update installation instructions
test(parser): cover compound commands
```

Write commit messages in the imperative mood, keeping them short and specific. Avoid messages such as `update`, `changes`, or `fix stuff`.

## Dependencies

Dependencies should only be added when necessary. Every new dependency must:

- Be justified in the pull request.
- Be added to `requirements.txt`.
- Support Python 3.12+.
- Be documented in the README when it affects installation or usage.

## Architectural Changes

For significant changes to the architecture or overall project behavior:

1. Open an issue to discuss the proposal.
2. Explain the alternatives that were considered.
3. Update or create an Architecture Decision Record in `docs/adr/`, when applicable.
4. Update the relevant documentation.

## Security Reports

Do not publish sensitive information, credentials, or details about a security vulnerability in a public issue. Report it privately instead, from the repository's **Security** tab with **Report a vulnerability** ([direct link](https://github.com/JoaoTomas991/ascii-art-generator/security/advisories/new)).

## License

Contributions will be distributed under the same license selected for the project. The project is licensed under the MIT License; see [`LICENSE`](LICENSE) for details.

Thank you for contributing to ASCII Art Generator!