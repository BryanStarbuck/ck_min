# Changelog

## Version 1.1.0 - 2025-12-10

### Changed

**Default Model Quality**
- Changed default Whisper model from `base` to `large-v3` for maximum transcription accuracy
- Users now get the highest quality transcriptions by default
- Can still use faster models with `-m base` or `-m medium` flags

**Progress Output Behavior**
- Progress output is now **enabled by default** for better user feedback
- Shows detailed progress, file listings, and command execution details
- Added `--quiet` flag to disable progress output when not needed
- Removed `--verbose` flag (replaced with `--quiet` for clearer intent)

### Migration Guide

**Old Behavior → New Behavior**

Before (v1.0):
```bash
# Default was fast/lower quality
node script/transcribe.js              # Used 'base' model, no progress

# To see progress
node script/transcribe.js --verbose    # Showed progress

# For high quality
node script/transcribe.js -m large-v3  # Had to specify manually
```

After (v1.1):
```bash
# Default is high quality with progress
node script/transcribe.js              # Uses 'large-v3' model, shows progress

# To hide progress
node script/transcribe.js --quiet      # Hides detailed progress

# For faster processing
node script/transcribe.js -m base      # Use faster model explicitly
```

### Rationale

**Why Default to large-v3?**
- Charlie Kirk content requires high accuracy for proper transcription
- Users expect quality over speed for podcast/interview content
- Disk space and time are less constrained than quality
- Users can always opt-in to faster models when needed

**Why Enable Progress by Default?**
- Transcription can take significant time (especially with large-v3)
- Users need feedback to know the process is working
- Better user experience seeing what's happening
- Silent operation can be confusing for long-running tasks

### Updated Command Examples

```bash
# High quality with progress (default)
node script/transcribe.js

# High quality without progress details
node script/transcribe.js --quiet

# Fast processing with progress
node script/transcribe.js -m base

# Medium quality without progress
node script/transcribe.js -m medium --quiet

# Specific language for better accuracy
node script/transcribe.js -l en
```

### Performance Impact

Using `large-v3` by default will increase processing time:

| Model | 30-min Audio | Relative Speed | Quality |
|-------|--------------|----------------|---------|
| base | ~5 min | 1x (fastest) | Good |
| small | ~8 min | 1.6x | Better |
| medium | ~15 min | 3x | Great |
| **large-v3** | **~30 min** | **6x** | **Best** |

Users can override with `-m base` for faster processing when needed.

### Breaking Changes

⚠️ **`--verbose` flag removed**
- Replace `--verbose` with default behavior (no flag needed)
- Use `--quiet` if you don't want progress output

⚠️ **Default model changed**
- Transcriptions now take longer but are more accurate
- Use `-m base` to restore previous speed/quality tradeoff

### Files Changed

- `script/transcribe.js` - Updated configuration defaults and argument parsing
  - Changed `CONFIG.model` default from `'base'` to `'large-v3'`
  - Changed `verbose` flag to `showProgress` (default: true)
  - Updated `--verbose` to `--quiet` flag
  - Updated all references from 'verbose' type to 'progress' type
  - Updated help text and examples

### Backwards Compatibility

Scripts that explicitly set the model will continue to work:
```bash
node script/transcribe.js -m base     # Still works
node script/transcribe.js -m medium   # Still works
```

The only breaking change is the removal of `--verbose`, which can be addressed by removing the flag (since progress is now default).
