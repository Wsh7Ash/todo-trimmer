#!/usr/bin/env python3
"""Tests for todo-trimmer analyzer."""

import sys
from datetime import datetime, timedelta
sys.path.insert(0, 'src')

from analyzer import (
    find_stale_items, find_duplicates, text_similarity,
    analyze_todos, extract_categories
)
from parser import TodoItem


def test_text_similarity():
    """Test text similarity calculation."""
    assert text_similarity("fix bug", "fix bug") == 1.0
    assert text_similarity("fix bug", "update docs") == 0.0
    assert text_similarity("fix login bug", "fix bug") > 0.5
    assert text_similarity("buy groceries", "buy groceries and cook") >= 0.5
    print("[PASS] Text similarity works")


def test_find_stale_items():
    """Test finding stale todo items."""
    old_date = datetime.now() - timedelta(days=60)
    recent_date = datetime.now() - timedelta(days=10)
    
    items = [
        TodoItem(text="Old task", completed=False, created_date=old_date),
        TodoItem(text="Recent task", completed=False, created_date=recent_date),
        TodoItem(text="Completed task", completed=True, created_date=old_date),
    ]
    
    stale = find_stale_items(items, threshold_days=30)
    assert len(stale) == 1
    assert stale[0].text == "Old task"
    print("[PASS] Stale item detection works")


def test_find_duplicates():
    """Test duplicate detection."""
    items = [
        TodoItem(text="Fix login bug", completed=False),
        TodoItem(text="Fix login bug - check session", completed=False),
        TodoItem(text="Update documentation", completed=False),
        TodoItem(text="Write tests for auth", completed=False),
    ]
    
    duplicates = find_duplicates(items, similarity_threshold=0.3)
    assert len(duplicates) >= 1
    # First two should be in a duplicate group
    found_similar = any(
        "fix login bug" in item.text.lower()
        for group in duplicates for item in group
    )
    assert found_similar
    print("[PASS] Duplicate detection works")


def test_analyze_todos():
    """Test full analysis."""
    items = [
        TodoItem(text="Task 1", completed=False),
        TodoItem(text="Task 2", completed=True),
        TodoItem(text="Task 3 #work", completed=False, tags=["work"]),
    ]
    
    result = analyze_todos(items, stale_days=30)
    
    assert result.total_items == 3
    assert result.completed == 1
    assert result.active == 2
    assert result.category_counts.get("work") == 1
    print("[PASS] Full analysis works")


def test_extract_categories():
    """Test category extraction."""
    items = [
        TodoItem(text="Task 1", completed=False, tags=["work"]),
        TodoItem(text="Task 2", completed=False, tags=["personal"]),
        TodoItem(text="Task 3", completed=False, tags=["work", "urgent"]),
    ]
    
    counts = extract_categories(items)
    assert counts.get("work") == 2
    assert counts.get("personal") == 1
    assert counts.get("urgent") == 1
    print("[PASS] Category extraction works")


def run_tests():
    print("Running todo-trimmer analyzer tests...\n")
    test_text_similarity()
    test_find_stale_items()
    test_find_duplicates()
    test_analyze_todos()
    test_extract_categories()
    print("\n[PASS] All analyzer tests passed!")


if __name__ == "__main__":
    run_tests()
