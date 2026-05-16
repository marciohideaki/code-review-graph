# Architecture

## System Overview

`code-review-graph` is a local MCP server and CLI that maintains an incremental knowledge graph for a repository. It supports multiple AI coding tools, including Codex, Claude Code, Cursor, Windsurf, Zed, Continue, OpenCode, Antigravity, Gemini CLI, Qwen Code, Kiro, Qoder, GitHub Copilot, and GitHub Copilot CLI.

The system parses source files, stores structural relationships in SQLite, and exposes 30 MCP tools plus 5 MCP prompts for code review, search, architecture analysis, refactoring, wiki generation, and multi-repo search.

## Components

```text
AI coding tool
  ├─ MCP config, platform instructions, hooks, or skills
  └─ code-review-graph MCP server
       ├─ stdio transport
       ├─ streamable HTTP transport on localhost
       ├─ parser and incremental engine
       ├─ SQLite graph store
       ├─ post-processing: signatures, FTS, flows, communities, summaries
       ├─ optional embeddings store
       └─ tools for review, query, analysis, refactoring, wiki, and multi-repo search
```

Platform installation is handled by `code_review_graph/skills.py`. It writes MCP configuration and, where supported, installs native hooks, generated skills, Copilot instruction files, Gemini CLI settings, Qoder skills, Cursor hooks, Codex hooks, OpenCode plugin support, and a git pre-commit hook.

## Data Flow

Full builds call `collect_all_files()`, prefer tracked files from git or SVN where available, apply default ignore patterns and `.code-review-graphignore`, then parse each source file with `CodeParser`. Parsed nodes and edges are written through `GraphStore.store_file_nodes_edges()`.

Incremental updates detect changed files through git or SVN, find dependent files through stored import edges, skip unchanged files by SHA-256 hash, and re-run language-specific resolvers where needed. Post-processing refreshes signatures, FTS, execution flows, communities, and summary tables according to the selected `postprocess` mode.

Review tools start from changed files, compute impact radius, affected flows, community context, test coverage signals, and risk scores, then return compact context for the AI client.

## Storage

The primary graph database is SQLite in `.code-review-graph/graph.db`, or in `CRG_DATA_DIR` when configured. WAL mode is enabled for concurrent reads.

Core tables include `nodes`, `edges`, and `metadata`. Migrations add `flows`, `flow_memberships`, `communities`, `nodes_fts`, `community_summaries`, `flow_snapshots`, and `risk_index`. Edge rows include `confidence` and `confidence_tier`.

The embeddings store is separate and records vectors by qualified name, text hash, and provider identity. Provider identity includes the backend for OpenAI-compatible endpoints so vectors from different backends are not mixed.

## Parsing Strategy

Tree-sitter handles most language grammars. The parser maps extensions and shebang interpreters to 35 language labels, then extracts files, classes, functions, types, tests, imports, calls, inheritance, containment, references, framework injection, Temporal stubs, and Kafka consumer or producer topics.

Specialised resolver passes improve cross-file or framework-heavy code. Current resolvers include ReScript cross-module resolution, Spring dependency-injection call resolution, Temporal workflow/activity resolution, TypeScript path aliases, and Jedi-based Python call resolution when enrichment dependencies are installed.

## Transports And Automation

`code-review-graph serve` runs MCP over stdio. `code-review-graph serve --http` runs streamable HTTP on localhost, defaulting to `127.0.0.1:5555`.

Automation is available through platform hooks, `code-review-graph watch`, the git pre-commit hook, and `crg-daemon` for multi-repo watcher supervision.

## Visualisation And Exports

`visualization.py` generates a self-contained D3.js HTML visualisation. The CLI can also export GraphML, Neo4j Cypher, Obsidian vault files, and SVG.
