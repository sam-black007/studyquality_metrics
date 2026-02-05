"""
Model Training Script for Screen Classification
Trains a MobileNetV2 model on collected screenshot data
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from datetime import datetime

from src.config import (
    TRAINING_DATA_DIR, MODELS_DIR, SCREEN_CLASSIFIER_MODEL,
    SCREEN_CLASSES, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT,
    BATCH_SIZE, EPOCHS, VALIDATION_SPLIT, LEARNING_RATE,
    USE_DATA_AUGMENTATION, ROTATION_RANGE, WIDTH_SHIFT_RANGE,
    HEIGHT_SHIFT_RANGE, HORIZONTAL_FLIP, REPORTS_DIR
)


def check_dataset():
    """Check if dataset exists and has sufficient samples"""
    if not os.path.exists(TRAINING_DATA_DIR):
        print(f"Error: Training data directory not found: {TRAINING_DATA_DIR}")
        print("Please run collect_data.py first to collect training samples.")
        return False
    
    print("\n" + "="*60)
    print("DATASET CHECK")
    print("="*60)
    
    total_samples = 0
    class_counts = {}
    
    for cls in SCREEN_CLASSES:
        class_dir = os.path.join(TRAINING_DATA_DIR, cls)
        if os.path.exists(class_dir):
            count = len([f for f in os.listdir(class_dir) if f.endswith('.png')])
            class_counts[cls] = count
            total_samples += count
            print(f"  {cls:20s}: {count:4d} samples")
        else:
            class_counts[cls] = 0
            print(f"  {cls:20s}:    0 samples (WARNING: No data!)")
    
    print("="*60)
    print(f"  {'TOTAL':20s}: {total_samples:4d} samples")
    print("="*60 + "\n")
    
    if total_samples < 50:
        print("⚠ Warning: Very few samples. Recommend at least 50 per class.")
        print("The model may not train well with limited data.")
        return False
    
    if any(count == 0 for count in class_counts.values()):
        print("⚠ Warning: Some classes have no samples!")
        print("Consider collecting data for all classes.")
    
    return True


def create_model(num_classes: int) -> keras.Model:
    """
    Create MobileNetV2-based transfer learning model
    
    Args:
        num_classes: Number of output classes
        
    Returns:
        Compiled Keras model
    """
    # Load pre-trained MobileNetV2 (without top classification layer)
    base_model = MobileNetV2(
        input_shape=(SCREENSHOT_HEIGHT, SCREENSHOT_WIDTH, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Build model
    inputs = keras.Input(shape=(SCREENSHOT_HEIGHT, SCREENSHOT_WIDTH, 3))
    
    # Preprocessing
    x = layers.Rescaling(1./255)(inputs)
    
    # Base model
    x = base_model(x, training=False)
    
    # Classification head
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = keras.Model(inputs, outputs)
    
    # Compile
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model


def create_data_generators():
    """Create training and validation data generators"""
    
    if USE_DATA_AUGMENTATION:
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=ROTATION_RANGE,
            width_shift_range=WIDTH_SHIFT_RANGE,
            height_shift_range=HEIGHT_SHIFT_RANGE,
            horizontal_flip=HORIZONTAL_FLIP,
            validation_split=VALIDATION_SPLIT
        )
    else:
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=VALIDATION_SPLIT
        )
    
    train_generator = train_datagen.flow_from_directory(
        TRAINING_DATA_DIR,
        target_size=(SCREENSHOT_HEIGHT, SCREENSHOT_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    val_generator = train_datagen.flow_from_directory(
        TRAINING_DATA_DIR,
        target_size=(SCREENSHOT_HEIGHT, SCREENSHOT_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    return train_generator, val_generator


def plot_training_history(history, save_path: str):
    """Plot and save training history"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Accuracy
    ax1.plot(history.history['accuracy'], label='Train Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Loss
    ax2.plot(history.history['loss'], label='Train Loss')
    ax2.plot(history.history['val_loss'], label='Val Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=100, bbox_inches='tight')
    print(f"Training history plot saved to: {save_path}")


def train_model():
    """Main training function"""
    print("\n" + "="*60)
    print("SCREEN CLASSIFIER MODEL TRAINING")
    print("="*60 + "\n")
    
    # Check dataset
    if not check_dataset():
        response = input("\nDataset has issues. Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            print("Training cancelled.")
            return
    
    # Create directories
    os.makedirs(MODELS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # Create data generators
    print("Creating data generators...")
    train_gen, val_gen = create_data_generators()
    
    num_classes = len(train_gen.class_indices)
    print(f"\nNumber of classes: {num_classes}")
    print(f"Class mapping: {train_gen.class_indices}")
    print(f"Training samples: {train_gen.samples}")
    print(f"Validation samples: {val_gen.samples}")
    
    # Create model
    print("\nCreating MobileNetV2 model...")
    model = create_model(num_classes)
    
    print("\nModel architecture:")
    model.summary()
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7
        )
    ]
    
    # Train
    print(f"\n{'='*60}")
    print("TRAINING STARTED")
    print(f"{'='*60}\n")
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save model
    model.save(SCREEN_CLASSIFIER_MODEL)
    print(f"\n✓ Model saved to: {SCREEN_CLASSIFIER_MODEL}")
    
    # Plot training history
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = os.path.join(REPORTS_DIR, f"training_history_{timestamp}.png")
    plot_training_history(history, plot_path)
    
    # Final evaluation
    print(f"\n{'='*60}")
    print("FINAL EVALUATION")
    print(f"{'='*60}")
    
    val_loss, val_acc = model.evaluate(val_gen, verbose=0)
    print(f"Validation Loss: {val_loss:.4f}")
    print(f"Validation Accuracy: {val_acc:.4f}")
    print(f"{'='*60}\n")
    
    print("✓ Training complete!")
    print(f"You can now run main.py to use the trained model.\n")


if __name__ == "__main__":
    train_model()
