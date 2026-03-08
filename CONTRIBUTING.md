# Contributing

Before contributing, please adhere to the [Code of Conduct](CODE_OF_CONDUCT.md), platform policies, and relevant laws and regulations.

## Submit Issues

If you encounter problems during use or have suggestions for improvement, please feel free to submit feedback through any of the following channels:

- [GitHub Issues][issues-github]
- [GitCode Issues][issues-gitcode]

## Pull Requests

1. Ensure there are no related PRs.
2. Fork this repository.
3. Clone the repository locally using [Git](https://git-scm.com/).
4. Familiarize yourself with the project development methods.
5. Create a branch, such as `feature/xxx` or `bugfix/xxx`.
6. Write and commit your code.
7. Submit a Pull Request to this repository.

## Development

This project is managed using uv. For more information about uv, please refer to the [uv documentation][uv-docs].

### Setting Up the Environment

Before writing code, you need to set up the development environment.

1. Install Git and uv.
2. Clone the repository locally by running `git clone https://github.com/hellotool/ttk-text`.
3. Initialize submodules by running `git submodule update --init --recursive`.
4. Install dependencies by running `uv sync`.

### Running the Example

```bash
uv run example.py
```

## Standards

### Code Standards

**Python (`.py`):**

- Function parameters must include type annotations.
- Maximum line length: 120 characters.
- All other cases should follow [PEP 8](https://peps.python.org/pep-0008/).

### Git Commit Standards

Follow [Conventional Commits][conventional-commits].

[issues-github]: https://github.com/hellotool/ttk-text/issues
[issues-gitcode]: https://gitcode.com/hellotool/ttk-text/issues

[conventional-commits]: https://www.conventionalcommits.org/
[uv-docs]: https://docs.astral.sh/uv/
