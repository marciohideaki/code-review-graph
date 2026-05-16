# Code Review Graph User Guide

Version: 2.3.3

## Installation

```bash
pip install code-review-graph
code-review-graph install
code-review-graph build
```

`install` detects supported AI coding tools, writes MCP configuration, installs native hooks or skills where the platform supports them, and adds graph-aware instructions to platform rule files. Restart your editor or coding tool after installing.

To target one platform:

```bash
code-review-graph install --platform codex
code-review-graph install --platform claude-code
code-review-graph install --platform cursor
code-review-graph install --platform windsurf
code-review-graph install --platform zed
code-review-graph install --platform continue
code-review-graph install --platform opencode
code-review-graph install --platform antigravity
code-review-graph install --platform gemini-cli
code-review-graph install --platform qwen
code-review-graph install --platform kiro
code-review-graph install --platform qoder
code-review-graph install --platform copilot
code-review-graph install --platform copilot-cli
```

## Supported Platforms

| Platform | Target | Config file |
|----------|--------|-------------|
| Codex | `codex` | `~/.codex/config.toml` |
| Claude Code | `claude-code` or `claude` | `.mcp.json` |
| Cursor | `cursor` | `.cursor/mcp.json` |
| Windsurf | `windsurf` | `~/.codeium/windsurf/mcp_config.json` |
| Zed | `zed` | platform Zed `settings.json` |
| Continue | `continue` | `~/.continue/config.json` |
| OpenCode | `opencode` | `.opencode.json` |
| Antigravity | `antigravity` | `~/.gemini/antigravity/mcp_config.json` |
| Gemini CLI | `gemini-cli` | `.gemini/settings.json` |
| Qwen Code | `qwen` | `~/.qwen/settings.json` |
| Kiro | `kiro` | `.kiro/settings/mcp.json` |
| Qoder | `qoder` | `.qoder/mcp.json` |
| GitHub Copilot | `copilot` | `.vscode/mcp.json` |
| GitHub Copilot CLI | `copilot-cli` | `~/.copilot/mcp-config.json` |

Some platforms also receive native automation: Codex hooks, Claude Code hooks and generated skills, Gemini CLI hooks and skills, Cursor hooks, Qoder skills and hooks, OpenCode plugin support, and a git pre-commit hook where a git repository is available.

## Core Workflow

Build the graph once:

```bash
code-review-graph build
```

After that, run incremental updates manually with `code-review-graph update`, keep a foreground watcher running with `code-review-graph watch`, or use installed platform hooks. The multi-repo daemon can supervise watchers for several repositories:

```bash
crg-daemon add ~/project-a --alias project-a
crg-daemon start
crg-daemon status
```

For MCP clients, run the server over stdio by default or streamable HTTP on localhost:

```bash
code-review-graph serve
code-review-graph serve --http
```

`serve --tools` and `CRG_TOOLS` can restrict the 30 exposed MCP tools to a comma-separated allow-list.

## Common Tasks

Use `detect_changes_tool` for risk-scored review of recent changes. It maps diffs to affected functions, flows, communities, and test gaps.

Use `get_architecture_overview_tool` for a community-based architecture map with coupling warnings.

Use `semantic_search_nodes_tool` for keyword or vector-backed search. Run `embed_graph_tool` first if you want vector similarity.

Use `cross_repo_search_tool` after registering other repositories:

```bash
code-review-graph register /path/to/other/repo --alias mylib
```

Generate a markdown wiki from detected communities:

```bash
code-review-graph wiki
```

Generate an interactive visualisation or export the graph:

```bash
code-review-graph visualize
code-review-graph visualize --format graphml
code-review-graph visualize --format cypher
code-review-graph visualize --format obsidian
code-review-graph visualize --format svg
```

## Supported Languages

The parser supports 35 language labels across 56 extensions: Bash, C, C++, C#, Dart, Elixir, GDScript, Go, Java, JavaScript, Julia, Kotlin, Lua, Luau, Nix, notebooks, Objective-C, Perl, PHP, PowerShell, Python, R, ReScript, Ruby, Rust, Scala, Solidity, SQL, Svelte, Swift, TSX, TypeScript, Verilog/SystemVerilog, Vue, and Zig.

Notebook support covers Jupyter and Databricks `.ipynb` files, including Python, R, SQL, and Scala cells. Extension-less scripts are detected through common shebang interpreters.

## What Gets Indexed

Nodes represent files, classes, functions, types, and tests.

Edges represent `CALLS`, `IMPORTS_FROM`, `INHERITS`, `IMPLEMENTS`, `CONTAINS`, `TESTED_BY`, `DEPENDS_ON`, `REFERENCES`, `INJECTS`, `TEMPORAL_STUB`, `CONSUMES`, and `PRODUCES`.

See [schema.md](schema.md) for table details.

## Embeddings And Network Use

Local embeddings use `sentence-transformers`:

```bash
pip install "code-review-graph[embeddings]"
```

Cloud providers are opt-in. Google Gemini requires `GOOGLE_API_KEY`; MiniMax requires `MINIMAX_API_KEY`; OpenAI-compatible providers require `CRG_OPENAI_BASE_URL`, `CRG_OPENAI_API_KEY`, and `CRG_OPENAI_MODEL`. Cloud providers send function names, docstrings, and file paths to the selected external API, and print a stderr warning unless `CRG_ACCEPT_CLOUD_EMBEDDINGS=1` is set. Localhost OpenAI-compatible endpoints do not trigger the cloud warning.

## Ignore Patterns

By default, generated files, dependency directories, caches, build output, lockfiles, database files, and VCS metadata are excluded. In git repositories, indexing is based on tracked files from `git ls-files`, so gitignored files are skipped automatically.

To exclude additional tracked files, add `.code-review-graphignore` at the repository root:

```gitignore
generated/**
vendor/**
*.generated.ts
```
