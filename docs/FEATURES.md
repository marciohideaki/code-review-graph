# Features

## v2.3.3 (Current)

- **30 MCP tools** and **5 MCP prompts** for build, search, review, graph analysis, refactoring, wiki generation, and multi-repo search.
- **14 install targets**: Codex, Claude Code, Cursor, Windsurf, Zed, Continue, OpenCode, Antigravity, Gemini CLI, Qwen Code, Kiro, Qoder, GitHub Copilot, and GitHub Copilot CLI.
- **35 language labels across 56 extensions**, including Elixir, Objective-C, Bash, GDScript, Verilog/SystemVerilog, SQL, ReScript, Nix, Svelte, Julia, PowerShell, Zig, notebooks, and shebang-detected scripts.
- **Streamable HTTP transport** alongside stdio via `code-review-graph serve --http`.
- **Graph analysis suite**: hubs, bridge nodes, knowledge gaps, surprising connections, suggested questions, and free-form traversal.
- **Edge confidence and richer edge kinds**: `REFERENCES`, `INJECTS`, `TEMPORAL_STUB`, `CONSUMES`, and `PRODUCES`.
- **OpenAI-compatible embeddings** alongside local, Google Gemini, and MiniMax providers, with explicit cloud egress warnings.
- **Multi-repo daemon** via `crg-daemon` and `code-review-graph daemon`.
- **Export formats**: GraphML, Neo4j Cypher, Obsidian vault, SVG, and interactive HTML.
- **1,236 tests passing** in the current local verification run.

Older release history lives in `CHANGELOG.md`; this page tracks the current feature set.

## Privacy & Data
- All data stays 100% local
- Graph stored in `.code-review-graph/graph.db` (SQLite), auto-gitignored
- No telemetry
- Network calls occur only for explicit cloud embeddings, local model downloads, package installation, or visualisations that load D3.js from its CDN
- Respects `.gitignore` and `.code-review-graphignore`
