# 贡献指南

**简体中文** |
[English](./CONTRIBUTING.md)

首先，感谢您考虑为 **Themed Tkinter Text** 做出贡献！

我们欢迎任何形式的贡献，无论是报告问题、提出建议、修复错误还是添加新功能。

> [!TIP]
> 如果你是开源贡献的新手，这些资源或许能帮到你：
>
> - GitHub 社区的 [开源软件指南][how-to-contribute-github-opensource-guide]。
> - Gitee 社区的 [开源指北][participating-gitee-opensource-guide]。

## 行为准则

参与本项目时，请遵守我们的 [贡献者公约](./CODE_OF_CONDUCT.md)。我们致力于为每个人提供友善、包容的社区环境。

## 如何贡献

### 提交问题或建议

如果您在使用中遇到问题或有改进建议，欢迎通过以下任一渠道提交反馈：

- [GitHub Issues][issues-github]
- [AtomGit Issues][issues-atomgit]

### 参与开发

1. 确保仓库中没有相关的拉取请求（PR）。
2. Fork 本仓库。
3. 使用 [Git][git-homepage] 将仓库克隆到本地。
4. 熟悉项目的开发方法。
5. 创建分支，如 `feature/xxx` 或 `bugfix/xxx`。
6. 编写代码。
7. 运行以下命令，确保代码符合规范且未引入错误：
   ```bash
   uv run ruff check
   uv run ruff format
   uv run pyright
   uv run pytest
   ```
8. 提交代码。
9. 向本仓库提交 PR。

## 开发

本项目使用 uv 进行管理。更多信息请参考 [uv 文档][uv-homepage]。

### 搭建开发环境

编写代码前，需要先搭建开发环境：

1. 安装 [Git][git-homepage] 和 [uv][uv-homepage]。
2. 克隆仓库：
   ```bash
   git clone https://github.com/hellotool/ttk-text
   ```
3. 初始化子模块：
   ```bash
   git submodule update --init --recursive
   ```
4. 安装依赖：
   ```bash
   uv sync
   ```

### 运行示例

```bash
uv run example.py
```

## 规范

### 代码规范

您可以尽情地编写代码，`uv run poe fix` 命令和您的 IDE 会帮助您检查并修复一些小问题。

### Git 提交规范

遵循 [约定式提交][conventionalcommits-homepage]。

[issues-github]: https://github.com/hellotool/ttk-text/issues
[issues-atomgit]: https://atomgit.com/hellotool/ttk-text/issues

[conventionalcommits-homepage]: https://www.conventionalcommits.org/zh-hans/v1.0.0/
[uv-homepage]: https://docs.astral.sh/uv/zh/
[git-homepage]: https://git-scm.com/

[how-to-contribute-github-opensource-guide]: https://opensource.guide/zh-hans/how-to-contribute/
[participating-gitee-opensource-guide]: https://gitee.com/opensource-guide/guide/participating/roles.html
