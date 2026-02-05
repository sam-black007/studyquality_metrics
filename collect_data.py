"""
Data Collection Tool for Screen Classification
Helps user build a training dataset by capturing labeled screenshots
"""
import os
import time
import mss
from PIL import Image
from datetime import datetime
from src.config import TRAINING_DATA_DIR, SCREEN_CLASSES, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT


def create_directories():
    """Create directory structure for training data"""
    for class_name in SCREEN_CLASSES:
        class_dir = os.path.join(TRAINING_DATA_DIR, class_name)
        os.makedirs(class_dir, exist_ok=True)
    print(f"Created directories in: {TRAINING_DATA_DIR}")


def collect_samples(class_name: str, num_samples: int = 50, interval: float = 3.0):
    """
    Collect screenshot samples for a specific class
    
    Args:
        class_name: Name of the class (must be in SCREEN_CLASSES)
        num_samples: Number of screenshots to collect
        interval: Seconds between captures
    """
    if class_name not in SCREEN_CLASSES:
        print(f"Error: '{class_name}' not in valid classes: {SCREEN_CLASSES}")
        return
    
    class_dir = os.path.join(TRAINING_DATA_DIR, class_name)
    
    print(f"\n{'='*60}")
    print(f"Collecting {num_samples} samples for class: {class_name}")
    print(f"{'='*60}")
    print(f"Instructions:")
    print(f"  1. Open windows/apps that represent '{class_name}'")
    print(f"  2. Switch between different examples")
    print(f"  3. Screenshots will be taken every {interval} seconds")
    print(f"\nStarting in 5 seconds... Get ready!")
    print(f"{'='*60}\n")
    
    time.sleep(5)
    
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        
        for i in range(num_samples):
            # Capture
            screenshot = sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # Resize
            img = img.resize((SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT), Image.Resampling.LANCZOS)
            
            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{class_name}_{timestamp}_{i:03d}.png"
            filepath = os.path.join(class_dir, filename)
            img.save(filepath)
            
            print(f"[{i+1}/{num_samples}] Captured: {filename}")
            
            # Wait for next capture
            if i < num_samples - 1:
                time.sleep(interval)
    
    print(f"\n✓ Completed! Saved {num_samples} samples to: {class_dir}\n")


def interactive_collection():
    """Interactive mode for collecting data"""
    create_directories()
    
    print("\n" + "="*60)
    print("SCREEN CLASSIFICATION DATA COLLECTION TOOL")
    print("="*60)
    print("\nAvailable classes:")
    for i, cls in enumerate(SCREEN_CLASSES, 1):
        print(f"  {i}. {cls}")
    
    print("\nRecommended samples per class: 50-100")
    print("More diverse samples = better model accuracy")
    print("="*60 + "\n")
    
    while True:
        print("\nOptions:")
        print("  1. Collect samples for a class")
        print("  2. View current dataset stats")
        print("  3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            print("\nSelect class:")
            for i, cls in enumerate(SCREEN_CLASSES, 1):
                print(f"  {i}. {cls}")
            
            class_choice = input(f"\nEnter class number (1-{len(SCREEN_CLASSES)}): ").strip()
            
            try:
                class_idx = int(class_choice) - 1
                if 0 <= class_idx < len(SCREEN_CLASSES):
                    class_name = SCREEN_CLASSES[class_idx]
                    
                    num_samples = input("Number of samples to collect (default 50): ").strip()
                    num_samples = int(num_samples) if num_samples else 50
                    
                    interval = input("Interval between captures in seconds (default 3): ").strip()
                    interval = float(interval) if interval else 3.0
                    
                    collect_samples(class_name, num_samples, interval)
                else:
                    print("Invalid class number!")
            except ValueError:
                print("Invalid input!")
        
        elif choice == "2":
            print("\n" + "="*60)
            print("DATASET STATISTICS")
            print("="*60)
            
            total = 0
            for cls in SCREEN_CLASSES:
                class_dir = os.path.join(TRAINING_DATA_DIR, cls)
                if os.path.exists(class_dir):
                    count = len([f for f in os.listdir(class_dir) if f.endswith('.png')])
                    print(f"  {cls:20s}: {count:4d} samples")
                    total += count
                else:
                    print(f"  {cls:20s}:    0 samples")
            
            print("="*60)
            print(f"  {'TOTAL':20s}: {total:4d} samples")
            print("="*60 + "\n")
        
        elif choice == "3":
            print("\nExiting data collection tool.")
            break
        
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    interactive_collection()
