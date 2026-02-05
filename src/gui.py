"""
GUI Dashboard for AI Study Focus Analyzer
Real-time monitoring interface with webcam feed and status display
"""
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
import numpy as np

from src.face_tracker import FaceTracker
from src.screen_eye import ScreenAnalyzer
from src.logic import FocusAnalyzer
from src.logger import SessionLogger
from src.reporter import ReportGenerator
from src.config import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    WEBCAM_DISPLAY_WIDTH, WEBCAM_DISPLAY_HEIGHT,
    CAPTURE_INTERVAL, LOG_INTERVAL
)


class FocusMonitorGUI:
    """
    Main GUI application for Focus Monitor
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        
        # Initialize components
        self.face_tracker = FaceTracker()
        self.screen_analyzer = ScreenAnalyzer()
        self.focus_analyzer = FocusAnalyzer()
        self.logger = SessionLogger()
        self.report_gen = ReportGenerator()
        
        # State
        self.is_running = False
        self.is_paused = False
        self.webcam = None
        self.monitoring_thread = None
        self.last_screen_capture_time = 0
        self.last_log_time = 0
        
        # Current analysis results
        self.current_face_state = "UNKNOWN"
        self.current_screen_class = "UNKNOWN"
        self.current_activity = "UNKNOWN"
        self.current_focus_score = 50
        self.current_score_label = "Fair"
        
        # Session stats
        self.session_start_time = None
        self.focus_score_history = []
        
        # Build UI
        self.build_ui()
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-p>', lambda e: self.toggle_pause())
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def build_ui(self):
        """Build the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left panel - Webcam feed
        left_panel = ttk.LabelFrame(main_frame, text="Webcam Feed", padding="10")
        left_panel.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.webcam_label = ttk.Label(left_panel)
        self.webcam_label.pack()
        
        # Right top panel - Status
        status_panel = ttk.LabelFrame(main_frame, text="Current Status", padding="10")
        status_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Status labels
        status_grid = ttk.Frame(status_panel)
        status_grid.pack(fill=tk.BOTH, expand=True)
        
        # Face State
        ttk.Label(status_grid, text="Face State:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.face_state_label = ttk.Label(status_grid, text="UNKNOWN", font=('Arial', 12))
        self.face_state_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Screen Content
        ttk.Label(status_grid, text="Screen Content:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        self.screen_class_label = ttk.Label(status_grid, text="UNKNOWN", font=('Arial', 12))
        self.screen_class_label.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Activity Status
        ttk.Label(status_grid, text="Activity:", font=('Arial', 10, 'bold')).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.activity_label = ttk.Label(status_grid, text="UNKNOWN", font=('Arial', 12))
        self.activity_label.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Focus Score
        ttk.Label(status_grid, text="Focus Score:", font=('Arial', 10, 'bold')).grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.focus_score_label = ttk.Label(status_grid, text="50 (Fair)", 
                                           font=('Arial', 16, 'bold'))
        self.focus_score_label.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Progress bar for focus score
        self.focus_progress = ttk.Progressbar(status_grid, length=300, mode='determinate')
        self.focus_progress.grid(row=4, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        self.focus_progress['maximum'] = 100
        self.focus_progress['value'] = 50
        
        # Right bottom panel - Controls and Stats
        control_panel = ttk.LabelFrame(main_frame, text="Controls & Statistics", padding="10")
        control_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons
        button_frame = ttk.Frame(control_panel)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="Start Monitoring", 
                                       command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="Pause (Ctrl+P)", 
                                       command=self.toggle_pause, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                      command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.report_button = ttk.Button(button_frame, text="Generate Report", 
                                        command=self.generate_report)
        self.report_button.pack(side=tk.LEFT, padx=5)
        
        # Session statistics
        stats_frame = ttk.Frame(control_panel)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(stats_frame, text="Session Statistics", 
                 font=('Arial', 11, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        self.session_time_label = ttk.Label(stats_frame, text="Session Time: 00:00:00")
        self.session_time_label.pack(anchor=tk.W, pady=2)
        
        self.productive_time_label = ttk.Label(stats_frame, text="Productive Time: 0 min")
        self.productive_time_label.pack(anchor=tk.W, pady=2)
        
        self.avg_score_label = ttk.Label(stats_frame, text="Avg Focus Score: 0")
        self.avg_score_label.pack(anchor=tk.W, pady=2)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def start_monitoring(self):
        """Start the monitoring process"""
        # Open webcam
        self.webcam = cv2.VideoCapture(0)
        
        if not self.webcam.isOpened():
            messagebox.showerror("Error", "Could not open webcam!")
            return
        
        self.is_running = True
        self.is_paused = False
        self.session_start_time = datetime.now()
        self.last_screen_capture_time = time.time()
        self.last_log_time = time.time()
        self.focus_score_history = []
        
        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.status_bar.config(text="Monitoring active...")
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        # Start UI update loop
        self.update_ui()
    
    def stop_monitoring(self):
        """Stop the monitoring process"""
        self.is_running = False
        
        # Wait for thread to finish
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        
        # Release webcam
        if self.webcam:
            self.webcam.release()
            self.webcam = None
        
        # Save session
        self.logger.save_session_json()
        
        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.status_bar.config(text="Monitoring stopped. Session saved.")
        
        messagebox.showinfo("Session Complete", "Monitoring stopped. Session data has been saved.")
    
    def toggle_pause(self):
        """Toggle pause state"""
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.pause_button.config(text="Resume")
            self.status_bar.config(text="Monitoring paused")
        else:
            self.pause_button.config(text="Pause (Ctrl+P)")
            self.status_bar.config(text="Monitoring active...")
    
    def monitoring_loop(self):
        """Main monitoring loop (runs in separate thread)"""
        while self.is_running:
            if self.is_paused:
                time.sleep(0.5)
                continue
            
            # Capture webcam frame
            ret, frame = self.webcam.read()
            if not ret:
                continue
            
            # Analyze face
            face_analysis = self.face_tracker.analyze_frame(frame)
            self.current_face_state = face_analysis['state']
            
            # Draw debug info on frame
            annotated_frame = self.face_tracker.draw_debug_info(frame, face_analysis)
            
            # Store frame for UI update
            self.current_frame = annotated_frame
            
            # Capture screen periodically
            current_time = time.time()
            if current_time - self.last_screen_capture_time >= CAPTURE_INTERVAL:
                screen_result = self.screen_analyzer.analyze()
                self.current_screen_class = screen_result['class']
                self.screen_confidence = screen_result['confidence']
                self.last_screen_capture_time = current_time
            
            # Analyze combined state
            analysis = self.focus_analyzer.analyze(
                self.current_face_state,
                self.current_screen_class,
                self.screen_confidence
            )
            
            self.current_activity = analysis['activity_status']
            self.current_focus_score = analysis['focus_score']
            self.current_score_label = analysis['score_label']
            
            # Track score history
            self.focus_score_history.append(self.current_focus_score)
            
            # Log periodically
            if current_time - self.last_log_time >= LOG_INTERVAL:
                self.logger.log_entry(analysis)
                self.last_log_time = current_time
            
            # Small delay
            time.sleep(0.1)
    
    def update_ui(self):
        """Update UI elements (runs in main thread)"""
        if not self.is_running:
            return
        
        # Update webcam display
        if hasattr(self, 'current_frame'):
            frame = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (WEBCAM_DISPLAY_WIDTH, WEBCAM_DISPLAY_HEIGHT))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.webcam_label.imgtk = imgtk
            self.webcam_label.configure(image=imgtk)
        
        # Update status labels
        self.face_state_label.config(text=self.current_face_state)
        self.screen_class_label.config(text=self.current_screen_class)
        self.activity_label.config(text=self.current_activity)
        
        # Update focus score
        score_text = f"{self.current_focus_score} ({self.current_score_label})"
        self.focus_score_label.config(text=score_text)
        self.focus_progress['value'] = self.current_focus_score
        
        # Color code based on score
        if self.current_focus_score >= 80:
            color = 'green'
        elif self.current_focus_score >= 60:
            color = 'blue'
        elif self.current_focus_score >= 40:
            color = 'orange'
        else:
            color = 'red'
        
        self.focus_score_label.config(foreground=color)
        
        # Update session stats
        if self.session_start_time:
            elapsed = datetime.now() - self.session_start_time
            hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            self.session_time_label.config(text=f"Session Time: {hours:02d}:{minutes:02d}:{seconds:02d}")
        
        stats = self.logger.get_session_stats()
        self.productive_time_label.config(text=f"Productive Time: {stats['productive_time']:.1f} min")
        self.avg_score_label.config(text=f"Avg Focus Score: {stats['avg_focus_score']:.1f}")
        
        # Schedule next update
        self.root.after(100, self.update_ui)
    
    def generate_report(self):
        """Generate productivity report"""
        report_dir = self.report_gen.generate_report()
        
        if report_dir:
            messagebox.showinfo("Report Generated", 
                              f"Report saved to:\n{report_dir}")
        else:
            messagebox.showwarning("No Data", 
                                 "No data available to generate report.")
    
    def on_closing(self):
        """Handle window close event"""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Monitoring is active. Stop and quit?"):
                self.stop_monitoring()
                self.cleanup()
                self.root.destroy()
        else:
            self.cleanup()
            self.root.destroy()
    
    def cleanup(self):
        """Clean up resources"""
        if self.webcam:
            self.webcam.release()
        
        self.face_tracker.release()
        self.screen_analyzer.close()


def main():
    """Main entry point for GUI"""
    root = tk.Tk()
    app = FocusMonitorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
