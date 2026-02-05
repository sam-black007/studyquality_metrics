"""
AI Study Focus & Screen Activity Analyzer
Main entry point for the application

Usage:
    python main.py              # Launch GUI
    python main.py --cli        # CLI mode (future)
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui import main as gui_main


def main():
    """Main entry point"""
    print("="*60)
    print("AI STUDY FOCUS & SCREEN ACTIVITY ANALYZER")
    print("="*60)
    print()
    print("Starting GUI application...")
    print()
    print("Controls:")
    print("  - Click 'Start Monitoring' to begin")
    print("  - Press Ctrl+P to pause/resume")
    print("  - Click 'Stop' to end session")
    print("  - Click 'Generate Report' to create daily summary")
    print()
    print("Privacy Notice:")
    print("  ✓ All processing is done locally")
    print("  ✓ No data leaves your computer")
    print("  ✓ Only analysis results are saved (no images)")
    print()
    print("="*60)
    print()
    
    # Launch GUI
    try:
        gui_main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nApplication closed.")


if __name__ == "__main__":
    main()
