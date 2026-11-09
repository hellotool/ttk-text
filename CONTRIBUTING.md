# Contribution Guidelines

[简体中文](./CONTRIBUTING.zh-CN.md) |
**English** |

First of all, thank you for considering contributing to **Themed Tkinter Text**!

We welcome any form of contribution, whether it's reporting issues, suggesting improvements, fixing bugs, or adding new features.

> [!TIP]
> If you're new to open source contributions, here are some helpful resources:
>
> - GitHub Community’s [Introduction to Open Source][how-to-contribute-github-opensource-guide].
> - Gitee Community’s [Open Source Guide][participating-gitee-opensource-guide].

## Code of Conduct

When participating in this project, please adhere to our [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). We are committed to providing a friendly and inclusive environment for everyone.

## How to Contribute

### Submitting Issues or Suggestions

If you encounter problems during use or have suggestions for improvement, please feel free to submit feedback through any of the following channels:

- [GitHub Issues][issues-github]
- [AtomGit Issues][issues-atomgit]

### Participating in Development

1. Ensure there are no related pull requests (PRs) on the repository.
2. Fork this repository.
3. Clone the repository locally using [Git][git-homepage].
4. Familiarize yourself with the project development approach.
5. Create a branch, such as `feature/xxx` or `bugfix/xxx`.
6. Write your code.
7. Run the following commands to ensure your code meets the standards and introduces no errors:
   ```bash
   uv run ruff check
   uv run ruff format
   uv run pyright
   uv run pytest
   ```
8. Commit your code.
9. Submit a PR to this repository.

## Development

This project is managed using uv. For more information, please refer to the [uv documentation][uv-homepage].

### Setting Up the Environment

Before writing code, you need to set up the development environment:

1. Install [Git][git-homepage] and [uv][uv-homepage].
2. Clone the repository:
   ```bash
   git clone https://github.com/hellotool/ttk-text
   ```
3. Initialize submodules:
   ```bash
   git submodule update --init --recursive
   ```
4. Install dependencies:
   ```bash
   uv sync
   ```

### Running the Example

```bash
uv run example.py
```

## Standards

### Code Standards

You can write code to your heart's content; the `uv run poe fix` command and your IDE will help you check and fix minor issues.

### Git Commit Standards

Follow [Conventional Commits][conventionalcommits-homepage].

[issues-github]: https://github.com/hellotool/ttk-text/issues
[issues-atomgit]: https://atomgit.com/hellotool/ttk-text/issues

[conventionalcommits-homepage]: https://www.conventionalcommits.org/en/v1.0.0/
[uv-homepage]: https://docs.astral.sh/uv/
[git-homepage]: https://git-scm.com/

[how-to-contribute-github-opensource-guide]: https://opensource.guide/how-to-contribute/
[participating-gitee-opensource-guide]: https://gitee.com/opensource-guide/guide/participating/roles.html
