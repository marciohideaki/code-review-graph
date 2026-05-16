# CLAUDE.md - Project Context for Claude Code

## Project Overview

`code-review-graph` is a persistent, incrementally updated knowledge graph for token-efficient code review across AI coding tools. Claude Code is one supported client. The project also supports Codex, Cursor, Windsurf, Zed, Continue, OpenCode, Antigravity, Gemini CLI, Qwen Code, Kiro, Qoder, GitHub Copilot, and GitHub Copilot CLI.

The tool parses repositories with Tree-sitter, stores structural relationships in SQLite, and exposes 30 MCP tools plus 5 MCP prompts for review, search, architecture analysis, refactoring, wiki generation, and multi-repo work.

## Graph Tool Usage (Token-Efficient)
When using code-review-graph MCP tools, follow these rules:
1. First call: `get_minimal_context_tool(task="<description>")` for compact task context.
2. All subsequent calls: use `detail_level="minimal"` unless you need more.
3. Prefer `query_graph_tool` with a specific target over broad `list_*` calls.
4. The `next_tool_suggestions` field in every response tells you the optimal next step.
5. Target: ≤5 tool calls per task, ≤800 total tokens of graph context.

## Architecture

- **Core Package**: `code_review_graph/` (Python 3.10+)
  - `parser.py`: Tree-sitter parser for 35 language labels across 56 extensions, notebooks, and shebang-detected scripts
  - `graph.py`: SQLite graph store with nodes, edges, confidence scoring, metadata, and impact queries
  - `main.py`: FastMCP entry point, stdio and streamable HTTP transport, 30 tools and 5 prompts
  - `tools/`: grouped MCP tool implementation modules
  - `incremental.py`: git/SVN change detection, file watching, hashing, and post-build resolver passes
  - `embeddings.py`: local, Google Gemini, MiniMax, and OpenAI-compatible embeddings
  - `visualization.py`: D3.js interactive HTML visualisation generator
  - `cli.py`: CLI entry point for install, build, update, postprocess, watch, status, visualise, serve, wiki, detect-changes, registry, daemon, and eval
  - `daemon.py` and `daemon_cli.py`: multi-repo watcher supervision
  - `flows.py`: execution flow detection and criticality scoring
  - `communities.py`: Leiden or file-based community detection and architecture overview
  - `search.py`: FTS5 and vector hybrid search
  - `changes.py`: risk-scored change impact analysis
  - `refactor.py`: rename preview, dry-run/apply support, dead code detection, and refactoring suggestions
  - `hints.py`: review hint generation
  - `prompts.py`: 5 MCP prompt templates
  - `wiki.py`: markdown wiki generation from community structure
  - `skills.py`: platform config, hooks, instruction snippets, and generated skills
  - `registry.py`: multi-repo registry with connection pool
  - `migrations.py`: database migrations through schema v9
  - `tsconfig_resolver.py`: TypeScript path alias resolution

- **VS Code Extension**: `code-review-graph-vscode/` (TypeScript)
  - Separate subproject with its own `package.json`, `tsconfig.json`
  - Reads from `.code-review-graph/graph.db` via SQLite

- **Database**: `.code-review-graph/graph.db` or `CRG_DATA_DIR` (SQLite, WAL mode)

## Key Commands

```bash
# Development
uv run pytest tests/ --tb=short -q          # Run tests
uv run ruff check code_review_graph/        # Lint
uv run mypy code_review_graph/ --ignore-missing-imports --no-strict-optional

# Build & test
uv run code-review-graph build              # Full graph build
uv run code-review-graph update             # Incremental update
uv run code-review-graph status             # Show stats
uv run code-review-graph serve              # Start MCP server over stdio
uv run code-review-graph serve --http       # Start streamable HTTP on localhost
uv run code-review-graph wiki               # Generate markdown wiki
uv run code-review-graph detect-changes     # Risk-scored change analysis
uv run code-review-graph register <path>    # Register repo in multi-repo registry
uv run code-review-graph repos              # List registered repos
uv run code-review-graph eval               # Run evaluation benchmarks
uv run crg-daemon status                    # Show multi-repo daemon status
```

## Code Conventions

- **Line length**: 100 chars (ruff)
- **Python target**: 3.10+
- **SQL**: Always use parameterized queries (`?` placeholders), never f-string values
- **Error handling**: Catch specific exceptions, log with `logger.warning/error`
- **Thread safety**: `threading.Lock` for shared caches, `check_same_thread=False` for SQLite
- **Node names**: Always sanitize via `_sanitize_name()` before returning to MCP clients
- **File reads**: Read bytes once, hash, then parse (TOCTOU-safe pattern)

## Security Invariants

- No `eval()`, `exec()`, `pickle`, or `yaml.unsafe_load()`
- No `shell=True` in subprocess calls
- `_validate_repo_root()` prevents path traversal via repo_root parameter
- `_sanitize_name()` strips control characters, caps at 256 chars (prompt injection defense)
- `escH()` in visualisation escapes HTML entities including quotes and backticks
- SRI hash on D3.js CDN script tag
- API keys only from environment variables, never hardcoded
- Cloud embeddings warn on stderr before source-code metadata leaves the machine

## Test Structure

- Parser and language coverage: parser, multilang, fixtures, notebooks, framework resolvers, and TypeScript path resolution.
- Storage and update behaviour: graph, migrations, transactions, FTS sync, incremental updates, daemon, registry, and post-processing.
- MCP and workflows: tools, prompts, hints, review context, change analysis, refactoring, wiki, search, flows, communities, and evaluation.
- VS Code and visual output: visualisation, exports, and extension-side SQLite tests.

## CI Pipeline

- **lint**: ruff on Python 3.10
- **type-check**: mypy
- **security**: bandit scan
- **test**: pytest matrix (3.10, 3.11, 3.12, 3.13) with 50% coverage minimum


<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:ca08a54f -->
## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

## Session Completion

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd dolt push
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
<!-- END BEADS INTEGRATION -->

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes_tool` or `query_graph_tool` instead of Grep
- **Understanding impact**: `get_impact_radius_tool` instead of manually tracing imports
- **Code review**: `detect_changes_tool` + `get_review_context_tool` instead of reading entire files
- **Finding relationships**: `query_graph_tool` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview_tool` + `list_communities_tool`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
|------|----------|
| `detect_changes_tool` | Reviewing code changes; gives risk-scored analysis |
| `get_review_context_tool` | Need source snippets for review; token-efficient |
| `get_impact_radius_tool` | Understanding blast radius of a change |
| `get_affected_flows_tool` | Finding which execution paths are impacted |
| `query_graph_tool` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes_tool` | Finding functions/classes by name or keyword |
| `get_architecture_overview_tool` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes_tool` for code review.
3. Use `get_affected_flows_tool` to understand impact.
4. Use `query_graph_tool` pattern="tests_for" to check coverage.
