#!/usr/bin/env python3
"""Analyze todo lists for staleness, duplicates, and patterns."""

from datetime import datetime, timedelta
from typing import List, Dict
from dataclasses import dataclass
try:
    from .parser import TodoItem
except ImportError:
    from parser import TodoItem


@dataclass
class AnalysisResult:
    total_items: int
    completed: int
    active: int
    stale_items: List[TodoItem]
    duplicate_groups: List[List[TodoItem]]
    category_counts: Dict[str, int]
    priority_counts: Dict[str, int]


def find_stale_items(items: List[TodoItem], threshold_days: int = 30, 
                     reference_date: datetime = None) -> List[TodoItem]:
    """Find items that haven't been touched in threshold_days."""
    if reference_date is None:
        reference_date = datetime.now()
    
    threshold = reference_date - timedelta(days=threshold_days)
    stale = []
    
    for item in items:
        if item.completed:
            continue
        if item.created_date and item.created_date < threshold:
            stale.append(item)
    
    return stale


def find_duplicates(items: List[TodoItem], similarity_threshold: float = 0.6) -> List[List[TodoItem]]:
    """Find potential duplicate tasks using simple text similarity."""
    active = [i for i in items if not i.completed]
    duplicates = []
    used = set()
    
    for i, item1 in enumerate(active):
        if i in used:
            continue
        
        group = [item1]
        for j, item2 in enumerate(active[i+1:], start=i+1):
            if j in used and j != i:
                continue
            
            similarity = text_similarity(item1.text.lower(), item2.text.lower())
            if similarity >= similarity_threshold:
                group.append(item2)
                used.add(j)
        
        if len(group) > 1:
            duplicates.append(group)
            used.add(i)
    
    return duplicates


def text_similarity(text1: str, text2: str) -> float:
    """Simple word-based similarity score (0.0 to 1.0)."""
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    if not words1 or not words2:
        return 0.0
    
    # Jaccard similarity
    intersection = words1 & words2
    union = words1 | words2
    
    return len(intersection) / len(union)


def extract_categories(items: List[TodoItem]) -> Dict[str, int]:
    """Extract category counts from tags."""
    counts = {}
    for item in items:
        for tag in item.tags or []:
            counts[tag] = counts.get(tag, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))


def extract_priorities(items: List[TodoItem]) -> Dict[str, int]:
    """Extract priority counts."""
    counts = {}
    for item in items:
        if item.priority:
            counts[item.priority] = counts.get(item.priority, 0) + 1
    return dict(sorted(counts.items()))


def analyze_todos(items: List[TodoItem], stale_days: int = 30) -> AnalysisResult:
    """Perform full analysis of todo list."""
    completed = sum(1 for i in items if i.completed)
    active = len(items) - completed
    
    return AnalysisResult(
        total_items=len(items),
        completed=completed,
        active=active,
        stale_items=find_stale_items(items, stale_days),
        duplicate_groups=find_duplicates(items),
        category_counts=extract_categories(items),
        priority_counts=extract_priorities(items)
    )
