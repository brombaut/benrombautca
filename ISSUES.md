# Issue Tracker

This project tracks work in **GitHub Issues** on [brombaut/benrombautca](https://github.com/brombaut/benrombautca/issues), managed from the terminal with the [`gh`](https://cli.github.com/) CLI.

There is no local issue database. GitHub is the single source of truth, so there is nothing to pull before reading and nothing to commit after writing.

## Conventions

Priority and type are expressed as labels, since GitHub has no native field for either.

| Label | Meaning |
| --- | --- |
| `p0` | Critical |
| `p1` | High |
| `p2` | Medium (default) |
| `p3` | Low |
| `p4` | Backlog |
| `epic` | Parent issue grouping related work |
| `feature` | New functionality |
| `task` | Small unit of work |
| `bug` | Something is broken |

Every issue gets exactly one priority label and one type label.

**Parent/child**: use GitHub's native sub-issues. An `epic` is the parent; features, tasks, and bugs are attached to it as sub-issues. Progress rolls up automatically in the GitHub UI.

## How to interact with it

All commands run from the project root.

### View open issues

```bash
gh issue list --state open --limit 50 \
  --json number,title,labels \
  --jq '.[] | "\(.number)\t\([.labels[].name]|join(","))\t\(.title)"'
```

Filter to one priority or type with `--label`:

```bash
gh issue list --state open --label epic
gh issue list --state open --label p0
```

### View a single issue

```bash
gh issue view <number>
```

Add `--comments` to include discussion, or `--web` to open it in a browser.

### View an epic and its sub-issues

```bash
gh issue view <epic-number>   # sub-issues are listed in the output
```

For just the children:

```bash
gh api repos/brombaut/benrombautca/issues/<epic-number>/sub_issues \
  --jq '.[] | "\(.number)\t\(.state)\t\(.title)"'
```

### Create an issue

```bash
gh issue create --title "Issue title" --body "Description." --label feature,p2
```

Use `--body-file` for anything longer than a sentence or two, which avoids shell quoting problems:

```bash
gh issue create --title "Issue title" --body-file /tmp/body.md --label feature,p2
```

### Attach an issue to an epic

Sub-issues are referenced by internal ID, not issue number, so look it up first:

```bash
CHILD_ID=$(gh api repos/brombaut/benrombautca/issues/<child-number> --jq .id)
gh api -X POST repos/brombaut/benrombautca/issues/<epic-number>/sub_issues \
  -F sub_issue_id=$CHILD_ID
```

### Start working on an issue

GitHub has no `in_progress` state. Assign it to yourself to signal active work:

```bash
gh issue edit <number> --add-assignee @me
```

### Close an issue

```bash
gh issue close <number> --reason completed --comment "What was done."
```

Use `--reason "not planned"` for work being abandoned. The closing comment replaces the old `close_reason` column, so write one.

### Reopen an issue

```bash
gh issue reopen <number>
```

### Change priority

```bash
gh issue edit <number> --remove-label p2 --add-label p1
```

### Epic progress

```bash
for e in $(gh issue list --state open --label epic --json number --jq '.[].number'); do
  gh api repos/brombaut/benrombautca/issues/$e/sub_issues \
    --jq "[\"#$e\", (map(select(.state==\"closed\"))|length|tostring) + \"/\" + (length|tostring) + \" done\"] | @tsv"
done
```

### Link commits to issues

Including `Fixes #123` or `Closes #123` in a commit message that lands on `main` closes that issue automatically. Prefer this over closing by hand.

## History

Issues were previously tracked in a local SQLite database (`issues.db`) and, before that, in [beads](https://github.com/steveyegge/beads). All 25 issues from that database were migrated into GitHub Issues in September 2026 as #497–#521. Each migrated issue carries a footer in its body recording its original database ID and its original creation and closure dates, since GitHub does not allow those timestamps to be backdated. The database file has been removed from the repository.
