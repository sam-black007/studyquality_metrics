"""
Module 7: Daily Report Generator

This module generates comprehensive daily productivity reports with:
- Summary statistics
- Visualizations (pie charts, line graphs)
- Actionable insights

Author: AI Study Focus Monitor
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import format_duration

logger = logging.getLogger(__name__)

# Try to import visualization libraries
try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    VIZ_AVAILABLE = True
except ImportError:
    logger.warning("Pandas/Matplotlib not available, visualizations will be limited")
    VIZ_AVAILABLE = False


class ReportGenerator:
    """
    Generates daily productivity reports.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the report generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.reports_dir = Path("data/reports")
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("ReportGenerator initialized")
    
    def load_session_data(self, date: str = None) -> list:
        """
        Load all session data for a specific date.
        
        Args:
            date: Date string in YYYYMMDD format (default: today)
            
        Returns:
            List of session entries
        """
        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        
        sessions_dir = Path("data/sessions")
        all_entries = []
        
        # Find all JSON files for this date
        pattern = f"session_{date}_*.json"
        for json_file in sessions_dir.glob(pattern):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_entries.extend(data.get('entries', []))
                logger.info(f"Loaded {len(data.get('entries', []))} entries from {json_file.name}")
            except Exception as e:
                logger.error(f"Error loading {json_file}: {e}")
        
        return all_entries
    
    def calculate_statistics(self, entries: list) -> dict:
        """
        Calculate summary statistics from session entries.
        
        Args:
            entries: List of session entry dictionaries
            
        Returns:
            Dictionary containing statistics
        """
        if not entries:
            return {
                'total_time': 0,
                'productive_time': 0,
                'learning_time': 0,
                'distraction_time': 0,
                'low_focus_time': 0,
                'fatigued_time': 0,
                'average_score': 0,
                'peak_hours': [],
                'low_periods': []
            }
        
        # Each entry represents 1 minute
        total_time = len(entries)
        
        # Count time by activity status
        productive_time = sum(1 for e in entries if e['activity_status'] == 'PRODUCTIVE')
        learning_time = sum(1 for e in entries if e['activity_status'] == 'LEARNING')
        distraction_time = sum(1 for e in entries if e['activity_status'] == 'DISTRACTED')
        low_focus_time = sum(1 for e in entries if e['activity_status'] == 'LOW_FOCUS')
        fatigued_time = sum(1 for e in entries if e['activity_status'] == 'FATIGUED')
        
        # Average focus score
        scores = [e['focus_score'] for e in entries]
        average_score = sum(scores) / len(scores) if scores else 0
        
        # Analyze hourly patterns
        hourly_scores = {}
        for entry in entries:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            hour = timestamp.hour
            if hour not in hourly_scores:
                hourly_scores[hour] = []
            hourly_scores[hour].append(entry['focus_score'])
        
        # Calculate average score per hour
        hourly_averages = {
            hour: sum(scores) / len(scores) 
            for hour, scores in hourly_scores.items()
        }
        
        # Find peak productivity hours (top 3)
        peak_hours = sorted(hourly_averages.items(), key=lambda x: x[1], reverse=True)[:3]
        peak_hours = [f"{hour:02d}:00" for hour, _ in peak_hours]
        
        # Find low focus periods (bottom 3)
        low_period_hours = sorted(hourly_averages.items(), key=lambda x: x[1])[:3]
        low_periods = [f"{hour:02d}:00" for hour, _ in low_period_hours]
        
        return {
            'total_time': total_time,
            'productive_time': productive_time,
            'learning_time': learning_time,
            'distraction_time': distraction_time,
            'low_focus_time': low_focus_time,
            'fatigued_time': fatigued_time,
            'average_score': round(average_score, 1),
            'peak_hours': peak_hours,
            'low_periods': low_periods,
            'hourly_averages': hourly_averages
        }
    
    def create_pie_chart(self, stats: dict, output_path: Path):
        """
        Create a pie chart showing time distribution.
        
        Args:
            stats: Statistics dictionary
            output_path: Path to save the chart
        """
        if not VIZ_AVAILABLE:
            logger.warning("Visualization libraries not available")
            return
        
        # Prepare data
        labels = []
        sizes = []
        colors = []
        
        if stats['productive_time'] > 0:
            labels.append('Productive Study')
            sizes.append(stats['productive_time'])
            colors.append('#2ecc71')  # Green
        
        if stats['learning_time'] > 0:
            labels.append('Educational Video')
            sizes.append(stats['learning_time'])
            colors.append('#3498db')  # Blue
        
        if stats['distraction_time'] > 0:
            labels.append('Distracted')
            sizes.append(stats['distraction_time'])
            colors.append('#e74c3c')  # Red
        
        if stats['low_focus_time'] > 0:
            labels.append('Low Focus')
            sizes.append(stats['low_focus_time'])
            colors.append('#f39c12')  # Orange
        
        if stats['fatigued_time'] > 0:
            labels.append('Fatigued')
            sizes.append(stats['fatigued_time'])
            colors.append('#95a5a6')  # Gray
        
        if not sizes:
            logger.warning("No data to create pie chart")
            return
        
        # Create pie chart
        plt.figure(figsize=(10, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title('Time Distribution by Activity', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Pie chart saved: {output_path}")
    
    def create_timeline_chart(self, entries: list, output_path: Path):
        """
        Create a line chart showing focus score over time.
        
        Args:
            entries: List of session entries
            output_path: Path to save the chart
        """
        if not VIZ_AVAILABLE or not entries:
            logger.warning("Cannot create timeline chart")
            return
        
        # Extract timestamps and scores
        timestamps = [datetime.fromisoformat(e['timestamp']) for e in entries]
        scores = [e['focus_score'] for e in entries]
        
        # Create line chart
        plt.figure(figsize=(14, 6))
        plt.plot(timestamps, scores, linewidth=2, color='#3498db')
        plt.fill_between(timestamps, scores, alpha=0.3, color='#3498db')
        
        # Add horizontal lines for reference
        plt.axhline(y=80, color='#2ecc71', linestyle='--', alpha=0.5, label='Good Focus')
        plt.axhline(y=50, color='#f39c12', linestyle='--', alpha=0.5, label='Moderate')
        plt.axhline(y=30, color='#e74c3c', linestyle='--', alpha=0.5, label='Distracted')
        
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Focus Score', fontsize=12)
        plt.title('Focus Score Over Time', fontsize=16, fontweight='bold')
        plt.ylim(0, 100)
        plt.legend(loc='upper right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Timeline chart saved: {output_path}")
    
    def create_hourly_chart(self, stats: dict, output_path: Path):
        """
        Create a bar chart showing average focus score by hour.
        
        Args:
            stats: Statistics dictionary
            output_path: Path to save the chart
        """
        if not VIZ_AVAILABLE or 'hourly_averages' not in stats:
            logger.warning("Cannot create hourly chart")
            return
        
        hourly_data = stats['hourly_averages']
        if not hourly_data:
            return
        
        # Sort by hour
        hours = sorted(hourly_data.keys())
        scores = [hourly_data[h] for h in hours]
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(hours, scores, color='#3498db', alpha=0.7)
        
        # Color code bars
        for i, score in enumerate(scores):
            if score >= 80:
                bars[i].set_color('#2ecc71')  # Green
            elif score >= 50:
                bars[i].set_color('#f39c12')  # Orange
            else:
                bars[i].set_color('#e74c3c')  # Red
        
        plt.xlabel('Hour of Day', fontsize=12)
        plt.ylabel('Average Focus Score', fontsize=12)
        plt.title('Productivity by Hour', fontsize=16, fontweight='bold')
        plt.xticks(hours, [f"{h:02d}:00" for h in hours], rotation=45)
        plt.ylim(0, 100)
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Hourly chart saved: {output_path}")
    
    def generate_text_summary(self, stats: dict, date_str: str) -> str:
        """
        Generate a text summary of the day's productivity.
        
        Args:
            stats: Statistics dictionary
            date_str: Date string for the report
            
        Returns:
            Formatted text summary
        """
        summary_lines = [
            "=" * 60,
            f"📊 Daily Study Report - {date_str}",
            "=" * 60,
            "",
            "📈 PRODUCTIVITY SUMMARY",
            f"✅ Productive Study Time: {format_duration(stats['productive_time'] * 60)}",
            f"📚 Educational Video Time: {format_duration(stats['learning_time'] * 60)}",
            f"🎯 Average Focus Score: {stats['average_score']}/100",
            "",
            "⚠️ DISTRACTIONS",
            f"📱 Distraction Time: {format_duration(stats['distraction_time'] * 60)}",
            f"😴 Fatigued Time: {format_duration(stats['fatigued_time'] * 60)}",
            f"🔄 Low Focus Time: {format_duration(stats['low_focus_time'] * 60)}",
            "",
        ]
        
        # Add insights
        if stats['peak_hours']:
            summary_lines.append("💡 INSIGHTS")
            summary_lines.append(f"🌟 Peak Productivity Hours: {', '.join(stats['peak_hours'])}")
        
        if stats['low_periods']:
            summary_lines.append(f"⏰ Low Focus Periods: {', '.join(stats['low_periods'])}")
        
        # Add recommendations
        summary_lines.append("")
        summary_lines.append("🎓 RECOMMENDATIONS")
        
        if stats['average_score'] >= 80:
            summary_lines.append("Excellent focus today! Keep up the great work.")
        elif stats['average_score'] >= 60:
            summary_lines.append("Good focus overall. Consider minimizing distractions during low periods.")
        else:
            summary_lines.append("Focus could be improved. Try the Pomodoro technique or shorter study blocks.")
        
        if stats['distraction_time'] > stats['productive_time']:
            summary_lines.append("⚠️ Distraction time exceeded productive time. Consider using website blockers.")
        
        if stats['fatigued_time'] > 30:
            summary_lines.append("😴 High fatigue detected. Ensure adequate sleep and take regular breaks.")
        
        summary_lines.append("")
        summary_lines.append("=" * 60)
        
        return "\n".join(summary_lines)
    
    def generate_daily_report(self, date: str = None) -> dict:
        """
        Generate a complete daily report.
        
        Args:
            date: Date string in YYYYMMDD format (default: today)
            
        Returns:
            Dictionary containing report info
        """
        if date is None:
            date = datetime.now().strftime("%Y%m%d")
        
        date_formatted = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")
        
        logger.info(f"Generating report for {date_formatted}")
        
        # Load session data
        entries = self.load_session_data(date)
        
        if not entries:
            logger.warning(f"No data found for {date}")
            return {
                'date': date_formatted,
                'status': 'no_data',
                'message': 'No session data found for this date'
            }
        
        # Calculate statistics
        stats = self.calculate_statistics(entries)
        
        # Create output directory for this date
        report_dir = self.reports_dir / f"report_{date}"
        report_dir.mkdir(exist_ok=True)
        
        # Generate visualizations
        pie_chart_path = report_dir / "time_distribution.png"
        timeline_path = report_dir / "focus_timeline.png"
        hourly_path = report_dir / "hourly_productivity.png"
        
        self.create_pie_chart(stats, pie_chart_path)
        self.create_timeline_chart(entries, timeline_path)
        self.create_hourly_chart(stats, hourly_path)
        
        # Generate text summary
        text_summary = self.generate_text_summary(stats, date_formatted)
        
        # Save text summary
        summary_path = report_dir / "summary.txt"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(text_summary)
        
        # Print summary to console
        print(text_summary)
        
        logger.info(f"Report generated successfully: {report_dir}")
        
        return {
            'date': date_formatted,
            'status': 'success',
            'stats': stats,
            'report_dir': str(report_dir),
            'files': {
                'summary': str(summary_path),
                'pie_chart': str(pie_chart_path) if VIZ_AVAILABLE else None,
                'timeline': str(timeline_path) if VIZ_AVAILABLE else None,
                'hourly': str(hourly_path) if VIZ_AVAILABLE else None
            }
        }


def main():
    """
    Test the ReportGenerator module independently.
    """
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.helpers import load_config
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load config
    config = load_config()
    
    # Initialize generator
    generator = ReportGenerator(config)
    
    # Generate report for today (or specified date)
    date_arg = sys.argv[1] if len(sys.argv) > 1 else None
    
    if date_arg and date_arg.startswith('--date='):
        report_date = date_arg.split('=')[1]
    else:
        report_date = None
    
    result = generator.generate_daily_report(report_date)
    
    if result['status'] == 'success':
        print(f"\nReport saved to: {result['report_dir']}")
    else:
        print(f"\n{result['message']}")


if __name__ == "__main__":
    main()
