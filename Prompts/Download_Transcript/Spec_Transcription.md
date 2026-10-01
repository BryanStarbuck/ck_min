Below is the entire spec formatted cleanly in Markdown, with all indentation preserved and easy to copy/paste.

# MP4/MP3 → Text Transcription CLI (JavaScript) – Spec

## 1. Goals

- Input: Local `.mp4` or `.mp3` file (podcast, long-form talking audio).
- Output: Text transcript (plain text and optionally JSON with timestamps).
- Run: From command line on **macOS** and **Windows**.
- Stack:
  - **JavaScript/TypeScript** for CLI and orchestration.
  - **Open-source transcription engine** installed via system package manager (preferred).
  - Optional: Call a **remote ASR API** when desired (fallback or “high accuracy” mode).

---

## 2. High-Level Architecture



User
|
v
JavaScript CLI (Node)

Parses CLI args (input file, output path, engine, language, model, etc.)

Validates file / environment

Branch:
A) Local Engine Mode (default)
B) External API Mode (optional)

Streams progress logs to console

Writes transcript to .txt / .json


Two main modes:

1. **Local Engine Mode**  
   - Uses a locally installed speech-to-text engine (e.g. Whisper).  
   - JS CLI shells out to the engine via `child_process`.

2. **API Mode (Optional)**  
   - JS CLI reads audio file, optionally converts to `.wav`/`.mp3`.  
   - Sends to ASR API.  
   - Receives transcript, writes to disk.

---

## 3. Technologies

### 3.1 Language & Runtime

- **Node.js** (LTS; e.g. 20.x)
- **TypeScript** recommended
- NPM/Yarn

### 3.2 JS Libraries

- CLI:
  - `commander` or `yargs`
  - `chalk` or `kleur`
  - `ora`
- System:
  - `child_process`
  - `fs`
  - `path`
- HTTP:
  - `axios` or native `fetch`

### 3.3 Local Transcription Engine (Open Source)

**Preferred Engine: OpenAI Whisper or whisper.cpp**

- macOS (Homebrew):



brew install ffmpeg
brew install whisper-cpp


- Windows:
- Install Node.js
- Install `ffmpeg` via Chocolatey:

  ```
  choco install ffmpeg
  ```

- Install whisper.cpp binaries manually or via package manager  
- Add whisper binary to PATH

### 3.4 Optional API Providers

- ASR APIs that accept MP3/MP4/WAV uploads
- Use `TRANSCRIBE_API_KEY` env variable

---

## 4. Command-Line Interface Design

### 4.1 CLI Command



podcast-transcribe [options] <inputFile>


### 4.2 Options

- `-o, --output <file>`  
  Output file (default: same name as input with `.txt`)

- `-e, --engine <engine>`  
  `local` (default) | `api`

- `-m, --model <modelName>`  
  Whisper model (e.g., `base`, `small`, `medium`, `large-v3`)

- `-l, --language <lang>`  
  Manual language override

- `--format <format>`  
  `txt` (default) | `json`

- `--api-url <url>`  
  Override default ASR endpoint

- `--api-key <key>`  
  Override env var

- `--tmp-dir <dir>`  
  Custom temp directory

- `--verbose`  
  Detailed logs

- `--dry-run`  
  Show commands but do not execute

### 4.3 Example Usage

**Local Whisper:**



podcast-transcribe episode1.mp4


**Local Whisper JSON:**



podcast-transcribe -m medium --format json episode1.mp3


**API mode:**



podcast-transcribe --engine api --api-url https://api.example.com/transcribe
 episode1.mp4


---

## 5. Workflow (Local Engine Mode)

### 5.1 Environment Setup

**macOS**



brew install ffmpeg
brew install whisper-cpp


**Windows**



choco install ffmpeg


Install whisper.cpp manually and place binaries in PATH.

### 5.2 Processing Steps

1. Validate input file  
2. Convert to wav if needed (using ffmpeg)  
3. Build whisper command-line call:



whisper -m ggml-medium.bin -f input.wav -of output


4. Spawn with `child_process.spawn`  
5. Read `.txt` or `.json` results  
6. Cleanup temp files  

---

## 6. Workflow (API Mode)

1. Validate API settings  
2. Convert audio to API-required format (mp3/wav)  
3. Upload audio via `axios` or `fetch` multipart/form-data  
4. Parse transcript JSON  
5. Write `.txt` or `.json` to output  
6. Handle rate limits/network errors  

---

## 7. File & Output Format

### 7.1 Text Output


Transcript
Source file: episode1.mp4
Engine: whisper (local)
Model: medium

[full transcript...]


### 7.2 JSON Output

```json
{
  "sourceFile": "episode1.mp4",
  "engine": "local-whisper",
  "model": "medium",
  "language": "en",
  "segments": [
    {
      "start": 0.0,
      "end": 5.2,
      "text": "Welcome to the podcast..."
    },
    {
      "start": 5.2,
      "end": 13.8,
      "text": "Today we'll be talking about..."
    }
  ]
}

8. Project Structure
project-root/
  package.json
  tsconfig.json
  src/
    cli.ts
    engines/
      index.ts
      localWhisper.ts
      apiEngine.ts
    utils/
      ffmpeg.ts
      file.ts
      logging.ts
  dist/
    cli.js

9. Error Handling & Edge Cases

Missing engine:

whisper binary not found. 
macOS: brew install whisper-cpp
Windows: install whisper.cpp and add to PATH


Unsupported formats → auto-convert via ffmpeg

Huge files → warn user

API upload limits → chunking future feature

10. Future Enhancements

Speaker diarization

Topic/chapter detection

AI summaries

Subtitle output (SRT/VTT)


---

If you want, I can now:

✅ Generate the **full TypeScript CLI code**  
✅ Generate **installation scripts for macOS & Windows**  
✅ Generate a **package.json** ready to publish to npm  

Just tell me what you want next.