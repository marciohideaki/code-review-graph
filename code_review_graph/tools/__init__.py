"""MCP tool implementations for the Code Review Graph server.

Exposes 30 FastMCP tool entry points:
1. build_or_update_graph_tool - full or incremental build
2. run_postprocess_tool - recompute signatures, flows, communities, and FTS
3. get_minimal_context_tool - compact task context
4. get_impact_radius_tool - blast radius from changed files
5. query_graph_tool - predefined graph queries
6. get_review_context_tool - focused subgraph and review prompt
7. semantic_search_nodes_tool - keyword and vector search across nodes
8. list_graph_stats_tool - aggregate statistics
9. embed_graph_tool - compute vector embeddings for semantic search
10. get_docs_section_tool - token-optimised documentation retrieval
11. find_large_functions_tool - find oversized functions/classes by line count
12. list_flows_tool - list execution flows sorted by criticality
13. get_flow_tool - get details of a single execution flow
14. get_affected_flows_tool - find flows affected by changed files
15. list_communities_tool - list detected code communities
16. get_community_tool - get details of a single community
17. get_architecture_overview_tool - architecture overview from community structure
18. detect_changes_tool - risk-scored change impact analysis for code review
19. refactor_tool - unified refactoring (rename preview, dead code, suggestions)
20. apply_refactor_tool - apply a previously previewed refactoring
21. generate_wiki_tool - generate Markdown wiki from community structure
22. get_wiki_page_tool - retrieve a specific wiki page
23. list_repos_tool - list registered repositories
24. cross_repo_search_tool - search across all registered repositories
25. get_hub_nodes_tool - find most connected nodes
26. get_bridge_nodes_tool - find architectural chokepoints
27. get_knowledge_gaps_tool - identify structural weaknesses
28. get_surprising_connections_tool - find unexpected architectural coupling
29. get_suggested_questions_tool - auto-generated review questions from graph analysis
30. traverse_graph_tool - BFS/DFS traversal from best-matching node
"""

from __future__ import annotations

# Re-export names that external code may patch via "code_review_graph.tools.*"
from ..changes import parse_diff_ranges as parse_diff_ranges
from ..changes import parse_git_diff_ranges as parse_git_diff_ranges
from ..changes import parse_svn_diff_ranges as parse_svn_diff_ranges
from ..incremental import (
    get_changed_files as get_changed_files,
)
from ..incremental import (
    get_staged_and_unstaged as get_staged_and_unstaged,
)

# -- _common ----------------------------------------------------------------
from ._common import (
    _BUILTIN_CALL_NAMES,
    _get_store,
    _validate_repo_root,
)

# -- analysis_tools ---------------------------------------------------------
from .analysis_tools import (
    get_bridge_nodes_func,
    get_hub_nodes_func,
    get_knowledge_gaps_func,
    get_suggested_questions_func,
    get_surprising_connections_func,
)

# -- build ------------------------------------------------------------------
from .build import build_or_update_graph, run_postprocess

# -- community_tools --------------------------------------------------------
from .community_tools import (
    get_architecture_overview_func,
    get_community_func,
    list_communities_func,
)

# -- context ----------------------------------------------------------------
from .context import get_minimal_context

# -- docs -------------------------------------------------------------------
from .docs import embed_graph, generate_wiki_func, get_docs_section, get_wiki_page_func

# -- flows_tools ------------------------------------------------------------
from .flows_tools import get_flow, list_flows

# -- query ------------------------------------------------------------------
from .query import (
    find_large_functions,
    get_impact_radius,
    list_graph_stats,
    query_graph,
    semantic_search_nodes,
    traverse_graph_func,
)

# -- refactor_tools ---------------------------------------------------------
from .refactor_tools import apply_refactor_func, refactor_func

# -- registry_tools ---------------------------------------------------------
from .registry_tools import cross_repo_search_func, list_repos_func

# -- review -----------------------------------------------------------------
from .review import (
    detect_changes_func,
    get_affected_flows_func,
    get_review_context,
)

__all__ = [
    # _common
    "_BUILTIN_CALL_NAMES",
    "_get_store",
    "_validate_repo_root",
    # build
    "build_or_update_graph",
    "run_postprocess",
    # context
    "get_minimal_context",
    # community_tools
    "get_architecture_overview_func",
    "get_community_func",
    "list_communities_func",
    # docs
    "embed_graph",
    "generate_wiki_func",
    "get_docs_section",
    "get_wiki_page_func",
    # flows_tools
    "get_flow",
    "list_flows",
    # query
    "find_large_functions",
    "get_impact_radius",
    "list_graph_stats",
    "query_graph",
    "semantic_search_nodes",
    "traverse_graph_func",
    # refactor_tools
    "apply_refactor_func",
    "refactor_func",
    # registry_tools
    "cross_repo_search_func",
    "list_repos_func",
    # review
    "detect_changes_func",
    "get_affected_flows_func",
    "get_review_context",
    # analysis_tools
    "get_bridge_nodes_func",
    "get_hub_nodes_func",
    "get_knowledge_gaps_func",
    "get_suggested_questions_func",
    "get_surprising_connections_func",
    # re-exported for backward compat (used in test patches)
    "get_changed_files",
    "get_staged_and_unstaged",
    "parse_git_diff_ranges",
    "parse_svn_diff_ranges",
    "parse_diff_ranges",
]
