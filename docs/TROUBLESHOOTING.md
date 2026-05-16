# Troubleshooting

## Quick reference for common install/setup problems

Four issues account for most support questions. Check these first:

### 1. `Hooks use a matcher + hooks array` error in `.claude/settings.json`

**You're on a pre-2.2.3 release.** Releases 2.2.1 and 2.2.2 shipped a broken hook schema: flat `{matcher, command, timeout}` entries without the required nested `hooks: []` array, timeouts in milliseconds instead of seconds, and a `PreCommit` event that is not a real Claude Code event. PR #208, shipped in 2.2.3, rewrote the generator to emit the correct v1.x+ schema.

**Fix:**

```bash
pip install --upgrade code-review-graph   # v2.3.3 or later
cd /path/to/your/project
code-review-graph install                 # rewrites .claude/settings.json
```

The reinstall merges the new nested format over the broken `hooks` block and adds a real git pre-commit hook in `.git/hooks/pre-commit`. Commit checks live there in v2.2.3 and later, not in Claude Code settings.

Valid Claude Code hook events are: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `PreCompact`, `Notification`. There is no `PreCommit`.

### 2. `code-review-graph: command not found` after `pip install`

`pip install` put the console script into a `bin/` directory that isn't on your `$PATH`. Four fixes, in order of recommendation:

**Option 1: Use `pipx` (cleanest):**

```bash
pip uninstall code-review-graph
pipx install code-review-graph
```

`pipx` installs CLI tools in an isolated venv and guarantees `~/.local/bin` is on PATH.

**Option 2: Use `uvx` (no install needed):**

```bash
uvx code-review-graph install
uvx code-review-graph build
```

**Option 3: Run it as a Python module (always works):**

```bash
python -m code_review_graph install
python -m code_review_graph build
```

**Option 4: Fix PATH manually:**

```bash
pip show code-review-graph | grep Location
# Find the sibling `bin/` directory; on macOS user installs this is
# typically ~/Library/Python/3.X/bin. Add it to your shell rc:
echo 'export PATH="$HOME/Library/Python/3.12/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 3. Is code-review-graph project-scoped or user-scoped?

**Both.** Different pieces have different scopes:

| Piece                         | Scope          | Where                                                            |
|-------------------------------|----------------|------------------------------------------------------------------|
| The Python package            | User-scoped    | Install once via `pip`/`pipx`/`uvx`                              |
| The graph database            | Project-scoped | `.code-review-graph/graph.db` inside each project                |
| MCP server config | Platform-specific | Some clients use project files such as `.mcp.json`, `.cursor/mcp.json`, `.vscode/mcp.json`, `.gemini/settings.json`, `.kiro/settings/mcp.json`, `.qoder/mcp.json`, or `.opencode.json`; others use user-level config |
| Multi-repo registry           | User-scoped    | `~/.code-review-graph/registry.json` (only for `cross_repo_search`) |

Install the tool once, then run `code-review-graph install && code-review-graph build` inside each project where you want graph-aware reviews.

### 4. Using a venv? Reinstall or update generated config

Platform hooks and MCP tool paths are written at install time. If you switch to, or create, a virtual environment after running `code-review-graph install`, generated config may still point to the old interpreter.

Fix it by updating the generated config to match your venv:

```json
// Example .mcp.json: point to your venv's Python or uvx inside the venv
{
  "mcpServers": {
    "code-review-graph": {
      "command": "/path/to/your/venv/bin/uvx",
      "args": ["code-review-graph", "serve"]
    }
  }
}
```

Or simply re-run `code-review-graph install` **from within the activated venv** so the paths are regenerated correctly:

```bash
source .venv/bin/activate          # activate your venv first
code-review-graph install          # rewrites .mcp.json and hook paths
```

Then fully quit and reopen your AI coding tool so it picks up the new config.

### 5. "I built the graph but my AI tool doesn't see it in a new session"

Most likely causes, ranked:

1. **You didn't restart the client after `install`.** Most MCP clients read config at startup.
2. **The new session's `cwd` is a different directory.** The MCP server reads `.code-review-graph/graph.db` from the configured project root. If the session opens in a parent folder or a different project, it will not find the graph you built.
3. **You ran `build` but not `install`.** `build` creates `graph.db`; `install` registers the MCP server with the selected client.
4. **The MCP server is crashing on startup.** Check your client's MCP status command or its MCP logs.

**Quick checklist:**

```bash
cd /path/to/your/project
code-review-graph status    # should print Files/Nodes/Edges from the built graph
ls .mcp.json                # should exist
cat .mcp.json               # should reference `code-review-graph serve`
# then: fully quit your AI coding tool and reopen it inside this project
```

If `status` shows the graph but the client does not list `code-review-graph`, re-run `code-review-graph install` from the correct project root and restart the client.

## Database lock errors
The graph uses SQLite with WAL mode. If you see lock errors:
- Ensure only one build process runs at a time
- The database auto-recovers; just retry
- Delete `.code-review-graph/graph.db-wal` and `.code-review-graph/graph.db-shm` if corrupt

## Large repositories (>10k files)
- First build may take 30-60 seconds
- Subsequent incremental updates are fast (<2s)
- Add more ignore patterns to `.code-review-graphignore`:
  ```
  generated/**
  vendor/**
  *.min.js
  ```

## Missing nodes after build
- Check that the file's language is supported (see [FEATURES.md](FEATURES.md))
- Check that the file isn't matched by an ignore pattern
- Run with `full_rebuild=True` to force a complete re-parse

## Graph seems stale
- Hooks auto-update on edit/commit
- If stale, run `/code-review-graph:build-graph` manually
- Check that platform hooks are configured, or re-run `code-review-graph install` to regenerate them

## Embeddings not working
- Install with: `pip install code-review-graph[embeddings]`
- Run `embed_graph_tool` to compute vectors
- First embedding run downloads the model (~90MB, one time)
- For cloud providers, set the provider-specific environment variables and accept the source-code egress warning, or set `CRG_ACCEPT_CLOUD_EMBEDDINGS=1`

## MCP server won't start
- Verify `uv` is installed (`uv --version`; install with `pip install uv` or `brew install uv`)
- Check that `uvx code-review-graph serve` runs without errors
- If using a custom MCP config, ensure it launches `code-review-graph serve` or `uvx code-review-graph serve`
- Re-run `code-review-graph install` to regenerate the config

## Windows / WSL

- Use forward slashes in paths when passing `repo_root` to MCP tools
- In WSL, ensure `uv` is installed inside WSL (not the Windows version): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- If `uv` is not found after install, add `~/.cargo/bin` to your PATH
- File watching (`code-review-graph watch`) may have delays on WSL1 due to filesystem event limitations; WSL2 is recommended
- On Windows native (non-WSL), long path support may need to be enabled: `git config --system core.longpaths true`

## Community detection requires igraph

- Install with: `pip install code-review-graph[communities]`
- Without igraph, community detection falls back to file-based grouping (less precise but functional)

## Wiki generation with LLM summaries

- Install with: `pip install code-review-graph[wiki]`
- Requires a running Ollama instance for LLM-powered summaries
- Without Ollama, wiki pages are generated with structural information only (no prose summaries)

## Optional dependency groups

If a tool returns an ImportError, install the relevant optional group:
- `pip install code-review-graph[embeddings]` for semantic search
- `pip install code-review-graph[google-embeddings]` for Google Gemini embeddings
- Set `MINIMAX_API_KEY` for MiniMax embeddings
- Set `CRG_OPENAI_BASE_URL`, `CRG_OPENAI_API_KEY`, and `CRG_OPENAI_MODEL` for OpenAI-compatible embeddings
- `pip install code-review-graph[communities]` for igraph-based community detection
- `pip install code-review-graph[eval]` for evaluation benchmarks (matplotlib)
- `pip install code-review-graph[wiki]` for wiki LLM summaries (ollama)
- `pip install code-review-graph[enrichment]` for Jedi-powered Python call resolution
- `pip install code-review-graph[all]` for everything
