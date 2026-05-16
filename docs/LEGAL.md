# Legal & Privacy

**Licence:** MIT (see [LICENSE](../LICENSE) in project root)

**Privacy:**
- Zero telemetry
- All graph data stored locally in `.code-review-graph/graph.db`
- No network calls during normal graph build, update, query, or review work; optional cloud embeddings are the explicit exception
- Optional local embeddings model downloaded once from HuggingFace when using the `[embeddings]` extra
- Optional cloud embeddings send function names, docstrings, and file paths to the selected external API only when explicitly configured

**Data:** Stays local unless you opt into a cloud embedding provider, run package installation, or open/export visualisations that load D3.js from its CDN.

**Warranty:** Provided as-is, without warranty of any kind.
