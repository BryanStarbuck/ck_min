# Charlie Kirk Transcription Tool

Batch transcription tool for converting Charlie Kirk audio/video files to text using OpenAI's Whisper.

## Features

- ✅ Batch processing of multiple MP3/MP4 files
- ✅ Local Whisper engine (privacy-focused, no API calls)
- ✅ Cross-platform support (macOS & Windows)
- ✅ Multiple quality models (base, small, medium, large-v3)
- ✅ Automatic output organization
- ✅ Progress tracking and detailed logging
- ✅ Metadata headers in transcripts

## Prerequisites

### macOS

```bash
brew install ffmpeg
brew install whisper-cpp
```

Or install OpenAI's Whisper directly:

```bash
brew install ffmpeg
pip install openai-whisper
```

### Windows

```bash
choco install ffmpeg
```

Then install Whisper manually:
- Download whisper.cpp from https://github.com/ggerganov/whisper.cpp
- Or install via pip: `pip install openai-whisper`
- Ensure `whisper` is in your PATH

## Installation

No installation needed! Just run the script directly with Node.js.

```bash
cd ~/BGit/act3/charlie-kirk/Download_Transcript
node script/transcribe.js
```

## Usage

### Basic Usage

1. Place MP3 or MP4 files in the `to_transcribe/` directory
2. Run the transcription script:

```bash
node script/transcribe.js
```

3. Find transcripts in the `transcribed_out/` directory

### Advanced Usage

```bash
# Use a better quality model
node script/transcribe.js -m medium

# Enable verbose logging
node script/transcribe.js --verbose

# Specify custom directories
node script/transcribe.js -i ./my_audio -o ./my_transcripts

# Specify language (for better accuracy)
node script/transcribe.js -l en

# Dry run (see what would happen without executing)
node script/transcribe.js --dry-run

# Combine options
node script/transcribe.js -m large-v3 -l en --verbose
```

### Using NPM Scripts

```bash
# Basic transcription
npm run transcribe

# With verbose logging
npm run transcribe:verbose

# Using medium quality model
npm run transcribe:medium

# Using highest quality model
npm run transcribe:large

# Show help
npm run help
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input <dir>` | Input directory | `../to_transcribe` |
| `-o, --output <dir>` | Output directory | `../transcribed_out` |
| `-m, --model <model>` | Whisper model (base, small, medium, large-v3) | `base` |
| `-l, --language <lang>` | Language override (e.g., en, es, fr) | Auto-detect |
| `--verbose` | Enable verbose logging | `false` |
| `--dry-run` | Show what would be done without executing | `false` |
| `-h, --help` | Show help message | - |

## Whisper Models

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `base` | Fast | Good | Quick drafts, testing |
| `small` | Medium | Better | General use |
| `medium` | Slow | Great | High quality transcripts |
| `large-v3` | Very Slow | Best | Maximum accuracy |

## Output Format

Transcripts include metadata and are saved as `.txt` files:

```
Transcript
Source file: episode1.mp4
Engine: whisper (local)
Model: base
Transcribed: 2025-12-10T19:00:00.000Z

---

[Full transcript content here...]
```

## Directory Structure

```
Download_Transcript/
├── to_transcribe/          # Input: Place MP3/MP4 files here
├── transcribed_out/        # Output: Transcripts appear here
├── script/
│   └── transcribe.js       # Main transcription script
├── package.json            # NPM configuration
└── README.md              # This file
```

## Supported File Formats

- MP3 (.mp3)
- MP4 (.mp4)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)

## Troubleshooting

### "ffmpeg not found"

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```bash
choco install ffmpeg
```

### "Whisper not found"

**macOS:**
```bash
brew install whisper-cpp
# OR
pip install openai-whisper
```

**Windows:**
```bash
pip install openai-whisper
```

Make sure the `whisper` command is in your PATH.

### Transcription is slow

- Use a smaller model: `-m base` or `-m small`
- Consider using GPU acceleration (requires additional setup)
- Process files one at a time instead of batches

### Output file not found

The script expects Whisper to create files in the output directory. If you're using a custom Whisper installation, ensure it supports the `--output_dir` and `--output_format` flags.

## Performance Tips

1. **Start with base model**: Test with `-m base` first to ensure everything works
2. **Use medium for production**: `-m medium` offers a good balance
3. **Only use large-v3 when needed**: It's very slow but most accurate
4. **Process during off-hours**: Large models can take significant time
5. **Enable verbose mode**: Use `--verbose` to see detailed progress

## Example Workflow

```bash
# 1. Add files to transcribe
cp ~/Downloads/charlie_kirk_episode_*.mp3 to_transcribe/

# 2. Check what will be processed (dry run)
node script/transcribe.js --dry-run

# 3. Run transcription with medium quality
node script/transcribe.js -m medium --verbose

# 4. Check the output
ls -lh transcribed_out/

# 5. Read a transcript
cat transcribed_out/charlie_kirk_episode_123.txt
```

## Uses for Transcripts

Transcripts can be used for:

- Text search and analysis
- Quote extraction
- Topic breakdown
- Research notes
- Content classification

## License

MIT

## Support

For issues or questions, file an issue in the repository.
