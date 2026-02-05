# 🚀 How to Publish on GitHub - Step by Step

This guide shows you exactly how to upload your Study Focus Monitor to GitHub so others can download and use it.

## Step 1: Create a GitHub Account

1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Choose a username (e.g., "yourname123")
4. Verify your email

## Step 2: Create a New Repository

1. Click the **+** icon in top-right → "New repository"
2. Fill in:
   - **Repository name**: `study-focus-monitor`
   - **Description**: "AI-powered study focus monitoring system using webcam and screen analysis"
   - **Public** (so anyone can download it)
   - ✅ Check "Add a README file"
   - Choose license: **MIT License**
3. Click **"Create repository"**

## Step 3: Upload Your Code

### Option A: Using GitHub Desktop (Easiest for Beginners)

1. **Download GitHub Desktop:**
   - Go to [desktop.github.com](https://desktop.github.com)
   - Install it on your computer

2. **Clone your repository:**
   - Open GitHub Desktop
   - File → Clone Repository
   - Choose `study-focus-monitor`
   - Select where to save it on your computer

3. **Copy your files:**
   - Copy all files from `d:\test file\` to the cloned folder
   - GitHub Desktop will show all the new files

4. **Commit and push:**
   - In GitHub Desktop, you'll see all the files
   - Write a commit message: "Initial commit - First version"
   - Click **"Commit to main"**
   - Click **"Push origin"**

### Option B: Using Git Command Line

```bash
cd "d:\test file"

# Initialize git (only first time)
git init
git add .
git commit -m "Initial commit - First version"

# Connect to GitHub (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/study-focus-monitor.git
git branch -M main
git push -u origin main
```

## Step 4: Verify Upload

1. Go to `https://github.com/yourusername/study-focus-monitor`
2. You should see all your files!

## Step 5: Make it Look Professional

### Add Badges to README

Edit your README.md on GitHub and add this at the top:

```markdown
# AI Study Focus Monitor

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
```

### Add GitHub Topics

1. Go to your repository
2. Click the ⚙️ settings icon near "About"
3. Add topics: `python`, `ai`, `productivity`, `study`, `focus`, `opencv`, `tensorflow`

## Step 6: Share with Users

Now users can install your app in 3 ways:

### Method 1: Clone and Setup (Easiest)

Users run:
```bash
git clone https://github.com/yourusername/study-focus-monitor.git
cd study-focus-monitor
setup.bat  # or setup.sh on Mac/Linux
```

### Method 2: Direct pip install

Users run:
```bash
pip install git+https://github.com/yourusername/study-focus-monitor.git
```

### Method 3: Download ZIP

1. GitHub shows a green **"Code"** button
2. Users click it → "Download ZIP"
3. Extract and run `setup.bat`

## Step 7: Create a Release (Optional but Recommended)

This makes it easier for users to download specific versions:

1. Go to your repository on GitHub
2. Click "Releases" (right sidebar) → "Create a new release"
3. Click "Choose a tag" → type `v1.0.0` → "Create new tag"
4. Release title: **"v1.0.0 - First Release"**
5. Description:
   ```markdown
   First stable release of AI Study Focus Monitor!
   
   ## Features
   - Real-time attention tracking
   - Screen content analysis
   - Focus scoring and reports
   - Privacy-focused (no cloud, local-only)
   
   ## Installation
   Run `setup.bat` (Windows) or `setup.sh` (Mac/Linux)
   
   See [QUICKSTART.md](QUICKSTART.md) for details.
   ```
6. Click **"Publish release"**

## Step 8: Share the Link!

Your project is now live at:
```
https://github.com/yourusername/study-focus-monitor
```

Share this link:
- 📧 Email to friends/classmates
- 💬 Social media
- 📱 WhatsApp/Discord groups
- 🎓 Student forums

## Bonus: Create a Standalone Executable

For users without Python:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Build executable:**
   ```bash
   pyinstaller --name="StudyFocusMonitor" --onefile --windowed main.py
   ```

3. **The executable will be in `dist/` folder**

4. **Zip it and upload to GitHub Release:**
   - Create a zip: `StudyFocusMonitor-Windows-v1.0.0.zip`
   - Go to your release page on GitHub
   - Click "Edit"
   - Drag & drop the zip file to attach it
   - Click "Update release"

Now users can download the `.exe` and run it without installing Python!

## Updating Your Code Later

When you make changes:

```bash
cd "d:\test file"
git add .
git commit -m "Describe what you changed"
git push
```

## Need Help?

- 📖 [GitHub Guides](https://guides.github.com/)
- 💬 Ask on [GitHub Community](https://github.community/)
- 📺 [YouTube: How to use GitHub](https://www.youtube.com/results?search_query=how+to+use+github+for+beginners)

---

## 🗑️ Uninstalling the App

If users want to remove the app, they can find complete instructions in [UNINSTALL.md](UNINSTALL.md).

**Quick removal:**
- Just delete the project folder (if cloned)
- Or run `pip uninstall study-focus-monitor` (if installed via pip)

**To delete from GitHub:**
1. Go to repository Settings
2. Scroll to "Danger Zone"
3. Click "Delete this repository"

---

**Congratulations! Your project is now on GitHub and ready for the world to use! 🎉**
