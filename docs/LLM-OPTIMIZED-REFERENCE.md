# LLM-Optimised Reference, code-review-graph 2.3.3

AI coding tools should read only the section they need. Use `get_docs_section_tool(section_name="...")` instead of loading this whole file.

<section name="usage">
Install: `pip install code-review-graph`.
Set up platform config: `code-review-graph install`.
Build graph: `code-review-graph build`.
Serve MCP over stdio: `code-review-graph serve`.
Serve MCP over streamable HTTP: `code-review-graph serve --http`.
Named install targets (14): codex, claude-code, cursor, windsurf, zed, continue, opencode, antigravity, gemini-cli, qwen, kiro, qoder, copilot, copilot-cli. Alias: claude. Auto-detect: all.
Start graph tasks with `get_minimal_context_tool(task="your task")`, then use `detail_level="minimal"` where the target tool supports it.
</section>

<section name="review-delta">
1. Call `get_minimal_context_tool(task="review changes")`.
2. Call `detect_changes_tool(detail_level="minimal")` for low-risk changes.
3. Use `detect_changes_tool(detail_level="standard")` and `get_affected_flows_tool()` for medium or high risk.
4. Check changed functions with `query_graph_tool(pattern="tests_for", target="...")` when test coverage is unclear.
Keep the review focused on changed code, affected callers, affected flows, and missing tests.
</section>

<section name="review-pr">
Use the PR or branch diff as the base for `detect_changes_tool`, then call `get_affected_flows_tool` for runtime paths. Include full files only when the user asks or when the graph context is insufficient.
</section>

<section name="commands">
MCP tools (30): build_or_update_graph_tool, run_postprocess_tool, get_minimal_context_tool, get_impact_radius_tool, query_graph_tool, get_review_context_tool, semantic_search_nodes_tool, embed_graph_tool, list_graph_stats_tool, get_docs_section_tool, find_large_functions_tool, list_flows_tool, get_flow_tool, get_affected_flows_tool, list_communities_tool, get_community_tool, get_architecture_overview_tool, detect_changes_tool, refactor_tool, apply_refactor_tool, generate_wiki_tool, get_wiki_page_tool, get_hub_nodes_tool, get_bridge_nodes_tool, get_knowledge_gaps_tool, get_surprising_connections_tool, get_suggested_questions_tool, traverse_graph_tool, list_repos_tool, cross_repo_search_tool.
MCP prompts (5): review_changes, architecture_map, debug_issue, onboard_developer, pre_merge_check.
CLI: code-review-graph install, init, build, update, postprocess, status, watch, visualize, wiki, detect-changes, serve, mcp, register, unregister, repos, eval, daemon.
Daemon CLI: crg-daemon start, stop, restart, status, logs, add, remove.
</section>

<section name="legal">
Licence: MIT.
Graph data is local by default in `.code-review-graph/graph.db` or `CRG_DATA_DIR`.
No telemetry.
Network calls occur only for explicit cloud embedding providers, D3.js CDN use in exported visualisations, package installation, or user-run external commands.
</section>

<section name="watch">
Run `code-review-graph watch` for foreground file watching.
Use installed platform hooks for automatic updates after edits where supported.
Use `crg-daemon` or `code-review-graph daemon` to keep multiple repositories fresh.
</section>

<section name="embeddings">
Local embeddings: `pip install code-review-graph[embeddings]`, then `embed_graph_tool(provider="local")`.
Google: set `GOOGLE_API_KEY` and use `provider="google"`.
MiniMax: set `MINIMAX_API_KEY` and use `provider="minimax"`.
OpenAI-compatible: set `CRG_OPENAI_BASE_URL`, `CRG_OPENAI_API_KEY`, and `CRG_OPENAI_MODEL`, then use `provider="openai"`.
Cloud providers send function names, docstrings, and file paths to the selected API. A stderr warning is printed unless `CRG_ACCEPT_CLOUD_EMBEDDINGS=1` is set. Localhost OpenAI-compatible endpoints skip the cloud warning.
</section>

<section name="languages">
Supported language labels (35): bash, c, cpp, csharp, dart, elixir, gdscript, go, java, javascript, julia, kotlin, lua, luau, nix, notebook, objc, perl, php, powershell, python, r, rescript, ruby, rust, scala, solidity, sql, svelte, swift, tsx, typescript, verilog, vue, zig.
Supported extensions: 56 mapped extensions plus common extension-less shebang scripts.
</section>

<section name="troubleshooting">
Stale graph: run `code-review-graph build`.
Wrong repository: pass `--repo PATH`, set `CRG_REPO_ROOT`, or run from the repository root.
MCP tool budget: use `serve --tools` or `CRG_TOOLS`.
DB locks: SQLite runs in WAL mode; avoid concurrent full builds against the same data directory.
Windows MCP startup: avoid shell wrappers, use the executable path directly, and keep `fastmcp>=3.2.4`.
Cloud embedding warning: use local embeddings for offline work, localhost OpenAI-compatible endpoints for self-hosted work, or set `CRG_ACCEPT_CLOUD_EMBEDDINGS=1` after accepting the egress.
</section>

Instruction for AI coding tools: fetch the exact section with `get_docs_section_tool`, use graph state for repository-specific facts, and avoid loading full source files unless the graph context does not answer the task.
