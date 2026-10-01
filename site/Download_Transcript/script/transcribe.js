#!/usr/bin/env node

/**
 * MP3/MP4 → Text Transcription CLI
 *
 * Transcribes audio/video files using local Whisper engine
 * Works on macOS and Windows
 *
 * Prerequisites:
 *   macOS: brew install ffmpeg whisper-cpp
 *   Windows: choco install ffmpeg, install whisper.cpp manually
 *
 * Usage:
 *   node transcribe.js [options]
 *
 * Options:
 *   -i, --input <dir>     Input directory (default: ../to_transcribe)
 *   -o, --output <dir>    Output directory (default: ../transcribed_out)
 *   -m, --model <model>   Whisper model (base, small, medium, large-v3) (default: large-v3)
 *   -l, --language <lang> Language override (e.g., en, es, fr)
 *   --quiet               Disable progress output (progress shown by default)
 *   --dry-run             Show what would be done without executing
 *   -h, --help            Show help
 */

const fs = require('fs');
const path = require('path');
const { spawn, execSync } = require('child_process');
const os = require('os');

// Configuration
const CONFIG = {
  inputDir: null,
  outputDir: null,
  model: 'large-v3',
  language: null,
  showProgress: true,
  dryRun: false,
  whisperCommand: 'whisper',
  ffmpegCommand: 'ffmpeg',
  supportedExtensions: ['.mp3', '.mp4', '.wav', '.m4a', '.ogg']
};

// ANSI color codes for better CLI output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

function log(message, type = 'info') {
  const timestamp = new Date().toISOString();
  const prefix = {
    info: `${colors.blue}ℹ${colors.reset}`,
    success: `${colors.green}✓${colors.reset}`,
    error: `${colors.red}✗${colors.reset}`,
    warn: `${colors.yellow}⚠${colors.reset}`,
    progress: `${colors.cyan}→${colors.reset}`
  }[type] || '';

  // Always show info, success, error, and warn
  if (type !== 'progress') {
    console.log(`${prefix} ${message}`);
  } else if (CONFIG.showProgress) {
    // Only show progress messages if showProgress is enabled
    console.log(`${prefix} ${message}`);
  }
}

function printHelp() {
  console.log(`
${colors.bright}MP3/MP4 → Text Transcription CLI${colors.reset}

${colors.cyan}Usage:${colors.reset}
  node transcribe.js [options]

${colors.cyan}Options:${colors.reset}
  -i, --input <dir>     Input directory (default: ../to_transcribe)
  -o, --output <dir>    Output directory (default: ../transcribed_out)
  -m, --model <model>   Whisper model: base, small, medium, large-v3 (default: large-v3)
  -l, --language <lang> Language override (e.g., en, es, fr)
  --quiet               Disable progress output (progress is shown by default)
  --dry-run             Show what would be done without executing
  -h, --help            Show this help message

${colors.cyan}Examples:${colors.reset}
  node transcribe.js
  node transcribe.js -m medium
  node transcribe.js -i ./audio -o ./transcripts --quiet
  node transcribe.js -m base -l en

${colors.cyan}Prerequisites:${colors.reset}
  ${colors.yellow}macOS:${colors.reset}
    brew install ffmpeg
    brew install whisper-cpp

  ${colors.yellow}Windows:${colors.reset}
    choco install ffmpeg
    Install whisper.cpp manually and add to PATH
`);
}

function parseArgs() {
  const args = process.argv.slice(2);

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    switch (arg) {
      case '-h':
      case '--help':
        printHelp();
        process.exit(0);
        break;

      case '-i':
      case '--input':
        CONFIG.inputDir = args[++i];
        break;

      case '-o':
      case '--output':
        CONFIG.outputDir = args[++i];
        break;

      case '-m':
      case '--model':
        CONFIG.model = args[++i];
        break;

      case '-l':
      case '--language':
        CONFIG.language = args[++i];
        break;

      case '--quiet':
        CONFIG.showProgress = false;
        break;

      case '--dry-run':
        CONFIG.dryRun = true;
        break;

      default:
        log(`Unknown option: ${arg}`, 'warn');
    }
  }

  // Set default directories relative to script location
  const scriptDir = __dirname;
  CONFIG.inputDir = CONFIG.inputDir || path.resolve(scriptDir, '../to_transcribe');
  CONFIG.outputDir = CONFIG.outputDir || path.resolve(scriptDir, '../transcribed_out');
}

function checkDependencies() {
  log('Checking dependencies...', 'info');

  const isWindows = os.platform() === 'win32';

  // Check for ffmpeg
  try {
    execSync(`${CONFIG.ffmpegCommand} -version`, { stdio: 'pipe' });
    log('✓ ffmpeg found', 'success');
  } catch (error) {
    log('ffmpeg not found!', 'error');
    if (isWindows) {
      log('Install with: choco install ffmpeg', 'error');
    } else {
      log('Install with: brew install ffmpeg', 'error');
    }
    return false;
  }

  // Check for whisper
  try {
    // Try whisper-cpp first (common on homebrew)
    try {
      execSync('whisper-cpp --help', { stdio: 'pipe' });
      CONFIG.whisperCommand = 'whisper-cpp';
      log('✓ whisper-cpp found', 'success');
    } catch (e) {
      // Try standard whisper
      execSync('whisper --help', { stdio: 'pipe' });
      CONFIG.whisperCommand = 'whisper';
      log('✓ whisper found', 'success');
    }
  } catch (error) {
    log('Whisper not found!', 'error');
    if (isWindows) {
      log('Install whisper.cpp and add to PATH', 'error');
    } else {
      log('Install with: brew install whisper-cpp', 'error');
    }
    return false;
  }

  return true;
}

function ensureDirectories() {
  log('Checking directories...', 'info');

  if (!fs.existsSync(CONFIG.inputDir)) {
    log(`Creating input directory: ${CONFIG.inputDir}`, 'warn');
    fs.mkdirSync(CONFIG.inputDir, { recursive: true });
  }

  if (!fs.existsSync(CONFIG.outputDir)) {
    log(`Creating output directory: ${CONFIG.outputDir}`, 'warn');
    fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  }

  log(`Input directory: ${CONFIG.inputDir}`, 'progress');
  log(`Output directory: ${CONFIG.outputDir}`, 'progress');
}

function getAudioFiles() {
  log('Scanning for audio/video files...', 'info');

  const files = fs.readdirSync(CONFIG.inputDir);
  const audioFiles = files.filter(file => {
    const ext = path.extname(file).toLowerCase();
    return CONFIG.supportedExtensions.includes(ext);
  });

  log(`Found ${audioFiles.length} file(s) to process`, 'info');

  if (CONFIG.showProgress) {
    audioFiles.forEach(file => log(`  - ${file}`, 'progress'));
  }

  return audioFiles;
}

function transcribeFile(inputFile) {
  return new Promise((resolve, reject) => {
    const inputPath = path.join(CONFIG.inputDir, inputFile);
    const baseName = path.basename(inputFile, path.extname(inputFile));
    const outputPath = path.join(CONFIG.outputDir, `${baseName}.txt`);

    log(`\n${colors.bright}Processing: ${inputFile}${colors.reset}`, 'info');

    if (CONFIG.dryRun) {
      log('Dry run - skipping actual transcription', 'warn');
      log(`Would transcribe: ${inputPath}`, 'info');
      log(`Output would be: ${outputPath}`, 'info');
      resolve({ inputFile, success: true, dryRun: true });
      return;
    }

    // Build whisper command
    // whisper model options depend on the implementation
    // For whisper-cpp: whisper -m model.bin -f file.wav
    // For OpenAI whisper: whisper file.mp3 --model base --output_dir dir

    const args = [inputPath];

    // Add model if specified
    if (CONFIG.model) {
      args.push('--model', CONFIG.model);
    }

    // Add language if specified
    if (CONFIG.language) {
      args.push('--language', CONFIG.language);
    }

    // Output format and directory
    args.push('--output_format', 'txt');
    args.push('--output_dir', CONFIG.outputDir);

    log(`Command: ${CONFIG.whisperCommand} ${args.join(' ')}`, 'progress');

    const startTime = Date.now();
    const whisperProcess = spawn(CONFIG.whisperCommand, args);

    let stdout = '';
    let stderr = '';

    whisperProcess.stdout.on('data', (data) => {
      stdout += data.toString();
      if (CONFIG.showProgress) {
        process.stdout.write(data);
      } else {
        // Show progress dots even when quiet
        process.stdout.write('.');
      }
    });

    whisperProcess.stderr.on('data', (data) => {
      stderr += data.toString();
      if (CONFIG.showProgress) {
        process.stderr.write(data);
      }
    });

    whisperProcess.on('close', (code) => {
      const duration = ((Date.now() - startTime) / 1000).toFixed(2);

      if (!CONFIG.showProgress) {
        process.stdout.write('\n');
      }

      if (code === 0) {
        // Check if output file was created
        // Whisper might create a file with a slightly different name
        const possibleOutputs = [
          outputPath,
          path.join(CONFIG.outputDir, `${baseName}.txt`),
          path.join(CONFIG.outputDir, `${path.basename(inputFile)}.txt`)
        ];

        let outputExists = false;
        let actualOutput = '';

        for (const possiblePath of possibleOutputs) {
          if (fs.existsSync(possiblePath)) {
            outputExists = true;
            actualOutput = possiblePath;
            break;
          }
        }

        if (outputExists) {
          const stats = fs.statSync(actualOutput);
          log(`✓ Transcription complete in ${duration}s`, 'success');
          log(`  Output: ${actualOutput}`, 'success');
          log(`  Size: ${(stats.size / 1024).toFixed(2)} KB`, 'progress');

          // Add metadata header to the output file
          const originalContent = fs.readFileSync(actualOutput, 'utf8');
          const metadata = `Transcript
Source file: ${inputFile}
Engine: whisper (local)
Model: ${CONFIG.model}
Transcribed: ${new Date().toISOString()}

---

${originalContent}`;

          fs.writeFileSync(actualOutput, metadata, 'utf8');

          resolve({ inputFile, success: true, outputPath: actualOutput, duration });
        } else {
          log(`✗ Transcription completed but output file not found`, 'error');
          log(`  Expected: ${outputPath}`, 'error');
          reject(new Error('Output file not created'));
        }
      } else {
        log(`✗ Transcription failed (exit code ${code})`, 'error');
        if (stderr) {
          log(`Error: ${stderr}`, 'error');
        }
        reject(new Error(`Whisper process exited with code ${code}`));
      }
    });

    whisperProcess.on('error', (error) => {
      log(`✗ Failed to start transcription: ${error.message}`, 'error');
      reject(error);
    });
  });
}

async function processAllFiles() {
  const audioFiles = getAudioFiles();

  if (audioFiles.length === 0) {
    log('No audio/video files found to process', 'warn');
    log(`Place MP3 or MP4 files in: ${CONFIG.inputDir}`, 'info');
    return;
  }

  const results = [];
  let successCount = 0;
  let failCount = 0;

  for (const file of audioFiles) {
    try {
      const result = await transcribeFile(file);
      results.push(result);
      successCount++;
    } catch (error) {
      log(`Failed to process ${file}: ${error.message}`, 'error');
      results.push({ inputFile: file, success: false, error: error.message });
      failCount++;
    }
  }

  // Print summary
  log('\n' + '='.repeat(60), 'info');
  log(`${colors.bright}Transcription Summary${colors.reset}`, 'info');
  log('='.repeat(60), 'info');
  log(`Total files: ${audioFiles.length}`, 'info');
  log(`${colors.green}Successful: ${successCount}${colors.reset}`, 'success');
  if (failCount > 0) {
    log(`${colors.red}Failed: ${failCount}${colors.reset}`, 'error');
  }
  log('='.repeat(60), 'info');

  if (CONFIG.showProgress) {
    console.log('\nDetailed results:');
    console.log(JSON.stringify(results, null, 2));
  }
}

// Main execution
async function main() {
  console.log(`${colors.bright}${colors.cyan}MP3/MP4 Transcription Tool${colors.reset}\n`);

  parseArgs();

  if (!checkDependencies()) {
    log('\n✗ Missing required dependencies. Please install them and try again.', 'error');
    process.exit(1);
  }

  ensureDirectories();

  try {
    await processAllFiles();
    log('\n✓ All done!', 'success');
  } catch (error) {
    log(`\n✗ Error: ${error.message}`, 'error');
    if (CONFIG.showProgress) {
      console.error(error);
    }
    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { main, transcribeFile, CONFIG };
