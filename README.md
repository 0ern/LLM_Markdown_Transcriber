# Portable AI Transcriber & Document-to-Markdown Toolkit

A 100% self-contained, zero-configuration, and privacy-focused Windows desktop automation framework designed to handle local AI-powered media transcription and multi-format document conversion. 

Built strictly on the philosophy of **Separation of Concerns (SoC)** and **Ultra-Portability**, this toolkit operates entirely within its own root directory. It isolates all heavy dependencies (including local CUDA binaries, machine learning neural models, and FFmpeg bundles), ensuring your global Windows environment remains pristine and pollution-free. If you no longer need the project, simply delete the main directory, and your system leaves no tracking files or residual "junk".

---

## ⚙️ How It Works

The project exposes two lightweight native Windows entry-point scripts (`.bat`), leaving all complex automation logic to an underlying unifed Python backend:

**`MarkDown_Transcriber.bat` (Media Subsystem):** Triggers a background environment diagnostics routine (`setup.py`). It verifies Python, updates `pip`, builds or updates a localized unified virtual environment (`.venv`), updates `yt-dlp` to prevent video scraping syntax breaks, and ensures Windows Long Paths are unlocked. Once verified, it passes execution to the core transcription cluster (`transcriber.py`) which coordinates local asset scraping, dynamic GPU/CUDA acceleration mapping, and AI inference.
Scans your local `Input_Documents` recursively. Utilizing the same portable ecosystem, it passes various files (PDFs, Word docs, Excel spreadsheets, images, presentations) into the local Microsoft MarkItDown instance via a streamlined Python runner (`document_converter.py`), converting them seamlessly into semantic Markdown documents.

---

## ✨ Key Features

- **🚀 100% Portable & Isolated:** Virtual environments, downloads, neural cache roots, and execution logs reside strictly inside the `lib/` directory. No global `PATH` modifications, no hidden AppData caching.
- **🎙️ State-of-the-Art AI Transcription:** Leverages `faster-whisper` (configured to use the modern, highly accurate `turbo` neural architecture) for lightning-fast transcriptions.
- **🔌 Automatic CUDA/GPU Dynamic Injection:** Automatically inspects local python virtual package directories at boot time and injects required NVIDIA CuBLAS/CuDNN `.dll` files straight into the runtime session execution context, enabling full GPU hardware acceleration out of the box.
- **🔄 Forced YouTube Scraper Shield:** Auto-upgrades `yt-dlp` silently on every single boot to stay ahead of breaking changes on media distribution networks.
- **📄 Native FFmpeg Lifecycle Management:** No need to manually download or install FFmpeg. The toolkit natively handles downloading, integrity unpacking, and deployment of official lightweight `gpl` standalone builds internally.
- **📂 Multi-Format Conversion Wrapper:** Mass-convert `.pdf`, `.docx`, `.doc`, `.xlsx`, `.xls`, `.pptx`, `.ppt`, `.html`, `.rtf`, `.odt`, `.ods`, `.odp`, `.png`, `.jpg`, and `.jpeg` into highly clean `.md` layouts natively using Microsoft's MarkItDown.
- **🛡️ Windows Safety Safeguards:** Natively prompts for UAC elevation via PowerShell to fix the Windows Long Paths constraint (per-character limits over 260 bytes), avoiding fatal pipeline constraints during complex model handling.

---

## 💻 System Requirements

- **Operating System:** Windows 10 or Windows 11 (64-bit architectures).
- **Python Environment:** A native execution of [Python 3.10 or higher](https://www.python.org/) installed globally on the host OS. (The script will automatically detect and configure it).
- **Hardware Acceleration (Optional but Recommended):** An NVIDIA Graphics Card (GPU) with sufficient VRAM to leverage high-speed CUDA-accelerated transcription. If an operational CUDA ecosystem isn't recognized or available, the transcriber safely triggers an automated fallback mechanism to run seamlessly over system CPU processing power.

---

## 📥 Getting Started

### 1. Download/Clone the Project
Download this repository as a `.zip` archive and extract it anywhere on your storage drive (e.g., Desktop, External SSD, local directory), or clone it via Git:
```
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```
### 2. How to Run the Transcriber
`Double-click MarkDown_Transcriber.bat.`

On the first boot, the toolkit will take a few moments to automatically download FFmpeg, create the virtual environment, install package dependencies, configure system Long Paths, and fetch the AI Whisper model.

Follow the terminal on-screen prompt: Paste a YouTube link (video, shorts, or full playlist) or type the path to a local audio/video file (e.g., `C:\audio\interview.mp3`).

Find your completed text files inside the automatically created `Markdown_output/` folder.

For documents

Place all files you wish to convert (PDFs, Office documents, images) inside the newly generated `Input_Documents` folder. (You can also organize them using subfolders).

Double-click `Double-click MarkDown_Transcriber.bat.` again. The script will recursively parse all documents.

Find your clean converted files ready inside the `Converted_Markdown` folder.

## 📂 Repository Structure

```
📁 your-repo-name/
│
├── 📄 MarkDown_Transcriber.bat   <- Local launcher for AI audio/YouTube transcription
│
├── 📁 Input_Documents/           <- Drop your source documents (PDF, Word, etc.) here
├── 📁 Converted_Markdown/        <- Output folder for processed document markdowns
├── 📁 Markdown_output/           <- Output folder for AI audio transcription text files
│
└── 📁 lib/                       <- Core system engine room (strictly isolated)
    ├── 📄 setup.py               <- System diagnostics, venv setup, yt-dlp & FFmpeg downloader
    ├── 📄 transcriber.py         <- Core AI audio pipeline (Whisper, CUDA layout manager)
    ├── 📄 document_converter.py  <- Core document conversion engine (MarkItDown adapter)
    │
    ├── 📁 FFmpeg/                <- Autogenerated folder holding portable ffmpeg.exe/ffprobe.exe
    ├── 📁 models/                <- Autogenerated folder storing local offline Whisper AI models
    └── 📁 markitdown/            
        └── 📁 .venv/             <- Unified virtual environment containing all dependencies & CUDA binaries
```

## 👥 Credits
This automation suite binds together several elite tools developed by the open-source community:

[Microsoft MarkItDown](https://github.com/microsoft/markitdown): For the exceptional structured multi-format document conversion backend.

[Faster-Whisper](https://github.com/SYSTRAN/faster-whisper): For the highly optimized reimplementation of OpenAI's Whisper model utilizing CTranslate2.

[yt-dlp](https://github.com/yt-dlp/yt-dlp): For the standard-setting video scraper engine utility.

[FFmpeg Builds by BtbN](https://github.com/BtbN/FFmpeg-Builds): For providing reliable, modern, standalone Windows binary releases.

## 📄 License
This project is licensed under the MIT License
