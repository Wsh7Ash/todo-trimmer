#!/usr/bin/env python3
"""Todo Trimmer CLI - Analyze and clean up your todo list."""

import argparse
import json
import sys
from pathlib import Path

from .parser import parse_todo_file
from .analyzer import analyze_todos, find_stale_items, find_duplicates
from .analyzer import text_similarity


def main():
    parser = argparse.ArgumentParser(
        description="Analyze and clean up your todo list.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s todos.md
  %(prog)s todos.md --json
  %(prog)s todos.md --stale-days 14
        """
    )
    
    parser.add_argument("todo_file", help="Path to todo file")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    parser.add_argument("-d", "--stale-days", type=int, default=30,
                        help="Days before a task is considered stale (default: 30)")
    parser.add_argument("--duplicates-only", action="store_true",
                        help="Show only duplicate detection results")
    
    args = parser.parse_args()
    
    # Read file
    try:
        with open(args.todo_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.todo_file}", file=sys.stderr)
        sys.exit(1)
    
    # Parse todos
    items = parse_todo_file(content)
    
    if not items:
        print("No todo items found in file.")
        sys.exit(0)
    
    # Analyze
    result = analyze_todos(items, args.stale_days)
    
    # Output
    if args.json:
        output = {
            "total_items": result.total_items,
            "completed": result.completed,
            "active": result.active,
            "stale_count": len(result.stale_items),
            "duplicate_groups": [
                [item.text for item in group]
                for group in result.duplicate_groups
            ],
            "categories": result.category_counts,
            "priorities": result.priority_counts,
            "stale_items": [
                {
                    "text": item.text,
                    "created": item.created_date.isoformat() if item.created_date else None,
                    "age_days": (datetime.now() - item.created_date).days if item.created_date else None
                }
                for item in result.stale_items
            ]
        }
        print(json.dumps(output, indent=2))
    elif args.duplicates_only:
        if result.duplicate_groups:
            print("POTENTIAL DUPLICATES:")
            for group in result.duplicate_groups:
                print(f"  Group: {len(group)} items")
                for item in group:
                    print(f"    - {item.text}")
        else:
            print("No duplicates found.")
    else:
        # Text report
        print(f"TODOS: {result.active} active, {result.completed} completed")
        
        if result.stale_items:
            print(f"STALE: {len(result.stale_items)} tasks older than {args.stale_days} days")
            print("\nSTALE TASKS:")
            for item in result.stale_items:
                age = (datetime.now() - item.created_date).days if item.created_date else '?'
                print(f"  [{'x' if item.completed else ' '}] {item.text} ({age} days old)")
        
        if result.duplicate_groups:
            print(f"\nDUPLICATES: {len(result.duplicate_groups)} potential duplicate groups")
            for group in result.duplicate_groups:
                print(f"\n  Group: {len(group)} similar items")
                for item in group:
                    print(f"    - {item.text}")
        
        if result.category_counts:
            print(f"\nCATEGORIES: {len(result.category_counts)} tags found")
            for cat, count in list(result.category_counts.items())[:5]:
                print(f"  #{cat}: {count}")
        
        if result.priority_counts:
            print(f"\nPRIORITIES: {sum(result.priority_counts.values())} prioritized tasks")
            for pri, count in result.priority_counts.items():
                print(f"  {pri}: {count}")
        
        if not result.stale_items and not result.duplicate_groups:
            print("\nYour todo list looks clean!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
