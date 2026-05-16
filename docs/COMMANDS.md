# Commands And MCP Reference

## Platform Skills

The repository ships seven checked-in skill documents in `skills/`: `build-graph`, `review-delta`, `review-pr`, `explore-codebase`, `review-changes`, `debug-issue`, and `refactor-safely`.

The installer also generates four Claude Code skills from `code_review_graph/skills.py`: Explore Codebase, Review Changes, Debug Issue, and Refactor Safely. Gemini CLI receives the same four generated skills under `.gemini/skills/`. Qoder receives the checked-in skill documents under `.qoder/skills/`.

## MCP Tools

`code-review-graph` exposes 30 MCP tools by default.

### Build And Context

| Tool | Key parameters | Use |
|------|----------------|-----|
| `build_or_update_graph_tool` | `full_rebuild`, `repo_root`, `base`, `postprocess`, `recurse_submodules` | Build or incrementally update the graph |
| `run_postprocess_tool` | `flows`, `communities`, `fts`, `repo_root` | Re-run signatures, FTS, flow detection, and community detection |
| `get_minimal_context_tool` | `task`, `changed_files`, `repo_root`, `base` | Return compact task context and suggested next tools |
| `get_docs_section_tool` | `section_name`, `repo_root` | Fetch one section from the LLM reference |

### Query And Search

| Tool | Key parameters | Use |
|------|----------------|-----|
| `get_impact_radius_tool` | `changed_files`, `max_depth`, `repo_root`, `base`, `detail_level` | Show blast radius for changed files |
| `query_graph_tool` | `pattern`, `target`, `repo_root`, `detail_level` | Run callers, callees, imports, tests, inheritance, children, or file summary queries |
| `semantic_search_nodes_tool` | `query`, `kind`, `limit`, `repo_root`, `model`, `provider`, `detail_level` | Search entities by keyword or vector similarity |
| `traverse_graph_tool` | `query`, `mode`, `depth`, `token_budget`, `repo_root` | Traverse from a best-matching node with BFS or DFS |
| `find_large_functions_tool` | `min_lines`, `kind`, `file_path_pattern`, `limit`, `repo_root` | Find large files, classes, functions, or tests |
| `list_graph_stats_tool` | `repo_root` | Show graph totals, language list, and freshness |

### Review, Flows, And Architecture

| Tool | Key parameters | Use |
|------|----------------|-----|
| `get_review_context_tool` | `changed_files`, `max_depth`, `include_source`, `max_lines_per_file`, `repo_root`, `base`, `detail_level` | Return review-focused context for changed files |
| `detect_changes_tool` | `base`, `changed_files`, `include_source`, `max_depth`, `repo_root`, `detail_level` | Produce risk-scored change analysis |
| `list_flows_tool` | `sort_by`, `limit`, `kind`, `detail_level`, `repo_root` | List execution flows |
| `get_flow_tool` | `flow_id`, `flow_name`, `include_source`, `repo_root` | Show a single execution flow |
| `get_affected_flows_tool` | `changed_files`, `base`, `repo_root` | Find flows affected by changed files |
| `list_communities_tool` | `sort_by`, `min_size`, `detail_level`, `repo_root` | List detected communities |
| `get_community_tool` | `community_name`, `community_id`, `include_members`, `repo_root` | Show one community |
| `get_architecture_overview_tool` | `repo_root` | Summarise communities and coupling |

### Analysis, Refactoring, Wiki, And Multi-Repo

| Tool | Key parameters | Use |
|------|----------------|-----|
| `get_hub_nodes_tool` | `top_n`, `repo_root` | Find highly connected nodes |
| `get_bridge_nodes_tool` | `top_n`, `repo_root` | Find architectural chokepoints |
| `get_knowledge_gaps_tool` | `repo_root` | Identify isolated nodes, thin communities, and untested hotspots |
| `get_surprising_connections_tool` | `top_n`, `repo_root` | Score unexpected architectural coupling |
| `get_suggested_questions_tool` | `repo_root` | Generate review questions from graph signals |
| `refactor_tool` | `mode`, `old_name`, `new_name`, `kind`, `file_pattern`, `repo_root` | Preview renames, find dead code, or suggest refactors |
| `apply_refactor_tool` | `refactor_id`, `repo_root`, `dry_run` | Apply or dry-run a previewed refactor |
| `generate_wiki_tool` | `repo_root`, `force` | Generate markdown wiki pages |
| `get_wiki_page_tool` | `community_name`, `repo_root` | Read one generated wiki page |
| `list_repos_tool` | none | List registered repositories |
| `cross_repo_search_tool` | `query`, `kind`, `limit` | Search all registered repositories |
| `embed_graph_tool` | `repo_root`, `model`, `provider` | Compute embeddings for semantic search |

Embedding providers are `local`, `google`, `minimax`, and `openai`. The local provider needs `code-review-graph[embeddings]`. Google needs `GOOGLE_API_KEY`; MiniMax needs `MINIMAX_API_KEY`; OpenAI-compatible providers need `CRG_OPENAI_BASE_URL`, `CRG_OPENAI_API_KEY`, and `CRG_OPENAI_MODEL`.

## MCP Prompts

| Prompt | Use |
|--------|-----|
| `review_changes` | Pre-commit review workflow using change analysis, affected flows, and test gaps |
| `architecture_map` | Architecture documentation using communities, flows, and Mermaid diagrams |
| `debug_issue` | Guided debugging using search, flow tracing, and recent changes |
| `onboard_developer` | New developer orientation using stats, architecture, and critical flows |
| `pre_merge_check` | PR readiness check with risk scoring, test gaps, and dead code detection |

## CLI Commands

```bash
code-review-graph install [--platform NAME] [--dry-run] [--no-skills] [--no-hooks] [--no-instructions] [-y]
code-review-graph init [same options as install]

code-review-graph build [--repo PATH] [--skip-flows] [--skip-postprocess] [--data-dir PATH]
code-review-graph update [--base REF] [--repo PATH] [--skip-flows] [--skip-postprocess] [--data-dir PATH]
code-review-graph postprocess [--repo PATH] [--no-flows] [--no-communities] [--no-fts] [--data-dir PATH]

code-review-graph status [--repo PATH] [--data-dir PATH]
code-review-graph watch [--repo PATH] [--data-dir PATH]
code-review-graph detect-changes [--base REF] [--brief] [--repo PATH]

code-review-graph visualize [--repo PATH] [--mode auto|full|community|file] [--serve] [--format html|graphml|cypher|obsidian|svg] [--data-dir PATH]
code-review-graph wiki [--repo PATH] [--force] [--data-dir PATH]

code-review-graph serve [--repo PATH] [--auto-watch] [--tools TOOL,TOOL] [--http] [--host ADDR] [--port PORT]
code-review-graph mcp [--repo PATH] [--auto-watch]

code-review-graph register PATH [--alias NAME]
code-review-graph unregister PATH_OR_ALIAS
code-review-graph repos

code-review-graph eval [--benchmark NAME[,NAME]] [--repo NAME[,NAME]] [--all] [--report] [--output-dir PATH]
```

The 14 named `install --platform` targets are `codex`, `claude-code`, `cursor`, `windsurf`, `zed`, `continue`, `opencode`, `antigravity`, `gemini-cli`, `qwen`, `kiro`, `qoder`, `copilot`, and `copilot-cli`. The CLI also accepts `claude` as an alias for Claude Code and `all` for automatic detection.

The `serve` command uses stdio by default. `serve --http` starts streamable HTTP on `127.0.0.1:5555` unless `--host` or `--port` is supplied.

## Daemon Commands

`crg-daemon` is a standalone entry point for the same multi-repo watcher managed by `code-review-graph daemon`.

```bash
code-review-graph daemon start [--foreground]
code-review-graph daemon stop
code-review-graph daemon restart [--foreground]
code-review-graph daemon status
code-review-graph daemon logs [--repo ALIAS] [--follow] [--lines N]
code-review-graph daemon add PATH [--alias NAME]
code-review-graph daemon remove PATH_OR_ALIAS

crg-daemon start [--foreground]
crg-daemon stop
crg-daemon restart [--foreground]
crg-daemon status
crg-daemon logs [--repo ALIAS] [-f] [-n N]
crg-daemon add PATH [--alias NAME]
crg-daemon remove PATH_OR_ALIAS
```

The daemon reads `~/.code-review-graph/watch.toml`, starts one `code-review-graph watch` child process per repository, watches the config file for changes, and restarts dead watchers during health checks.
