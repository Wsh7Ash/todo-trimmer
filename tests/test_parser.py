#!/usr/bin/env python3
"""Tests for todo-trimmer parser."""

import sys
sys.path.insert(0, 'src')

from parser import parse_todo_file, parse_markdown_todos, parse_plain_todos


def test_parse_markdown_todos():
    """Test parsing markdown todo format."""
    text = """# My Tasks

- [ ] Fix login bug
- [x] Update documentation
- [ ] Write tests
"""
    items = parse_markdown_todos(text)
    
    assert len(items) == 3
    assert items[0].text == "Fix login bug"
    assert items[0].completed == False
    assert items[1].text == "Update documentation"
    assert items[1].completed == True
    assert items[2].text == "Write tests"
    print("[PASS] Markdown parsing works")


def test_parse_todo_with_date():
    """Test parsing todos with dates."""
    text = "- [ ] Fix bug (2026-09-01)"
    items = parse_markdown_todos(text)
    
    assert len(items) == 1
    assert items[0].text == "Fix bug"
    assert items[0].created_date is not None
    print("[PASS] Date extraction works")


def test_parse_todo_with_tags():
    """Test parsing todos with tags."""
    text = "- [ ] Review PR #work #urgent"
    items = parse_markdown_todos(text)
    
    assert len(items) == 1
    assert "work" in items[0].tags
    assert "urgent" in items[0].tags
    print("[PASS] Tag extraction works")


def test_parse_todo_with_priority():
    """Test parsing todos with priority."""
    text = "- [ ] Critical fix [P1]"
    items = parse_markdown_todos(text)
    
    assert len(items) == 1
    assert items[0].priority == "P1"
    print("[PASS] Priority extraction works")


def test_parse_plain_todos():
    """Test parsing plain todo format."""
    text = """Buy groceries
x Done task
- Another task
"""
    items = parse_plain_todos(text)
    
    assert len(items) == 3
    assert items[0].text == "Buy groceries"
    assert items[0].completed == False
    assert items[1].text == "Done task"
    assert items[1].completed == True
    print("[PASS] Plain text parsing works")


def test_auto_detect():
    """Test auto-detection of format."""
    md_text = "- [ ] Task"
    plain_text = "Task"
    
    md_items = parse_todo_file(md_text)
    assert len(md_items) == 1
    assert md_items[0].completed == False
    
    plain_items = parse_todo_file(plain_text)
    assert len(plain_items) == 1
    print("[PASS] Auto-detection works")


def test_empty_input():
    """Test handling of empty input."""
    items = parse_todo_file("")
    assert len(items) == 0
    print("[PASS] Empty input handling works")


def run_tests():
    print("Running todo-trimmer parser tests...\n")
    test_parse_markdown_todos()
    test_parse_todo_with_date()
    test_parse_todo_with_tags()
    test_parse_todo_with_priority()
    test_parse_plain_todos()
    test_auto_detect()
    test_empty_input()
    print("\n[PASS] All parser tests passed!")


if __name__ == "__main__":
    run_tests()
