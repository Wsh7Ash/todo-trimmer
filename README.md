# 📋 Todo Trimmer

A CLI tool that helps you review and clean up your todo list. Identify stale tasks, duplicate items, and prioritize what matters.

## The Problem

Todo lists grow over time. Old tasks accumulate, duplicates creep in, and it becomes hard to focus on what's actually important.

## What It Does

Todo Trimmer analyzes your todo file and:
- **Finds stale tasks** - items untouched for 30+ days
- **Detects duplicates** - similar tasks that can be merged
- **Summarizes categories** - see where your tasks cluster
- **Suggests pruning** - identify candidates for deletion or archiving

## Features

- Supports common todo formats (markdown lists, plain text)
- Age analysis with visual indicators
- Duplicate detection using text similarity
- Category extraction from tags/prefixes
- JSON output for further processing

## Requirements

- Python 3.8+

## Quick Start

```bash
python -m todo_trimmer.cli todos.md
```

### Example Input (todos.md)

```markdown
# My Tasks

- [ ] Fix login bug (2026-09-01)
- [x] Update documentation
- [ ] Write tests for auth module
- [ ] Fix login bug - need to check session
- [ ] Review PR #42
- [ ] Buy groceries
```

### Example Output

```
TODOS: 5 active, 1 completed
STALE: 2 tasks older than 30 days
DUPLICATES: 1 potential duplicate pair

STALE TASKS:
  [ ] Fix login bug (2026-09-01) - 38 days old

POTENTIAL DUPLICATES:
  "Fix login bug" <-> "Fix login bug - need to check session"
```

## Usage

```bash
# Analyze markdown todo file
python -m todo_trimmer.cli todos.md

# Output as JSON
python -m todo_trimmer.cli todos.md --json

# Set stale threshold (days)
python -m todo_trimmer.cli todos.md --stale-days 14
```

## Project Structure

```
todo-trimmer/
├── src/
│   ├── cli.py
│   ├── parser.py
│   ├── analyzer.py
│   └── report.py
├── tests/
├── docs/
├── .github/workflows/ci.yml
├── LICENSE
└── README.md
```

## License

MIT License
