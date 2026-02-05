"""
Module 8: Live Dashboard

This module provides a real-time GUI showing:
- Current face attention state
- Screen content category
- Live focus score
- Session timer
- Pause/resume controls

Author: AI Study Focus Monitor
"""

import tkinter as tk
from tkinter import ttk
import logging
from datetime import datetime, timedelta
import threading
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import AttentionState, ContentCategory, format_duration

logger = logging.getLogger(__name__)


class Dashboard:
    """
    Real-time GUI dashboard for monitoring study focus.
    """
    
    def __init__(self, config: dict):
        """
        Initialize the dashboard.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.is_paused = False
        self.session_start_time = datetime.now()
        
        # Initialize main window
        self.root = tk.Tk()
        self.root.title("AI Study Focus Monitor")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Set color scheme
        self.bg_color = "#2c3e50"
        self.text_color = "#ecf0f1"
        self.root.configure(bg=self.bg_color)
        
        # State variables
        self.face_state_var = tk.StringVar(value="--")
        self.screen_type_var = tk.StringVar(value="--")
        self.focus_score_var = tk.StringVar(value="0")
        self.session_time_var = tk.StringVar(value="0m")
        self.status_var = tk.StringVar(value="Running")
        
        # Build UI
        self._build_ui()
        
        # Update timer
        self._update_timer()
        
        logger.info("Dashboard initialized")
    
    def _build_ui(self):
        """
        Build the dashboard UI components.
        """
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20, fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🎯 Study Focus Monitor",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title_label.pack()
        
        # Main info frame
        info_frame = tk.Frame(self.root, bg=self.bg_color)
        info_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)
        
        # Face State
        self._create_info_row(
            info_frame, 
            "👁 Face State:", 
            self.face_state_var,
            row=0
        )
        
        # Screen Type
        self._create_info_row(
            info_frame,
            "🖥 Screen Type:",
            self.screen_type_var,
            row=1
        )
        
        # Focus Score (larger, highlighted)
        score_frame = tk.Frame(info_frame, bg=self.bg_color)
        score_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        score_label = tk.Label(
            score_frame,
            text="🎯 Focus Score:",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        score_label.pack()
        
        self.score_display = tk.Label(
            score_frame,
            textvariable=self.focus_score_var,
            font=("Arial", 48, "bold"),
            bg=self.bg_color,
            fg="#2ecc71"  # Green
        )
        self.score_display.pack()
        
        # Session Timer
        self._create_info_row(
            info_frame,
            "⏱ Session Time:",
            self.session_time_var,
            row=3
        )
        
        # Status
        status_frame = tk.Frame(self.root, bg=self.bg_color)
        status_frame.pack(pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Arial", 12),
            bg=self.bg_color,
            fg="#2ecc71"
        )
        self.status_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=20)
        
        self.pause_button = tk.Button(
            button_frame,
            text="⏸ Pause",
            font=("Arial", 12, "bold"),
            bg="#f39c12",
            fg="white",
            activebackground="#e67e22",
            command=self.toggle_pause,
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        self.pause_button.pack(side=tk.LEFT, padx=10)
        
        end_button = tk.Button(
            button_frame,
            text="⏹ End Session",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            command=self.end_session,
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        end_button.pack(side=tk.LEFT, padx=10)
    
    def _create_info_row(self, parent, label_text, value_var, row):
        """
        Create a labeled information row.
        
        Args:
            parent: Parent widget
            label_text: Label text
            value_var: StringVar for the value
            row: Grid row number
        """
        label = tk.Label(
            parent,
            text=label_text,
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color,
            anchor=tk.W
        )
        label.grid(row=row, column=0, sticky=tk.W, pady=8)
        
        value = tk.Label(
            parent,
            textvariable=value_var,
            font=("Arial", 14, "bold"),
            bg=self.bg_color,
            fg="#3498db",
            anchor=tk.E
        )
        value.grid(row=row, column=1, sticky=tk.E, pady=8, padx=20)
    
    def _update_timer(self):
        """
        Update the session timer display.
        """
        if not self.is_paused:
            elapsed = datetime.now() - self.session_start_time
            elapsed_seconds = int(elapsed.total_seconds())
            self.session_time_var.set(format_duration(elapsed_seconds))
        
        # Schedule next update
        self.root.after(1000, self._update_timer)
    
    def update_display(
        self,
        face_state: AttentionState,
        screen_category: ContentCategory,
        focus_score: int
    ):
        """
        Update all display values.
        
        Args:
            face_state: Current face attention state
            screen_category: Current screen category
            focus_score: Current focus score (0-100)
        """
        # Update text values
        self.face_state_var.set(face_state.value)
        self.screen_type_var.set(screen_category.value)
        self.focus_score_var.set(str(focus_score))
        
        # Color code the score
        if focus_score >= 80:
            color = "#2ecc71"  # Green
        elif focus_score >= 50:
            color = "#f39c12"  # Orange
        else:
            color = "#e74c3c"  # Red
        
        self.score_display.configure(fg=color)
    
    def toggle_pause(self):
        """
        Toggle pause/resume state.
        """
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.pause_button.configure(text="▶ Resume", bg="#2ecc71")
            self.status_var.set("Paused")
            self.status_label.configure(fg="#f39c12")
            logger.info("Monitoring paused")
        else:
            self.pause_button.configure(text="⏸ Pause", bg="#f39c12")
            self.status_var.set("Running")
            self.status_label.configure(fg="#2ecc71")
            logger.info("Monitoring resumed")
    
    def end_session(self):
        """
        End the monitoring session and close the dashboard.
        """
        logger.info("Ending session...")
        self.root.quit()
        self.root.destroy()
    
    def is_paused_state(self) -> bool:
        """
        Check if monitoring is currently paused.
        
        Returns:
            True if paused, False otherwise
        """
        return self.is_paused
    
    def run(self):
        """
        Start the dashboard main loop (blocking).
        """
        logger.info("Dashboard running")
        self.root.mainloop()
    
    def run_async(self):
        """
        Run the dashboard in a separate thread (non-blocking).
        """
        dashboard_thread = threading.Thread(target=self.run, daemon=True)
        dashboard_thread.start()
        logger.info("Dashboard running in background thread")
        return dashboard_thread


def main():
    """
    Test the Dashboard module independently.
    """
    import time
    import random
    from utils.helpers import load_config
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load config
    config = load_config()
    
    # Initialize dashboard
    dashboard = Dashboard(config)
    
    # Simulate updates in a separate thread
    def simulate_updates():
        """Simulate real-time updates."""
        time.sleep(2)  # Wait for GUI to load
        
        states = [
            (AttentionState.FOCUSED, ContentCategory.STUDY, 95),
            (AttentionState.FOCUSED, ContentCategory.EDUCATIONAL_VIDEO, 85),
            (AttentionState.DISTRACTED, ContentCategory.SOCIAL_MEDIA, 20),
            (AttentionState.DROWSY, ContentCategory.STUDY, 40),
            (AttentionState.FOCUSED, ContentCategory.STUDY, 100),
        ]
        
        for face, screen, score in states:
            if not hasattr(dashboard.root, 'winfo_exists') or not dashboard.root.winfo_exists():
                break
            dashboard.update_display(face, screen, score)
            time.sleep(3)
    
    # Start simulation thread
    sim_thread = threading.Thread(target=simulate_updates, daemon=True)
    sim_thread.start()
    
    # Run dashboard (blocking)
    dashboard.run()


if __name__ == "__main__":
    main()
