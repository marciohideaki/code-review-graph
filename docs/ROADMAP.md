# Roadmap

## Shipped

### v2.3.3
- 30 MCP tools and 5 MCP prompts
- 14 install targets across Codex, Claude Code, Cursor, Windsurf, Zed, Continue, OpenCode, Antigravity, Gemini CLI, Qwen Code, Kiro, Qoder, GitHub Copilot, and GitHub Copilot CLI
- 35 supported language labels across 56 extensions
- Streamable HTTP MCP transport via `serve --http`
- Graph analysis tools for hubs, bridge nodes, knowledge gaps, surprising connections, suggested questions, and traversal
- Edge confidence scoring and richer edge kinds for references, dependency injection, Temporal stubs, and Kafka topics
- OpenAI-compatible embeddings with endpoint-aware provider identity
- Current schema migrations through v9

### v2.2.0
- Multi-repo watch daemon (`crg-daemon` / `code-review-graph daemon`)
- TOML-based daemon configuration (`~/.code-review-graph/watch.toml`)
- Child process management: one `code-review-graph watch` process per repo
- Config file watching with automatic reconciliation of watcher processes
- Daemonization with PID file management
- Health checking with automatic restart of dead watchers
- Standalone `crg-daemon` CLI entry point (7 subcommands)
- Integrated `daemon` subcommand group in main CLI

### v2.0.0
- Expanded MCP tool coverage and added workflow prompts
- Expanded language support with Dart, R, and Perl
- Execution flow detection with criticality scoring
- Community detection (Leiden algorithm via igraph, file-based fallback)
- Architecture overview with coupling warnings
- Risk-scored change detection (`detect_changes_tool`)
- Refactoring tools (rename preview, dead code, suggestions)
- Wiki generation from community structure
- Multi-repo registry with cross-repo search
- FTS5 full-text search with porter stemming
- Database migrations (v1-v5)
- Evaluation framework with matplotlib visualisation
- TypeScript tsconfig path alias resolution
- MiniMax embedding provider (embo-01)
- Optional dependency groups: `[embeddings]`, `[google-embeddings]`, `[communities]`, `[eval]`, `[wiki]`, `[all]`
- 486 tests across 22 test files

### v1.8.4
- Multi-word AND search, call target resolution, impact radius pagination
- `find_large_functions_tool`, Vue SFC and Solidity support
- Documentation overhaul

### v1.7.0
- `install` command as primary entry point (`init` kept as alias)
- `--dry-run` flag for previewing install/init changes
- Automatic PyPI publishing via GitHub Actions on release
- README rewrite with real benchmark data from httpx, FastAPI, and Next.js

### v1.6.x
- Portable `uvx`-based MCP config
- SessionStart hook for automatic graph tool preference
- 24 audit fixes: C/C++ support, performance, CI hardening

### v1.5.x
- Generated files in `.code-review-graph/` directory
- Visualization density: collapsed start, search, edge toggles
- Works without git

### v1.4.0
- `init` command, interactive D3.js visualisation, `serve` command

### v1.3.0
- Universal pip install, CLI entry point, Python version check

### v1.1.0-v1.2.0
- Watch mode, vector embeddings, logging, CI coverage

### v1.0.0 (Foundation)
- Persistent SQLite knowledge graph, Tree-sitter parsing, incremental updates
- Impact radius analysis, 6 MCP tools, 3 skills

## Planned

- GitHub PR bot integration
- Team sync (shared graph via git-tracked DB)
- Performance optimisation for monorepos (>50k files)

## Ongoing

- Additional language grammars as requested
- Integration with more client-specific hooks, skills, and instruction formats as supported platforms evolve
