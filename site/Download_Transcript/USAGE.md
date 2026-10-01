# Quick Usage Reference

## Default Behavior (v1.1+)

```bash
node script/transcribe.js
```

**Defaults:**
- ✅ Model: `large-v3` (highest quality, slower)
- ✅ Progress: ON (shows detailed progress)
- ✅ Input: `to_transcribe/` directory
- ✅ Output: `transcribed_out/` directory

---

## Common Use Cases

### 1. High Quality (Default)
```bash
# Just run it - uses large-v3 with progress
node script/transcribe.js
```
⏱️ ~30 minutes for 30-min audio

### 2. Medium Quality (Recommended for Testing)
```bash
# Good balance of speed and quality
node script/transcribe.js -m medium
```
⏱️ ~15 minutes for 30-min audio

### 3. Fast Processing
```bash
# Quick transcription for drafts
node script/transcribe.js -m base
```
⏱️ ~5 minutes for 30-min audio

### 4. Quiet Mode (No Progress)
```bash
# Run silently (useful for scripts/automation)
node script/transcribe.js --quiet
```

### 5. Custom Directories
```bash
# Specify different input/output locations
node script/transcribe.js -i ~/Downloads/audio -o ~/Documents/transcripts
```

### 6. Specific Language
```bash
# Improve accuracy by specifying language
node script/transcribe.js -l en
```

### 7. Combination
```bash
# Medium quality, English, quiet mode
node script/transcribe.js -m medium -l en --quiet
```

---

## Model Comparison

| Model | Speed | Quality | When to Use |
|-------|-------|---------|-------------|
| `base` | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | Quick drafts, testing |
| `small` | ⚡⚡ Medium | ⭐⭐⭐⭐ Better | General use, faster turnaround |
| `medium` | ⚡ Slow | ⭐⭐⭐⭐⭐ Great | Recommended for production |
| `large-v3` | 🐌 Very Slow | ⭐⭐⭐⭐⭐⭐ Best | **Default - Maximum accuracy** |

---

## Workflow Examples

### Quick Test
```bash
# Add one small file, test with base model
cp ~/Downloads/short_clip.mp3 to_transcribe/
node script/transcribe.js -m base
```

### Production Batch
```bash
# Add all podcast episodes, use default high quality
cp ~/Downloads/charlie_kirk_*.mp3 to_transcribe/
node script/transcribe.js
# Wait for high-quality transcriptions...
```

### Overnight Processing
```bash
# Queue up many files, run overnight with quiet mode
cp ~/Podcasts/*.mp3 to_transcribe/
nohup node script/transcribe.js --quiet > transcribe.log 2>&1 &
# Check progress: tail -f transcribe.log
```

### Archive Workflow
```bash
# Transcribe and archive in one go
node script/transcribe.js -m medium
mkdir -p archive/$(date +%Y-%m-%d)
mv transcribed_out/* archive/$(date +%Y-%m-%d)/
rm to_transcribe/*
```

---

## Flags Reference

| Flag | Description | Default |
|------|-------------|---------|
| `-i <dir>` | Input directory | `to_transcribe/` |
| `-o <dir>` | Output directory | `transcribed_out/` |
| `-m <model>` | Whisper model | `large-v3` |
| `-l <lang>` | Language code (en, es, fr, etc.) | Auto-detect |
| `--quiet` | Disable progress output | OFF (progress shown) |
| `--dry-run` | Test without executing | OFF |
| `-h, --help` | Show help | - |

---

## Tips

💡 **First time?** Test with a small file and `-m base` to verify everything works

💡 **Batch processing?** Use default `large-v3` and let it run overnight

💡 **Need speed?** Use `-m medium` for 3x faster processing with great quality

💡 **Automation?** Add `--quiet` to reduce output noise in logs

💡 **Quality issues?** Specify language with `-l en` for better accuracy

💡 **Long files?** Progress output helps you know it's still working

---

## Output Format

Each transcript includes metadata:

```
Transcript
Source file: episode_123.mp3
Engine: whisper (local)
Model: large-v3
Transcribed: 2025-12-10T20:00:00.000Z

---

[Full transcript text here...]
```

---

## NPM Scripts (Alternative)

```bash
# If you prefer npm commands
npm run transcribe          # Default (large-v3, progress)
npm run transcribe:medium   # Medium quality
npm run help               # Show help
```

---

## Troubleshooting

**Script runs but no progress?**
- Progress is ON by default now
- Check that you didn't use `--quiet`

**Too slow?**
- Use faster model: `-m base` or `-m medium`
- Default is now `large-v3` (slowest but best)

**Missing dependencies?**
```bash
brew install ffmpeg whisper-cpp
```

---

**Version:** 1.1.0
**Last Updated:** 2025-12-10
