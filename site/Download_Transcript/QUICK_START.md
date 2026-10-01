# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (One Time)

**On macOS:**
```bash
brew install ffmpeg
brew install whisper-cpp
```

**On Windows:**
```bash
choco install ffmpeg
pip install openai-whisper
```

### Step 2: Add Files

Place your MP3 or MP4 files in the `to_transcribe/` folder:

```bash
cp /path/to/your/audio.mp3 ~/BGit/act3/charlie-kirk/Download_Transcript/to_transcribe/
```

### Step 3: Run Transcription

```bash
cd ~/BGit/act3/charlie-kirk/Download_Transcript
node script/transcribe.js
```

### Step 4: Get Results

Your transcripts will be in `transcribed_out/` with the same filename but `.txt` extension.

---

## Quick Commands

```bash
# Basic (fast, lower quality)
node script/transcribe.js

# Medium quality (recommended)
node script/transcribe.js -m medium

# High quality (slow but accurate)
node script/transcribe.js -m large-v3

# See progress details
node script/transcribe.js --verbose

# Test without running
node script/transcribe.js --dry-run
```

---

## Troubleshooting

**Problem:** "whisper not found"
**Solution:**
```bash
# macOS
brew install whisper-cpp

# Windows/macOS alternative
pip install openai-whisper
```

**Problem:** "ffmpeg not found"
**Solution:**
```bash
# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

**Problem:** Script won't run
**Solution:**
```bash
# Make sure you're in the right directory
cd ~/BGit/act3/charlie-kirk/Download_Transcript

# Make script executable (macOS/Linux)
chmod +x script/transcribe.js

# Run with node explicitly
node script/transcribe.js
```

---

## That's It!

For more options and details, see the full [README.md](README.md).

## Common Use Cases

### Transcribe a single file quickly
```bash
# Move one file to to_transcribe/
cp ~/Downloads/interview.mp3 to_transcribe/
# Run with basic model
node script/transcribe.js
```

### Batch transcribe multiple files with good quality
```bash
# Move multiple files
cp ~/Downloads/charlie_kirk_*.mp3 to_transcribe/
# Run with medium model
node script/transcribe.js -m medium --verbose
```

### Process and archive
```bash
# Transcribe
node script/transcribe.js -m medium

# Move transcripts to archive
mkdir -p archive/$(date +%Y-%m-%d)
mv transcribed_out/* archive/$(date +%Y-%m-%d)/

# Clean input folder
rm to_transcribe/*
```
