# Uninstallation Guide

This guide shows you how to completely remove the AI Study Focus Monitor from your system.

---

## 🗑️ Complete Removal

### Step 1: Stop the Application

Make sure the app is not running:
- Close the dashboard window if open
- Check Task Manager (Windows) or Activity Monitor (Mac) for any running Python processes

---

### Step 2: Backup Your Data (Optional)

If you want to keep your study reports and session logs:

**Windows:**
```bash
# Copy to your Documents folder
xcopy "d:\test file\data" "%USERPROFILE%\Documents\StudyMonitorBackup" /E /I
```

**macOS/Linux:**
```bash
# Copy to your home directory
cp -r ~/study-focus-monitor/data ~/StudyMonitorBackup
```

Your important files:
- `data/sessions/*.csv` - Session logs
- `data/reports/` - All your daily reports with charts

---

### Step 3: Uninstall

#### Method A: Installed from GitHub Clone (Most Common)

Simply delete the project folder:

**Windows:**
```bash
# Using Command Prompt
cd "d:\"
rmdir /s /q "test file"
```

**Or use File Explorer:**
1. Navigate to `d:\test file`
2. Right-click → Delete
3. Confirm deletion

**macOS/Linux:**
```bash
rm -rf ~/study-focus-monitor
```

#### Method B: Installed via pip

```bash
pip uninstall study-focus-monitor
```

Type `y` to confirm.

---

### Step 4: Remove Dependencies (Optional)

If you don't need the Python libraries for other projects:

```bash
pip uninstall opencv-python mediapipe tensorflow-cpu numpy pandas matplotlib pillow mss pynput pyyaml scikit-learn scipy plotly
```

**Warning:** Only do this if you're sure these libraries aren't used by other Python projects!

---

### Step 5: Clean Up Git (If Applicable)

If you pushed to GitHub and want to remove the repository:

1. Go to https://github.com/sam-black007/studyquality_metrics
2. Click **Settings** (tab at top)
3. Scroll down to **Danger Zone**
4. Click **Delete this repository**
5. Type the repository name to confirm
6. Click **I understand the consequences, delete this repository**

**Note:** This is permanent and cannot be undone!

---

## ✅ Verification

After uninstallation, verify everything is removed:

**Windows:**
```bash
dir "d:\test file"
# Should show "File Not Found"
```

**macOS/Linux:**
```bash
ls ~/study-focus-monitor
# Should show "No such file or directory"
```

Check pip:
```bash
pip list | grep study-focus-monitor
# Should show nothing
```

---

## 🔄 Reinstallation

If you want to reinstall later:

```bash
git clone https://github.com/sam-black007/studyquality_metrics.git
cd studyquality_metrics
setup.bat  # or setup.sh
```

Your old data won't be restored unless you backed it up!

---

## 📊 What Gets Removed

✅ All application code
✅ Machine learning models
✅ Configuration files
✅ Session logs (unless backed up)
✅ Daily reports (unless backed up)
✅ Application logs

❌ Python installation (stays on your system)
❌ Other Python packages (unless manually removed)

---

## 🆘 Having Issues?

If you encounter problems during uninstallation:

1. **"Access Denied"** - Close all running instances of the app
2. **"File in Use"** - Restart your computer and try again
3. **Can't find the folder** - Check if it's in a different location

Still having issues? Contact support or open an issue on GitHub.

---

**Thank you for using AI Study Focus Monitor! 📚**

We hope it helped you stay focused and productive. Good luck with your studies!
