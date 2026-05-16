# Knowledge Graph Schema

## Node Types

| Kind | Meaning |
|------|---------|
| `File` | Source file with path, language, line range, and file hash |
| `Class` | Class, struct, interface, enum, module, contract, or similar named container |
| `Function` | Function, method, constructor, task, procedure, binding, or equivalent callable |
| `Type` | Type alias, interface, enum, or language-specific type declaration |
| `Test` | Test function or method, stored with `is_test = true` |

Common node fields are `name`, `qualified_name`, `file_path`, `line_start`, `line_end`, `language`, `parent_name`, `params`, `return_type`, `modifiers`, `is_test`, `file_hash`, `extra`, `updated_at`, `signature`, and `community_id`.

Qualified names use absolute file paths for files and `file_path::symbol` for contained symbols, for example `/repo/src/auth.py::AuthService.login`.

## Edge Types

| Kind | Meaning |
|------|---------|
| `CALLS` | A function, method, module scope, or equivalent callable invokes another symbol |
| `IMPORTS_FROM` | A file or symbol imports, opens, sources, includes, or otherwise refers to another module or file |
| `INHERITS` | A class or type extends another class or base type |
| `IMPLEMENTS` | A class or type implements an interface or protocol |
| `CONTAINS` | A file contains a symbol, or a container contains a nested symbol |
| `TESTED_BY` | A production symbol is covered by a test symbol |
| `DEPENDS_ON` | A general dependency when a more specific edge kind is not appropriate |
| `REFERENCES` | A symbol is referenced as a value, such as a callback or dispatch-table entry |
| `INJECTS` | Java Spring dependency injection connects an owner to an injected type |
| `TEMPORAL_STUB` | Java Temporal workflow or activity stub field points to an interface |
| `CONSUMES` | Kafka consumer code consumes from a topic |
| `PRODUCES` | Kafka producer code produces to a topic |

Edges include `confidence` and `confidence_tier`. Confidence tiers are `EXTRACTED`, `INFERRED`, and `AMBIGUOUS`.

## Core SQLite Tables

```sql
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    name TEXT NOT NULL,
    qualified_name TEXT NOT NULL UNIQUE,
    file_path TEXT NOT NULL,
    line_start INTEGER,
    line_end INTEGER,
    language TEXT,
    parent_name TEXT,
    params TEXT,
    return_type TEXT,
    modifiers TEXT,
    is_test INTEGER DEFAULT 0,
    file_hash TEXT,
    extra TEXT DEFAULT '{}',
    updated_at REAL NOT NULL,
    signature TEXT,
    community_id INTEGER
);

CREATE TABLE edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    source_qualified TEXT NOT NULL,
    target_qualified TEXT NOT NULL,
    file_path TEXT NOT NULL,
    line INTEGER DEFAULT 0,
    extra TEXT DEFAULT '{}',
    confidence REAL DEFAULT 1.0,
    confidence_tier TEXT DEFAULT 'EXTRACTED',
    updated_at REAL NOT NULL
);

CREATE TABLE metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

Indexes cover node file, kind, qualified name, community, edge source, edge target, edge kind, edge source/kind, edge target/kind, edge file, and the composite edge identity used for upserts.

## Post-Processing Tables

```sql
CREATE TABLE flows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    entry_point_id INTEGER NOT NULL,
    depth INTEGER NOT NULL,
    node_count INTEGER NOT NULL,
    file_count INTEGER NOT NULL,
    criticality REAL NOT NULL DEFAULT 0.0,
    path_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE flow_memberships (
    flow_id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    PRIMARY KEY (flow_id, node_id)
);

CREATE TABLE communities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 0,
    parent_id INTEGER,
    cohesion REAL NOT NULL DEFAULT 0.0,
    size INTEGER NOT NULL DEFAULT 0,
    dominant_language TEXT,
    description TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE VIRTUAL TABLE nodes_fts USING fts5(
    name, qualified_name, file_path, signature,
    content='nodes', content_rowid='rowid',
    tokenize='porter unicode61'
);

CREATE TABLE community_summaries (
    community_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    purpose TEXT DEFAULT '',
    key_symbols TEXT DEFAULT '[]',
    risk TEXT DEFAULT 'unknown',
    size INTEGER DEFAULT 0,
    dominant_language TEXT DEFAULT ''
);

CREATE TABLE flow_snapshots (
    flow_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    entry_point TEXT NOT NULL,
    critical_path TEXT DEFAULT '[]',
    criticality REAL DEFAULT 0.0,
    node_count INTEGER DEFAULT 0,
    file_count INTEGER DEFAULT 0
);

CREATE TABLE risk_index (
    node_id INTEGER PRIMARY KEY,
    qualified_name TEXT NOT NULL,
    risk_score REAL DEFAULT 0.0,
    caller_count INTEGER DEFAULT 0,
    test_coverage TEXT DEFAULT 'unknown',
    security_relevant INTEGER DEFAULT 0,
    last_computed TEXT DEFAULT ''
);
```

## Embeddings Store

Embeddings are stored in a separate SQLite table keyed by qualified name:

```sql
CREATE TABLE embeddings (
    qualified_name TEXT PRIMARY KEY,
    vector BLOB NOT NULL,
    text_hash TEXT NOT NULL,
    provider TEXT NOT NULL DEFAULT 'unknown'
);
```

The provider field partitions local, Google, MiniMax, and OpenAI-compatible embeddings. For OpenAI-compatible endpoints, the provider identity includes model and endpoint host/path to avoid mixing vector spaces.
