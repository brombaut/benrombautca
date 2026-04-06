# Issue Tracker

This project tracks work in a SQLite database at `issues.db` in the project root.

## Schema

```sql
CREATE TABLE issues (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'in_progress', 'closed')),
    priority INTEGER NOT NULL DEFAULT 2 CHECK(priority BETWEEN 0 AND 4),
    type TEXT NOT NULL DEFAULT 'task' CHECK(type IN ('epic', 'feature', 'task', 'bug')),
    parent_id TEXT REFERENCES issues(id),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    closed_at TEXT,
    close_reason TEXT
);
```

**Priority**: 0 = critical, 1 = high, 2 = medium, 3 = low, 4 = backlog.

**Parent/child**: Epics are parents. Tasks, features, and bugs can have a `parent_id` pointing to an epic (or another issue). This replaces a separate dependencies table — the hierarchy is just a foreign key.

## Keeping the remote in sync

Any time you modify `issues.db` (creating, updating, or closing issues), commit and push the file immediately so the remote always has the latest issue state. Do not batch issue changes with unrelated work — commit `issues.db` on its own or alongside `ISSUES.md` changes only.

## How to interact with it

Use `sqlite3 issues.db` from the project root. All queries below work as bash one-liners or from inside the sqlite3 shell.

### View open issues

```bash
sqlite3 issues.db -header -column "
  SELECT i.id, i.title, i.type, i.priority, p.title AS parent
  FROM issues i
  LEFT JOIN issues p ON i.parent_id = p.id
  WHERE i.status = 'open'
  ORDER BY i.priority, i.type DESC, i.created_at;
"
```

### View an epic and its children

```bash
sqlite3 issues.db -header -column "
  SELECT id, title, type, status, priority
  FROM issues
  WHERE id = '<epic-id>' OR parent_id = '<epic-id>'
  ORDER BY status, priority;
"
```

### View a single issue

```bash
sqlite3 issues.db -header -column "SELECT * FROM issues WHERE id = '<issue-id>';"
```

### Create an issue

```bash
sqlite3 issues.db "
  INSERT INTO issues (id, title, description, type, priority, parent_id, created_at, updated_at)
  VALUES ('<id>', '<title>', '<description>', '<type>', <priority>, '<parent_id or NULL>', datetime('now'), datetime('now'));
"
```

For IDs, use a short descriptive slug (e.g. `fix-carousel-bug`, `add-dark-mode`). If it's a child of an epic, set `parent_id` to the epic's ID.

### Start working on an issue

```bash
sqlite3 issues.db "UPDATE issues SET status = 'in_progress', updated_at = datetime('now') WHERE id = '<issue-id>';"
```

### Close an issue

```bash
sqlite3 issues.db "
  UPDATE issues
  SET status = 'closed', closed_at = datetime('now'), updated_at = datetime('now'), close_reason = '<reason>'
  WHERE id = '<issue-id>';
"
```

### Create an epic with children

```bash
sqlite3 issues.db "
  INSERT INTO issues (id, title, type, priority, created_at, updated_at)
  VALUES ('my-epic', 'Epic title', 'epic', 2, datetime('now'), datetime('now'));

  INSERT INTO issues (id, title, description, type, priority, parent_id, created_at, updated_at)
  VALUES ('my-epic-1', 'First task', 'Description', 'task', 2, 'my-epic', datetime('now'), datetime('now'));

  INSERT INTO issues (id, title, description, type, priority, parent_id, created_at, updated_at)
  VALUES ('my-epic-2', 'Second task', 'Description', 'task', 2, 'my-epic', datetime('now'), datetime('now'));
"
```

### Check epic progress

```bash
sqlite3 issues.db -header -column "
  SELECT
    p.id,
    p.title,
    COUNT(c.id) AS total_children,
    SUM(CASE WHEN c.status = 'closed' THEN 1 ELSE 0 END) AS done,
    SUM(CASE WHEN c.status = 'in_progress' THEN 1 ELSE 0 END) AS active,
    SUM(CASE WHEN c.status = 'open' THEN 1 ELSE 0 END) AS remaining
  FROM issues p
  LEFT JOIN issues c ON c.parent_id = p.id
  WHERE p.type = 'epic' AND p.status != 'closed'
  GROUP BY p.id;
"
```

### All issues summary

```bash
sqlite3 issues.db -header -column "
  SELECT status, COUNT(*) AS count FROM issues GROUP BY status;
"
```
