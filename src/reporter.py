"""
Report Generation Module
Creates daily/session productivity reports with charts and summaries
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Dict, List
import numpy as np

from src.config import (
    SESSION_LOG_CSV, REPORTS_DIR,
    CHART_DPI, CHART_FIGSIZE, LOG_INTERVAL
)


class ReportGenerator:
    """
    Generates productivity reports from session logs
    """
    
    def __init__(self):
        os.makedirs(REPORTS_DIR, exist_ok=True)
    
    def load_session_data(self, date: str = None) -> pd.DataFrame:
        """
        Load session data from CSV
        
        Args:
            date: Optional date string (YYYY-MM-DD) to filter data
            
        Returns:
            DataFrame with session data
        """
        if not os.path.exists(SESSION_LOG_CSV):
            return pd.DataFrame()
        
        df = pd.read_csv(SESSION_LOG_CSV)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filter by date if specified
        if date:
            target_date = pd.to_datetime(date).date()
            df = df[df['timestamp'].dt.date == target_date]
        
        return df
    
    def calculate_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Calculate statistics from session data
        
        Args:
            df: DataFrame with session data
            
        Returns:
            Dictionary with statistics
        """
        if df.empty:
            return {
                'total_time': 0,
                'productive_time': 0,
                'learning_time': 0,
                'distracted_time': 0,
                'fatigued_time': 0,
                'avg_focus_score': 0,
                'peak_focus_hour': None,
                'lowest_focus_hour': None
            }
        
        time_per_entry = LOG_INTERVAL / 60  # Minutes
        
        # Time by activity
        activity_counts = df['activity_status'].value_counts()
        
        productive_time = activity_counts.get('PRODUCTIVE', 0) * time_per_entry
        learning_time = activity_counts.get('LEARNING', 0) * time_per_entry
        distracted_time = activity_counts.get('DISTRACTED', 0) * time_per_entry
        fatigued_time = activity_counts.get('FATIGUED', 0) * time_per_entry
        total_time = len(df) * time_per_entry
        
        # Average focus score
        avg_score = df['focus_score'].mean()
        
        # Peak and lowest focus hours
        df['hour'] = df['timestamp'].dt.hour
        hourly_scores = df.groupby('hour')['focus_score'].mean()
        
        peak_hour = hourly_scores.idxmax() if not hourly_scores.empty else None
        lowest_hour = hourly_scores.idxmin() if not hourly_scores.empty else None
        
        return {
            'total_time': total_time,
            'productive_time': productive_time,
            'learning_time': learning_time,
            'distracted_time': distracted_time,
            'fatigued_time': fatigued_time,
            'avg_focus_score': avg_score,
            'peak_focus_hour': peak_hour,
            'lowest_focus_hour': lowest_hour,
            'total_entries': len(df)
        }
    
    def plot_activity_pie_chart(self, df: pd.DataFrame, save_path: str):
        """Create pie chart of activity distribution"""
        if df.empty:
            return
        
        activity_counts = df['activity_status'].value_counts()
        
        colors = {
            'PRODUCTIVE': '#4CAF50',
            'LEARNING': '#2196F3',
            'LOW_FOCUS': '#FFC107',
            'DISTRACTED': '#FF5722',
            'FATIGUED': '#9E9E9E'
        }
        
        fig, ax = plt.subplots(figsize=(8, 8))
        
        wedges, texts, autotexts = ax.pie(
            activity_counts.values,
            labels=activity_counts.index,
            autopct='%1.1f%%',
            colors=[colors.get(act, '#CCCCCC') for act in activity_counts.index],
            startangle=90
        )
        
        # Styling
        for text in texts:
            text.set_fontsize(12)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title('Activity Distribution', fontsize=16, weight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=CHART_DPI, bbox_inches='tight')
        plt.close()
    
    def plot_focus_timeline(self, df: pd.DataFrame, save_path: str):
        """Create timeline chart of focus score"""
        if df.empty:
            return
        
        fig, ax = plt.subplots(figsize=CHART_FIGSIZE)
        
        # Plot focus score over time
        ax.plot(df['timestamp'], df['focus_score'], 
                linewidth=2, color='#2196F3', alpha=0.7)
        
        # Add horizontal lines for score ranges
        ax.axhline(y=80, color='green', linestyle='--', alpha=0.3, label='Excellent')
        ax.axhline(y=60, color='blue', linestyle='--', alpha=0.3, label='Good')
        ax.axhline(y=40, color='orange', linestyle='--', alpha=0.3, label='Fair')
        ax.axhline(y=20, color='red', linestyle='--', alpha=0.3, label='Poor')
        
        # Styling
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Focus Score', fontsize=12)
        ax.set_title('Focus Score Over Time', fontsize=16, weight='bold')
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=CHART_DPI, bbox_inches='tight')
        plt.close()
    
    def plot_hourly_focus(self, df: pd.DataFrame, save_path: str):
        """Create bar chart of average focus by hour"""
        if df.empty:
            return
        
        df['hour'] = df['timestamp'].dt.hour
        hourly_avg = df.groupby('hour')['focus_score'].mean()
        
        fig, ax = plt.subplots(figsize=CHART_FIGSIZE)
        
        bars = ax.bar(hourly_avg.index, hourly_avg.values, 
                      color='#4CAF50', alpha=0.7, edgecolor='black')
        
        # Color bars by score
        for i, (hour, score) in enumerate(hourly_avg.items()):
            if score >= 80:
                bars[i].set_color('#4CAF50')  # Green
            elif score >= 60:
                bars[i].set_color('#2196F3')  # Blue
            elif score >= 40:
                bars[i].set_color('#FFC107')  # Yellow
            else:
                bars[i].set_color('#FF5722')  # Red
        
        ax.set_xlabel('Hour of Day', fontsize=12)
        ax.set_ylabel('Average Focus Score', fontsize=12)
        ax.set_title('Focus Score by Hour', fontsize=16, weight='bold')
        ax.set_ylim(0, 100)
        ax.set_xticks(range(24))
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=CHART_DPI, bbox_inches='tight')
        plt.close()
    
    def generate_text_summary(self, stats: Dict) -> str:
        """
        Generate text summary from statistics
        
        Args:
            stats: Statistics dictionary
            
        Returns:
            Formatted text summary
        """
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║          AI STUDY FOCUS ANALYZER - SESSION REPORT            ║
╚══════════════════════════════════════════════════════════════╝

📊 SESSION OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Session Time:        {stats['total_time']:.1f} minutes
Average Focus Score:       {stats['avg_focus_score']:.1f}/100

⏱ TIME BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Productive Study:        {stats['productive_time']:.1f} minutes
📚 Educational Videos:      {stats['learning_time']:.1f} minutes
⚠ Distracted:              {stats['distracted_time']:.1f} minutes
😴 Fatigued:                {stats['fatigued_time']:.1f} minutes

📈 INSIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Peak focus time
        if stats['peak_focus_hour'] is not None:
            peak_time = f"{stats['peak_focus_hour']:02d}:00"
            summary += f"🌟 Peak Focus Time:        {peak_time}\n"
        
        # Lowest focus time
        if stats['lowest_focus_hour'] is not None:
            low_time = f"{stats['lowest_focus_hour']:02d}:00"
            summary += f"📉 Lowest Focus Time:      {low_time}\n"
        
        # Productivity percentage
        if stats['total_time'] > 0:
            productive_pct = ((stats['productive_time'] + stats['learning_time']) / 
                            stats['total_time'] * 100)
            summary += f"\n💯 Productivity Rate:      {productive_pct:.1f}%\n"
        
        summary += "\n" + "="*64 + "\n"
        
        return summary
    
    def generate_report(self, date: str = None) -> str:
        """
        Generate complete report for a date
        
        Args:
            date: Date string (YYYY-MM-DD), defaults to today
            
        Returns:
            Path to generated report directory
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Load data
        df = self.load_session_data(date)
        
        if df.empty:
            print(f"No data found for {date}")
            return None
        
        # Calculate statistics
        stats = self.calculate_statistics(df)
        
        # Create report directory
        report_dir = os.path.join(REPORTS_DIR, f"report_{date}")
        os.makedirs(report_dir, exist_ok=True)
        
        # Generate charts
        pie_path = os.path.join(report_dir, "activity_distribution.png")
        timeline_path = os.path.join(report_dir, "focus_timeline.png")
        hourly_path = os.path.join(report_dir, "hourly_focus.png")
        
        self.plot_activity_pie_chart(df, pie_path)
        self.plot_focus_timeline(df, timeline_path)
        self.plot_hourly_focus(df, hourly_path)
        
        # Generate text summary
        summary = self.generate_text_summary(stats)
        summary_path = os.path.join(report_dir, "summary.txt")
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        # Print summary
        print(summary)
        
        print(f"\n✓ Report generated: {report_dir}")
        print(f"  - {pie_path}")
        print(f"  - {timeline_path}")
        print(f"  - {hourly_path}")
        print(f"  - {summary_path}\n")
        
        return report_dir
