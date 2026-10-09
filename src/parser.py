#!/usr/bin/env python3
"""Parse todo files in various formats."""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class TodoItem:
    text: str
    completed: bool
    created_date: datetime = None
    tags: List[str] = None
    priority: str = None


def parse_markdown_todos(text: str) -> List[TodoItem]:
    """Parse markdown todo format (- [ ] task or - [x] task)."""
    items = []
    lines = text.split('\n')
    
    for line in lines:
        # Match - [ ] or - [x] or - [X]
        match = re.match(r'^[\s]*-[\s]+\[([ xX])\][\s]+(.+)$', line)
        if match:
            done = match.group(1).lower() == 'x'
            text = match.group(2).strip()
            
            # Extract date if present (e.g., "Task (2026-09-01)")
            date_match = re.search(r'\((\d{4}-\d{2}-\d{2})\)', text)
            created = None
            if date_match:
                try:
                    created = datetime.strptime(date_match.group(1), '%Y-%m-%d')
                except ValueError:
                    pass
            
            # Extract tags (e.g., #work, #personal)
            tags = re.findall(r'#(\w+)', text)
            
            # Extract priority (e.g., [P1], [HIGH])
            priority_match = re.search(r'\[(P\d+|HIGH|MEDIUM|LOW)\]', text, re.IGNORECASE)
            priority = priority_match.group(1).upper() if priority_match else None
            
            # Clean text (remove date, tags, priority markers for display)
            clean_text = re.sub(r'\s*\(\d{4}-\d{2}-\d{2}\)', '', text)
            clean_text = re.sub(r'\s*#(\w+)', '', clean_text)
            clean_text = re.sub(r'\s*\[(P\d+|HIGH|MEDIUM|LOW)\]', '', clean_text, flags=re.IGNORECASE)
            clean_text = clean_text.strip()
            
            items.append(TodoItem(
                text=clean_text,
                completed=done,
                created_date=created,
                tags=tags,
                priority=priority
            ))
    
    return items


def parse_plain_todos(text: str) -> List[TodoItem]:
    """Parse simple line-based todo format."""
    items = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        # Check for completion markers
        if line.startswith('x ') or line.startswith('X ') or line.startswith('[x] ') or line.startswith('[X] '):
            completed = True
            text = line.lstrip('xX[] ').strip()
        else:
            completed = False
            text = line.lstrip('-* ').strip()
        
        if text:
            items.append(TodoItem(text=text, completed=completed))
    
    return items


def parse_todo_file(text: str) -> List[TodoItem]:
    """Auto-detect format and parse todos."""
    # Try markdown first
    if re.search(r'-\s*\[[ xX]\]', text):
        return parse_markdown_todos(text)
    else:
        return parse_plain_todos(text)
