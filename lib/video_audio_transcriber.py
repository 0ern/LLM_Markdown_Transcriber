import os
import sys
import warnings
import logging
import yt_dlp
from faster_whisper import WhisperModel

# Initialize Windows Virtual Terminal Processing to enable ANSI color codes
os.system('')

# =====================================================================
# TERMINAL ANSI COLOR CONFIGURATION CONSTANTS (DARKCYAN THEME)
# =====================================================================
C_DARKCYAN = "\033[36m"
C_DARKGRAY = "\033[90m"
C_RED = "\033[91m"
C_YELLOW = "\033[93m"
C_GREEN = "\033[92m"
C_RESET = "\033[0m"

# Disable Hugging Face symbolic link warnings on Windows systems
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

# Determine local system path layout for injecting local CUDA binaries
lib_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(lib_dir)

search_paths = [lib_dir]
nvidia_base_dir = os.path.join(lib_dir, "MarkItDown", ".venv", "Lib", "site-packages", "nvidia")
if os.path.exists(nvidia_base_dir):
    for root, dirs, files in os.walk(nvidia_base_dir):
        if "bin" in dirs:
            search_paths.append(os.path.join(root, "bin"))

os.environ["PATH"] = os.path.pathsep.join(search_paths) + os.path.pathsep + os.environ["PATH"]

# Set artificial intelligence neural network model version configuration
# OPTIONS: "tiny", "base", "small", "medium", "large-v3", "turbo"
MODEL_SIZE = "turbo"
TEXT_PROMPT = "Clean transcription with accurate punctuation and capitalization."

def main():
    # Automatically create the 'Input_Documents' folder at the root level if it does not exist
    os.makedirs(os.path.join(root_dir, "Input_Documents"), exist_ok=True)

    # Print engine readiness notification to the console
    print(f"Engine initialized. Ready for universal processing.")
    
    # Prompt the user to enter a URL or Drag & Drop a local file directly into the console
    source_input = input(f"\n{C_DARKCYAN}Paste URL (Playlist/Video/Reel/Post), Drag and Drop a local file here or simply press Enter to process files in 'Input_Documents' folder: {C_RESET}").strip()
    
    # Clean up potential quotation marks automatically added by Windows during file drag-and-drop actions
    source_input = source_input.strip('"').strip("'").strip()
    
    # Supported document formats compatible with Microsoft MarkItDown parser architecture
    DOC_EXTENSIONS = ('.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.html', '.htm', '.rtf', '.odt', '.ods', '.odp', '.png', '.jpg', '.jpeg')

    # If input is empty, process the batch 'Input_Documents' folder directly
    if not source_input:
        print(f"\n{C_DARKGRAY}[INFO] Empty input detected. Scanning 'Input_Documents' folder...{C_RESET}")
        sys.path.append(lib_dir)
        import document_converter
        document_converter.ensure_environment(lib_dir)
        # Define and build output folder path
        output_dir = os.path.join(root_dir, "Output_Markdown")
        os.makedirs(output_dir, exist_ok=True)
        document_converter.process_input_documents_folder(root_dir, output_dir, lib_dir)
        return

    # Intercept single document files for direct Drag and Drop terminal support
    if os.path.exists(source_input) and os.path.isfile(source_input) and source_input.lower().endswith(DOC_EXTENSIONS):
        print(f"\n{C_DARKGRAY}[INFO] Local document detected. Initializing MarkItDown converter...{C_RESET}")
        sys.path.append(lib_dir)
        import document_converter
        document_converter.ensure_environment(lib_dir)
        # Ensure output directory exists before converting a single file
        output_dir = os.path.join(root_dir, "Output_Markdown")
        os.makedirs(output_dir, exist_ok=True)
        document_converter.convert_single_file(source_input, output_dir, lib_dir)
        return

    # Define and build target output files directory path layout
    output_dir = os.path.join(root_dir, "Output_Markdown")
    os.makedirs(output_dir, exist_ok=True)

    # Define and build artificial intelligence local model cache repository path
    models_dir = os.path.join(lib_dir, "Whisper_models")
    os.makedirs(models_dir, exist_ok=True)

    print(f"\n{C_DARKCYAN}[1/4] Initializing machine learning model...{C_RESET}")
    try:
        # Attempt to force Nvidia GPU hardware acceleration (CUDA)
        model = WhisperModel(MODEL_SIZE, device="cuda", compute_type="float16", download_root=models_dir)
        print(f"{C_GREEN}[OK] Model successfully stored in VRAM (Nvidia GPU)!{C_RESET}")
    except Exception as gpu_error:
        print(f"{C_YELLOW}[WARNING] Nvidia CUDA not available. Falling back to CPU mode...{C_RESET}")
        try:
            # Fallback to CPU execution layout with optimized integer quantization
            model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8", download_root=models_dir)
            print(f"{C_GREEN}[OK] Model successfully loaded into System RAM (CPU Mode)!{C_RESET}")
        except Exception as cpu_error:
            print(f"\n{C_RED}[CRITICAL ERROR] Failed to initialize machine learning engine: {cpu_error}{C_RESET}")
            return

    print(f"\n{C_DARKCYAN}[2/4] Parsing input source metadata...{C_RESET}")
    
    # Custom quiet logger to suppress noisy warnings (like Instagram csrf tokens)
    class YTDLQuietLogger:
        def debug(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg): pass

    # Resolve input into a clean list of individual targets
    inputs = []
    playlist_title = "Web_Source"
    
    # Check if the user dragged and dropped a local text file containing a list of links
    if os.path.exists(source_input) and source_input.lower().endswith(('.md', '.txt')):
        # Set the markdown file name based on the text file name (e.g., links.txt -> links.md)
        playlist_title = os.path.splitext(os.path.basename(source_input))[0]
        with open(source_input, "r", encoding="utf-8") as f:
            # Read non-empty lines and filter out comments starting with '#'
            inputs = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    # Check if the user pasted multiple links separated by spaces or newlines directly
    elif "\n" in source_input or " " in source_input:
        playlist_title = "Pasted_Links"
        inputs = [line.strip() for line in source_input.replace("\n", " ").split(" ") if line.strip()]
    else:
        # Single URL or single local media file path
        inputs = [source_input]

    # =====================================================================
    # AUTOMATIC URL CLEANING / SANITIZATION SYSTEM
    # =====================================================================
    cleaned_inputs = []
    for item in inputs:
        # Only clean if it's a web link (not a local file path)
        if not os.path.exists(item):
            for param in ['&si=', '?si=', '?igsh=', '&igsh=', '&feature=shared', '?feature=shared']:
                if param in item:
                    item = item.split(param)[0]
        cleaned_inputs.append(item)
    inputs = cleaned_inputs

    videos = []
    extraction_settings = {
        'extract_flat': True,
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'logger': YTDLQuietLogger(),
        'extractor_args': {'youtube': {'player_client': ['default']}},
    }
    
    # Extract metadata for all identified individual input targets
    with yt_dlp.YoutubeDL(extraction_settings) as ydl:
        for item in inputs:
            if os.path.exists(item) and not item.lower().endswith(('.md', '.txt')):
                file_base_name = os.path.splitext(os.path.basename(item))[0]
                if playlist_title == "Web_Source":
                    playlist_title = file_base_name
                videos.append({
                    'id': f"local_{file_base_name}",
                    'title': file_base_name,
                    'url': item,
                    'channel': "Local Computer",
                    'is_local': True
                })
            else:
                success = False
                try:
                    # Try flat extraction first (highly optimized for large playlists)
                    playlist_info = ydl.extract_info(item, download=False)
                    if playlist_info:
                        if 'entries' in playlist_info:
                            entries = [e for e in playlist_info['entries'] if e]
                            if entries:
                                videos.extend(entries)
                                success = True
                                if playlist_title == "Web_Source":
                                    playlist_title = playlist_info.get('title', 'Unknown Playlist')
                        else:
                            videos.append(playlist_info)
                            success = True
                            if playlist_title == "Web_Source":
                                playlist_title = playlist_info.get('title', 'Web_Source')
                except Exception:
                    pass

                # Fallback layout: If flat extraction failed or returned an empty structure (common for single items on Instagram/TikTok), try full extraction
                if not success:
                    try:
                        fallback_settings = {**extraction_settings, 'extract_flat': False}
                        with yt_dlp.YoutubeDL(fallback_settings) as ydl_fallback:
                            fallback_info = ydl_fallback.extract_info(item, download=False)
                            if fallback_info:
                                if 'entries' in fallback_info and fallback_info.get('entries'):
                                    entries = [e for e in fallback_info['entries'] if e]
                                    videos.extend(entries)
                                else:
                                    videos.append(fallback_info)
                                if playlist_title == "Web_Source":
                                    playlist_title = fallback_info.get('title', 'Web_Source')
                    except Exception as e:
                        print(f"{C_YELLOW}[WARNING] Failed to fetch metadata for '{item}': {e}{C_RESET}")
                    
    total_videos = len(videos)
    if total_videos == 0:
        print(f"{C_RED}[ERROR] No valid videos or links could be resolved. Exiting...{C_RESET}")
        return
    print(f"{C_GREEN}[OK] Located {total_videos} remote item(s) in the download queue.{C_RESET}")

    # Filter and sanitize dangerous character entities from the playlist title string
    forbidden_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', ',', '\'', '|', '#', '@', '.', '!']
    safe_playlist_title = playlist_title
    for char in forbidden_chars:
        safe_playlist_title = safe_playlist_title.replace(char, '')
    safe_playlist_title = safe_playlist_title.strip().replace(" ", "_")

    # Prevent overwriting by checking if a finalized or multi-part file already exists
    base_title = safe_playlist_title
    version_counter = 1
    while os.path.exists(os.path.join(output_dir, f"{safe_playlist_title}.md")) or \
        os.path.exists(os.path.join(output_dir, f"{safe_playlist_title}_part_1.md")):
        safe_playlist_title = f"{base_title}_version_{version_counter}"
        version_counter += 1

    print(f"\n{C_DARKCYAN}[3/4] Starting sequential audio processing loop...{C_RESET}")
    
    # Initialize index segmentation variables for the dynamic output tracker logic
    current_part = 1
    current_word_count = 0
    WORD_LIMIT = 490000  # NotebookLM optimal word limit threshold safety buffer
    
    # Iterate through each item present inside the task collection
    for index, video in enumerate(videos, 1):
        # Ignore empty items inside the tracking map array
        if not video:
            continue
        
        # Build file name mapping corresponding to the current partition number
        filename = f"{safe_playlist_title}_part_{current_part}.md"
        current_output_file = os.path.join(output_dir, filename)
        
        # Initialize the target file volume if it does not exist on disk
        if not os.path.exists(current_output_file):
            with open(current_output_file, "w", encoding="utf-8") as f:
                # Cleaner header title block omitting Part 1 text unless rolled over
                part_suffix = f" (Part {current_part})" if current_part > 1 else ""
                f.write(f"# Transcript Collection: {playlist_title}{part_suffix}\n")
                f.write("\n=============\n\n")
            print(f"\n{C_DARKGRAY}[INFO] Initializing document volume: Markdown_output/{filename}{C_RESET}")

        # Extract structural parameters safely using safe fallbacks for missing dictionary blocks
        video_id = video.get('id')
        video_title = video.get('title', f"Item {index}")
        video_url = video.get('webpage_url') or video.get('url') or source_input
        video_channel = video.get('channel') or video.get('uploader') or "Unknown Source"
        is_local = video.get('is_local', False)
        
        print(f"{C_DARKCYAN}[{index}/{total_videos}] Processing: {video_title}{C_RESET}")
        
        audio_file_path = None
        video_description = "No caption available (Local file or not found)."
        
        # Bypass download mechanism entirely if dealing with a native computer asset file
        if is_local:
            audio_file_path = video_url
        else:
            # Establish temporal local file paths configuration for remote asset audio dumping tasks
            temp_audio_path = os.path.join(lib_dir, f"temp_audio_{video_id}")

            # Pre-fetch rich metadata to extract descriptions from non-video posts (like standard Instagram photo posts)
            meta_settings = {
                'quiet': True,
                'no_warnings': True,
                'logger': YTDLQuietLogger(),
                'extractor_args': {'youtube': {'player_client': ['default']}},
            }
            with yt_dlp.YoutubeDL(meta_settings) as ydl_meta:
                try:
                    full_info = ydl_meta.extract_info(video_url, download=False)
                    if full_info:
                        if full_info.get('description'):
                            video_description = full_info.get('description').strip()
                            # Normalize anomalous Unicode line terminators (\u2028 and \u2029) for clear markdown presentation
                            video_description = video_description.replace('\u2028', '\n').replace('\u2029', '\n')
                        if full_info.get('uploader') or full_info.get('channel'):
                            video_channel = full_info.get('uploader') or full_info.get('channel')
                        if full_info.get('title'):
                            video_title = full_info.get('title')
                except Exception:
                    pass

            downloader_settings = {
                'format': 'bestaudio/best',
                'outtmpl': temp_audio_path,
                'quiet': True,
                'no_warnings': True,
                'logger': YTDLQuietLogger(),
                'retries': 5,
                'fragment_retries': 5,
                'socket_timeout': 15,
                'extractor_args': {'youtube': {'player_client': ['default']}},
            }
            
            with yt_dlp.YoutubeDL(downloader_settings) as ydl:
                try:
                    # Trigger down-streaming routine to catch remote file audio component
                    info = ydl.extract_info(video_url, download=True)
                    if info and info.get('description'):
                        video_description = info.get('description').strip()
                        video_description = video_description.replace('\u2028', '\n').replace('\u2029', '\n')
                    else:
                        video_description = "No caption available."
                    audio_file_path = ydl.prepare_filename(info)

                    # Fallback directory crawler matching system if standard name derivation fails
                    if not os.path.exists(audio_file_path):
                        for file_name in os.listdir(lib_dir):
                            if file_name.startswith(f"temp_audio_{video_id}"):
                                audio_file_path = os.path.join(lib_dir, file_name)
                                break
                except Exception as e:
                    # Check if a caption was successfully recovered despite the lack of transcribable audio (e.g., standard photo posts)
                    if video_description and video_description != "No caption available (Local file or not found)." and video_description != "No caption available.":
                        print(f"{C_DARKGRAY}[INFO] Caption successfully extracted for non-video asset.{C_RESET}")
                        with open(current_output_file, "a", encoding="utf-8") as f:
                            f.write(f"## Item No. {index}\n")
                            f.write(f"## Title: {video_title}\n")
                            f.write(f"## Source: {video_channel}\n")
                            f.write(f"**Path/Link:** {video_url}\n")
                            f.write(f"**Asset ID:** `{video_id}`\n")
                            f.write(f"**Word Count:** {incoming_words} words\n\n")
                            f.write("### Transcript\n")
                            f.write("_No spoken audio track detected or available to transcribe for this asset._\n\n")
                            f.write("### Description / Caption\n")
                            f.write(f"{video_description}\n\n")
                            f.write("---\n\n")
                    else:
                        # Fallback error mapping for genuine network failures or completely private accounts
                        print(f"{C_YELLOW}[WARNING] Downloader failure encountered. Skipping item.{C_RESET}")
                        with open(current_output_file, "a", encoding="utf-8") as f:
                            f.write(f"## Item No. {index}\n")
                            f.write(f"## Title: {video_title}\n")
                            f.write(f"## Source: {video_channel}\n")
                            f.write(f"**Path/Link:** {video_url}\n")
                            f.write(f"**Asset ID:** `{video_id}`\n")
                            f.write(f"**Word Count:** {incoming_words} words\n\n")
                            f.write(f"**ERROR:** Failed to extract audio component or post metadata.\n\n---\n\n\n")
                    continue

        try:
            # Verify file exists and is not completely empty (0 bytes) before processing
            if audio_file_path and os.path.exists(audio_file_path) and os.path.getsize(audio_file_path) > 0:
                try:
                    # Submit audio into the local machine learning transcription execution queue
                    segments, _ = model.transcribe(audio_file_path, beam_size=5, language=None, initial_prompt=TEXT_PROMPT)

                    # Combine all whisper segments into a single continuous stream of text
                    raw_text = " ".join([segment.text.strip() for segment in segments])
                    
                    # Use regular expressions to cleanly split text right after sentence boundaries (. ? !)
                    import re
                    sentences = re.split(r'(?<=[.!?])\s+', raw_text)

                    # Join each complete sentence with a single newline, filtering out empty lines
                    full_transcript_text = "\n".join([sentence.strip() for sentence in sentences if sentence.strip()])
                except Exception:
                    # Handle internal engine crashes (e.g., 'tuple index out of range' on short/silent clips)
                    full_transcript_text = "_No spoken audio track detected or available to transcribe for this asset._"
            else:
                # Fallback text if the audio file doesn't exist or is completely empty
                full_transcript_text = "_No spoken audio track detected or available to transcribe for this asset._"

            # Double-check fallback if transcription execution returned an entirely empty sequence
            if not full_transcript_text.strip():
                full_transcript_text = "_No spoken audio track detected or available to transcribe for this asset._"

            incoming_words = len(full_transcript_text.split())

            # Dynamic volume segmentation tracking to rollover if word volume limits are breached
            if (current_word_count + incoming_words > WORD_LIMIT) and current_word_count > 0:
                print(f"{C_YELLOW}[VOLUME LIMIT] Current file reached {current_word_count} words. Rolling over...{C_RESET}")
                current_part += 1
                current_word_count = 0
                filename = f"{safe_playlist_title}_part_{current_part}.md"
                current_output_file = os.path.join(output_dir, filename)
                
                # Create the next rollover volume block header
                with open(current_output_file, "w", encoding="utf-8") as f:
                    f.write(f"# Transcript Collection: {playlist_title} (Part {current_part})\n")
                    f.write("\n=============\n\n")
                print(f"{C_DARKGRAY}[INFO] Initializing document volume: Markdown_output/{filename}{C_RESET}")

            # Append finalized clean text content blocks inside active open stream document
            with open(current_output_file, "a", encoding="utf-8") as f:
                f.write(f"## Item No. {index}\n")
                f.write(f"## Title: {video_title}\n")
                f.write(f"## Source: {video_channel}\n")
                f.write(f"**Path/Link:** {video_url}\n")
                f.write(f"**Asset ID:** `{video_id}`\n")
                f.write(f"**Word Count:** {incoming_words} words\n\n")
                f.write("### Transcript\n")
                f.write(f"{full_transcript_text.strip()}\n\n")
                f.write("### Description / Caption\n")
                f.write(f"{video_description}\n\n")
                f.write("---\n\n")
                
            # Increment the aggregate active tracking word register
            current_word_count += incoming_words
            print(f"{C_GREEN}[OK] Generated. (File size: {current_word_count}/{WORD_LIMIT} words){C_RESET}\n")
            
        except Exception as e:
            # Capture deep engine parsing errors and log the failure inside the markdown file to keep output structured
            print(f"{C_RED}[ERROR] Neural network engine failure: {e}{C_RESET}")
            with open(current_output_file, "a", encoding="utf-8") as f:
                f.write(f"## Item No. {index}\n")
                f.write(f"## Title: {video_title}\n")
                f.write(f"## Source: {video_channel}\n")
                f.write(f"**Path/Link:** {video_url}\n")
                f.write(f"**Asset ID:** `{video_id}`\n")
                f.write(f"**Word Count:** {incoming_words} words\n\n")
                f.write(f"**ERROR:** Neural network engine failed to transcribe this asset ({e}).\n\n---\n\n")
        finally:
            # ONLY erase files that were downloaded from the internet. Never delete user local files.
            if not is_local and audio_file_path and os.path.exists(audio_file_path):
                os.remove(audio_file_path)

    # Smart volume cleanup: If only 1 part was generated, safely drop the '_part_1' suffix.
    if current_part == 1:
        part1_filename = f"{safe_playlist_title}_part_1.md"
        part1_path = os.path.join(output_dir, part1_filename)
        final_filename = f"{safe_playlist_title}.md"
        final_path = os.path.join(output_dir, final_filename)
        
        if os.path.exists(part1_path):
            try:
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.rename(part1_path, final_path)
                print(f"\n{C_DARKGRAY}[INFO] Suffix optimized. Final document name: Markdown_output/{final_filename}{C_RESET}")
            except Exception as e:
                print(f"\n{C_YELLOW}[WARNING] Could not optimize document suffix layout: {e}{C_RESET}")

    print(f"\n{C_DARKCYAN}[4/4] Execution workflow completed! Documents generated inside 'Markdown_output' directory.{C_RESET}")

if __name__ == "__main__":
    main()