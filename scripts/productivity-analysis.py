#!/usr/bin/env python3
"""
VS Code Productivity Toolkit - Productivity Analysis Script

Analyzes the productivity impact of using the VS Code Productivity Toolkit
by measuring task usage, time savings, and workflow improvements.

Author: Diogo Ribeiro (dfr@esmad.ipp.pt)
License: MIT
"""

import os
import sys
import json
import time
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import argparse
import statistics
import subprocess

@dataclass
class TaskMetrics:
    """Metrics for a single task."""
    name: str
    category: str
    execution_count: int
    total_time: float
    average_time: float
    success_rate: float
    last_used: datetime
    time_saved: float  # Estimated time saved vs manual execution

@dataclass
class ProductivityMetrics:
    """Overall productivity metrics."""
    total_tasks_run: int
    total_time_saved: float
    most_used_category: str
    most_used_task: str
    daily_average_usage: float
    weekly_trend: List[int]
    automation_coverage: float

class ProductivityAnalyzer:
    """Analyzes productivity metrics from VS Code task usage."""
    
    def __init__(self, workspace_path: str = '.'):
        self.workspace_path = Path(workspace_path).resolve()
        self.db_path = self.workspace_path / '.vscode' / 'productivity_metrics.db'
        self.tasks_file = self.workspace_path / '.vscode' / 'tasks.json'
        self._init_database()
        
    def _init_database(self):
        """Initialize SQLite database for tracking metrics."""
        self.db_path.parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS task_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT NOT NULL,
                    category TEXT,
                    execution_time REAL,
                    success BOOLEAN,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    workspace_path TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS productivity_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_start DATETIME,
                    session_end DATETIME,
                    tasks_run INTEGER,
                    time_saved REAL,
                    workspace_path TEXT
                )
            ''')
            
            conn.commit()

    def record_task_execution(self, 
                            task_name: str,
                            category: str = 'unknown',
                            execution_time: float = 0.0,
                            success: bool = True):
        """Record a task execution for analysis."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO task_executions 
                (task_name, category, execution_time, success, workspace_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (task_name, category, execution_time, success, str(self.workspace_path)))
            conn.commit()

    def get_task_metrics(self, days: int = 30) -> List[TaskMetrics]:
        """Get metrics for all tasks in the specified time period."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    task_name,
                    category,
                    COUNT(*) as execution_count,
                    SUM(execution_time) as total_time,
                    AVG(execution_time) as average_time,
                    AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as success_rate,
                    MAX(timestamp) as last_used
                FROM task_executions 
                WHERE timestamp >= ? AND workspace_path = ?
                GROUP BY task_name, category
                ORDER BY execution_count DESC
            ''', (cutoff_date.isoformat(), str(self.workspace_path)))
            
            results = []
            for row in cursor.fetchall():
                task_name, category, count, total_time, avg_time, success_rate, last_used = row
                
                # Estimate time saved (rough calculation)
                estimated_manual_time = self._estimate_manual_time(task_name, category)
                time_saved = count * max(0, estimated_manual_time - (avg_time or 0))
                
                results.append(TaskMetrics(
                    name=task_name,
                    category=category or 'unknown',
                    execution_count=count,
                    total_time=total_time or 0.0,
                    average_time=avg_time or 0.0,
                    success_rate=success_rate or 0.0,
                    last_used=datetime.fromisoformat(last_used) if last_used else datetime.now(),
                    time_saved=time_saved
                ))
            
            return results

    def _estimate_manual_time(self, task_name: str, category: str) -> float:
        """Estimate how long a task would take manually."""
        # Rough estimates in seconds
        manual_estimates = {
            'lint': 30,     # Manual code review
            'format': 60,   # Manual formatting
            'test': 120,    # Manual testing
            'build': 180,   # Manual build process
            'deploy': 300,  # Manual deployment
            'backup': 240,  # Manual backup
            'setup': 600,   # Manual environment setup
        }
        
        # Check task name for keywords
        task_lower = task_name.lower()
        for keyword, estimate in manual_estimates.items():
            if keyword in task_lower:
                return estimate
        
        # Category-based estimates
        category_estimates = {
            'python': 90,
            'javascript': 90,
            'docker': 180,
            'git': 60,
            'general': 120
        }
        
        return category_estimates.get(category.lower(), 60)

    def get_productivity_metrics(self, days: int = 30) -> ProductivityMetrics:
        """Calculate overall productivity metrics."""
        task_metrics = self.get_task_metrics(days)
        
        if not task_metrics:
            return ProductivityMetrics(
                total_tasks_run=0,
                total_time_saved=0.0,
                most_used_category='none',
                most_used_task='none',
                daily_average_usage=0.0,
                weekly_trend=[0] * 7,
                automation_coverage=0.0
            )
        
        total_tasks_run = sum(m.execution_count for m in task_metrics)
        total_time_saved = sum(m.time_saved for m in task_metrics)
        
        # Most used category
        category_counts = {}
        for metric in task_metrics:
            category_counts[metric.category] = category_counts.get(metric.category, 0) + metric.execution_count
        most_used_category = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else 'none'
        
        # Most used task
        most_used_task = max(task_metrics, key=lambda x: x.execution_count).name if task_metrics else 'none'
        
        # Daily average
        daily_average_usage = total_tasks_run / days
        
        # Weekly trend
        weekly_trend = self._get_weekly_trend(days)
        
        # Automation coverage (what percentage of development tasks are automated)
        automation_coverage = self._calculate_automation_coverage()
        
        return ProductivityMetrics(
            total_tasks_run=total_tasks_run,
            total_time_saved=total_time_saved,
            most_used_category=most_used_category,
            most_used_task=most_used_task,
            daily_average_usage=daily_average_usage,
            weekly_trend=weekly_trend,
            automation_coverage=automation_coverage
        )

    def _get_weekly_trend(self, days: int) -> List[int]:
        """Get task execution counts for each day of the week."""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT 
                    strftime('%w', timestamp) as day_of_week,
                    COUNT(*) as count
                FROM task_executions 
                WHERE timestamp >= ? AND workspace_path = ?
                GROUP BY day_of_week
            ''', (cutoff_date.isoformat(), str(self.workspace_path)))
            
            # Initialize all days to 0
            weekly_counts = [0] * 7  # Sunday = 0, Monday = 1, etc.
            
            for row in cursor.fetchall():
                day_of_week, count = row
                weekly_counts[int(day_of_week)] = count
            
            return weekly_counts

    def _calculate_automation_coverage(self) -> float:
        """Calculate what percentage of common development tasks are automated."""
        if not self.tasks_file.exists():
            return 0.0
        
        try:
            with open(self.tasks_file, 'r') as f:
                tasks_data = json.load(f)
            
            installed_tasks = tasks_data.get('tasks', [])
            task_names = [task.get('label', '').lower() for task in installed_tasks]
            
            # Common development tasks that should be automated
            common_tasks = [
                'lint', 'format', 'test', 'build', 'deploy', 'start', 'install',
                'backup', 'clean', 'setup', 'check', 'validate', 'run', 'watch'
            ]
            
            automated_count = sum(1 for common_task in common_tasks 
                                if any(common_task in task_name for task_name in task_names))
            
            return (automated_count / len(common_tasks)) * 100
            
        except Exception as e:
            print(f"Warning: Could not calculate automation coverage: {e}")
            return 0.0

    def generate_report(self, days: int = 30, output_format: str = 'console') -> str:
        """Generate a comprehensive productivity report."""
        metrics = self.get_productivity_metrics(days)
        task_metrics = self.get_task_metrics(days)
        
        if output_format == 'json':
            return self._generate_json_report(metrics, task_metrics, days)
        else:
            return self._generate_console_report(metrics, task_metrics, days)

    def _generate_console_report(self, 
                                metrics: ProductivityMetrics,
                                task_metrics: List[TaskMetrics],
                                days: int) -> str:
        """Generate a human-readable console report."""
        report = []
        report.append("🚀 VS Code Productivity Toolkit - Analysis Report")
        report.append("=" * 60)
        report.append(f"Analysis Period: Last {days} days")
        report.append(f"Workspace: {self.workspace_path}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Overall metrics
        report.append("📊 OVERALL PRODUCTIVITY METRICS")
        report.append("-" * 40)
        report.append(f"Total Tasks Executed: {metrics.total_tasks_run}")
        report.append(f"Estimated Time Saved: {metrics.total_time_saved/60:.1f} minutes ({metrics.total_time_saved/3600:.1f} hours)")
        report.append(f"Daily Average Usage: {metrics.daily_average_usage:.1f} tasks/day")
        report.append(f"Automation Coverage: {metrics.automation_coverage:.1f}%")
        report.append(f"Most Used Category: {metrics.most_used_category}")
        report.append(f"Most Used Task: {metrics.most_used_task}")
        report.append("")
        
        # Weekly trend
        if sum(metrics.weekly_trend) > 0:
            report.append("📈 WEEKLY USAGE PATTERN")
            report.append("-" * 40)
            days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            for i, count in enumerate(metrics.weekly_trend):
                report.append(f"{days_of_week[i]}: {'█' * (count // max(1, max(metrics.weekly_trend) // 20))} ({count})")
            report.append("")
        
        # Top tasks
        if task_metrics:
            report.append("🏆 TOP TASKS BY USAGE")
            report.append("-" * 40)
            top_tasks = sorted(task_metrics, key=lambda x: x.execution_count, reverse=True)[:10]
            for i, task in enumerate(top_tasks, 1):
                time_saved_mins = task.time_saved / 60
                report.append(f"{i:2d}. {task.name}")
                report.append(f"    Category: {task.category}")
                report.append(f"    Used: {task.execution_count} times")
                report.append(f"    Time Saved: {time_saved_mins:.1f} minutes")
                report.append(f"    Success Rate: {task.success_rate*100:.1f}%")
                report.append("")
        
        # Category breakdown
        if task_metrics:
            report.append("📋 CATEGORY BREAKDOWN")
            report.append("-" * 40)
            category_stats = {}
            for task in task_metrics:
                if task.category not in category_stats:
                    category_stats[task.category] = {'count': 0, 'time_saved': 0.0}
                category_stats[task.category]['count'] += task.execution_count
                category_stats[task.category]['time_saved'] += task.time_saved
            
            for category, stats in sorted(category_stats.items(), key=lambda x: x[1]['count'], reverse=True):
                report.append(f"{category.title()}:")
                report.append(f"  Executions: {stats['count']}")
                report.append(f"  Time Saved: {stats['time_saved']/60:.1f} minutes")
                report.append("")
        
        # Recommendations
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 40)
        
        if metrics.automation_coverage < 50:
            report.append("• Consider installing more task categories to increase automation coverage")
        
        if metrics.daily_average_usage < 1:
            report.append("• Try to use automated tasks more frequently to maximize time savings")
        
        if task_metrics and max(task_metrics, key=lambda x: x.success_rate).success_rate < 0.9:
            report.append("• Some tasks have low success rates - consider reviewing task configurations")
        
        if not task_metrics:
            report.append("• No task usage detected - make sure to run tasks through VS Code")
        
        report.append("")
        report.append("🎯 Keep automating to boost your productivity!")
        
        return "\n".join(report)

    def _generate_json_report(self, 
                            metrics: ProductivityMetrics,
                            task_metrics: List[TaskMetrics],
                            days: int) -> str:
        """Generate a JSON report for programmatic processing."""
        report_data = {
            'metadata': {
                'analysis_period_days': days,
                'workspace_path': str(self.workspace_path),
                'generated_at': datetime.now().isoformat(),
                'toolkit_version': '1.0.0'
            },
            'overall_metrics': asdict(metrics),
            'task_metrics': [asdict(task) for task in task_metrics],
            'insights': {
                'high_impact_tasks': [
                    task.name for task in sorted(task_metrics, key=lambda x: x.time_saved, reverse=True)[:5]
                ],
                'improvement_opportunities': self._get_improvement_opportunities(metrics, task_metrics),
                'productivity_score': self._calculate_productivity_score(metrics, task_metrics)
            }
        }
        
        return json.dumps(report_data, indent=2, default=str)

    def _get_improvement_opportunities(self, 
                                     metrics: ProductivityMetrics,
                                     task_metrics: List[TaskMetrics]) -> List[str]:
        """Identify opportunities for productivity improvement."""
        opportunities = []
        
        if metrics.automation_coverage < 30:
            opportunities.append("low_automation_coverage")
        
        if metrics.daily_average_usage < 0.5:
            opportunities.append("underutilized_automation")
        
        if task_metrics:
            avg_success_rate = statistics.mean(task.success_rate for task in task_metrics)
            if avg_success_rate < 0.8:
                opportunities.append("task_reliability_issues")
        
        return opportunities

    def _calculate_productivity_score(self, 
                                    metrics: ProductivityMetrics,
                                    task_metrics: List[TaskMetrics]) -> float:
        """Calculate an overall productivity score (0-100)."""
        score = 0.0
        
        # Automation coverage (40% of score)
        score += (metrics.automation_coverage / 100) * 40
        
        # Usage frequency (30% of score)
        max_reasonable_daily_usage = 10  # Reasonable daily task usage
        usage_score = min(metrics.daily_average_usage / max_reasonable_daily_usage, 1.0)
        score += usage_score * 30
        
        # Success rate (30% of score)
        if task_metrics:
            avg_success_rate = statistics.mean(task.success_rate for task in task_metrics)
            score += avg_success_rate * 30
        
        return min(score, 100.0)

    def export_metrics(self, output_file: str, days: int = 30):
        """Export metrics to a file."""
        report = self.generate_report(days, 'json')
        with open(output_file, 'w') as f:
            f.write(report)
        print(f"Metrics exported to: {output_file}")

def main():
    """Main entry point for productivity analysis."""
    parser = argparse.ArgumentParser(
        description='Analyze VS Code Productivity Toolkit usage and impact',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate productivity report for last 30 days
  python productivity-analysis.py

  # Analyze specific time period
  python productivity-analysis.py --days 7

  # Export metrics to JSON
  python productivity-analysis.py --export metrics.json

  # Analyze specific workspace
  python productivity-analysis.py --workspace /path/to/project
        """
    )
    
    parser.add_argument('--workspace', default='.', help='Workspace path to analyze')
    parser.add_argument('--days', type=int, default=30, help='Analysis period in days')
    parser.add_argument('--export', help='Export metrics to JSON file')
    parser.add_argument('--format', choices=['console', 'json'], default='console', help='Output format')
    
    args = parser.parse_args()
    
    analyzer = ProductivityAnalyzer(args.workspace)
    
    if args.export:
        analyzer.export_metrics(args.export, args.days)
    else:
        report = analyzer.generate_report(args.days, args.format)
        print(report)

if __name__ == '__main__':
    main()
