# 🎙️ LLM Markdown Transcriber
An automated, zero-configuration pipeline designed to bridge multimedia assets and structural text documents directly into clean, LLM-ready Markdown formatting.

Whether you feed it a collection of URLs (YouTube playlists, Instagram Reels, TikTok posts), local audio/video binaries, or raw enterprise documents (PDFs, Word docs, Excel spreadsheets), this tool seamlessly processes and structures them. Optimized to handle ultra-long outputs with smart volume splitting, it ensures seamless integration with LLMs and knowledge platforms like NotebookLM.

## 🚀 Key Features
- **Zero-Config Automated Bootstrap:** A completely local deployment engine that auto-detects system environments, provisions a standalone Python environment, downloads runtime-isolated `uv` package managers, and hooks portable FFmpeg binaries out-of-the-box.

- **High-Speed Audio/Video Transcription:** Driven by the `faster-whisper` neural network engine (turbo model), featuring automated Nvidia GPU hardware acceleration tracking (CUDA float16) with a robust fallback to optimized CPU integer execution (int8).

- **Universal Scraping Pipeline:** Integrated with `yt-dlp` to parse complex URLs natively, extract high-fidelity audio streams, scrape captions for non-video assets, and automatically filter tracking links/analytics tags.

- **Advanced Document Parser:** Built-in native pipeline using Microsoft's MarkItDown architecture to parse tabular data, slides, text layers, and image metadata directly into pure Markdown text blocks.

- **Smart Volume Rollover:** Intelligently monitors aggregate word counts against optimal context window limits (~490,000 words safety buffer for NotebookLM), automatically splitting text loads across sequential document volumes.

- **Windows Environment Sanitization:** Auto-handles native operating system friction points, including virtual terminal color configuration and administrative registry injection to patch Windows Long Paths limitations.

## 🛠️ Built With
- **Core Engine:** `Python` (Targeted for standard 3.10+ structures up to native 3.14 runtime layers)

- **Transcription Model:** `faster-whisper` (CTranslate2 implementation of OpenAI's Whisper architecture)

- **Document Processing:** Microsoft `MarkItDown` API wrappers

- **Stream Fetching Engine:** `yt-dlp`

- **Environment Orchestrator:** Astral `uv` toolchain

- **Scripting Systems:** Windows Batch Command Shell (`.bat`) + Windows PowerShell modules

## 📋 Prerequisites & Installation
The project is structured with 100% portability in mind. There is <ins> no need to pre-install Python, FFmpeg, or global package managers </ins> on your host operating system.

### Installation Steps
1. Download this repository &rarr; [DOWNLOAD HERE](https://github.com/0ern/LLM_Markdown_Transcriber/archive/refs/heads/main.zip)

2. Exctract and double-click the main script: `Markdown_Transcriber.bat`

The system diagnostics utility will automatically evaluate system path parameters, elevate access to enable long paths support if needed, and unpack all local operational dependencies inside a sandboxed workspace.

## 📖 How To Use
Once launched, the central console will prompt you with processing execution avenues:

```
Paste URL (Playlist/Video/Reel/Post), Drag and Drop a local file here or simply press Enter to process files in 'Input_Documents' folder:
```

1. **Web Video or Playlist Extraction**
Directly copy-paste links from streaming or social media networks. It handles individual assets or whole sequential playlists automatically.

Example input: `https://www.youtube.com/watch?v=example`

2. **Batch Link Ingestion via Documents**
Drag and drop a local `.txt` or `.md` file containing a collection of URLs separated by lines. The program filters comments (`#`) and tracks structural generation based on file name identifiers.

3. **Drag-and-Drop Local File Support**
Drag any individual supported video, audio, or document format directly into the console to compile a single isolated target markdown output.

4. **Headless Local Folder Ingestion**
Leave the prompt empty and press `Enter` to run batch directory conversions. The script scans the root directory's asset bank and parses all discovered payloads.

Supported File Formats:
- Audio/Video: `.mp3`, `.wav`, `.m4a`, `.mp4`, `.mkv`, etc. (handled via Whisper)

- Documents: `.pdf`, `.docx`, `.doc`, `.xlsx`, `.xls`, `.pptx`, `.ppt`, `.rtf`, `.odt`, `.ods`, `.odp`, `.html`

- Images: `.png`, `.jpg`, `.jpeg`

## 📁 Project Directory Layout

```
LLM_Markdown_Transcriber/
│
├── Markdown_Transcriber.bat       # Main script and configuration engine
├── Input_Documents/               # [Auto-generated] Folder for local document files
├── Output_Markdown/               # [Auto-generated] Folder containing the generated markdown files
│
└── lib/
    ├── document_converter.py      # Automated uv/MarkItDown workflow controller
    ├── setup.py                   # Global system platform diagnostics script
    ├── video_audio_transcriber.py # Neural network Whisper ingestion logic
    │
    ├── FFmpeg/                    # [Auto-generated] Standalone media binaries
    ├── MarkItDown/                # [Auto-generated] Sandboxed Python environment
    └── Whisper_models/            # [Auto-generated] Downloaded neural weight cache repository
```

## 🎖️ Credits
[This project](https://github.com/0ern/LLM_Markdown_Transcriber) leverages the power of several outstanding open-source libraries and tools:

- [MarkItDown](https://github.com/microsoft/markitdown) - Microsoft's official utility for converting various file formats into Markdown.

- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - Re-implementation of OpenAI's Whisper model using CTranslate2 for ultra-fast performance.

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A feature-rich command-line audio/video downloader for thousands of hosting sites.

- [uv](https://github.com/astral-sh/uv) - An extremely fast Python package installer and resolver written in Rust.

- [FFmpeg Builds](https://github.com/yt-dlp/FFmpeg-Builds) - High-quality, standalone static multimedia binaries for Windows compilation tasks.

## 📄 License
This project is licensed under the MIT License - see the repository details for more information.
