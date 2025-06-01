# VidRip

VidRip is a powerful, terminal-based video and audio downloader for platforms like YouTube, Twitter (X), Facebook, and many others supported by `yt-dlp`. It offers batch downloading, audio extraction, progress tracking, thumbnail downloading, and metadata extraction, all wrapped in a simple command-line interface.

## Features

- **Batch Downloading**: Download multiple videos or audio files from a list of URLs in a text file.
- **Audio Extraction**: Extract audio as MP3 files with customizable quality (default: 192 kbps).
- **Progress Bar**: Visual download progress using `tqdm`.
- **Thumbnail Downloading**: Save video thumbnails as JPEG files.
- **Metadata Extraction**: Save video metadata (title, description, uploader, etc.) to JSON files.
- **Format Selection**: Choose specific video/audio formats or use the default "best" quality.
- **Supported Platforms**: YouTube, Twitter (X), Facebook, and [many more](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Installation

1. **Prerequisites**:
   - Python 3.6 or higher
   - pip (Python package manager)

2. **Install Dependencies**:
   ```bash
   pip install yt-dlp tqdm
   ```

3. **Download VidRip**:
   Clone the repository or download the `vidrip.py` file:
   ```bash
   git clone https://github.com/makalin/VidRip.git
   cd VidRip
   ```

## Usage

Run `vidrip.py` with the desired options. The basic syntax is:

```bash
python vidrip.py [URL] [OPTIONS]
```

### Options

- `-b, --batch-file FILE`: Text file with URLs (one per line) for batch downloading.
- `-o, --output DIR`: Output directory (default: `ripped_videos`).
- `-f, --format FORMAT`: Video/audio format (e.g., `best`, `mp4`, or format code like `22`).
- `-l, --list-formats`: List available formats for a video.
- `-a, --audio`: Extract audio only (MP3 format).
- `-t, --thumbnail`: Download the video thumbnail.
- `-m, --metadata`: Save video metadata to a JSON file.

## Examples

1. **Download a single video**:
   ```bash
   python vidrip.py https://www.youtube.com/watch?v=example
   ```

2. **Extract audio**:
   ```bash
   python vidrip.py https://www.youtube.com/watch?v=example -a
   ```

3. **Batch download from a file**:
   Create a file `urls.txt`:
   ```
   https://www.youtube.com/watch?v=example1
   https://twitter.com/example/status/123456
   ```
   Then run:
   ```bash
   python vidrip.py -b urls.txt -o my_videos
   ```

4. **Download with thumbnail and metadata**:
   ```bash
   python vidrip.py https://www.youtube.com/watch?v=example -t -m
   ```

5. **List available formats**:
   ```bash
   python vidrip.py https://www.youtube.com/watch?v=example -l
   ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video/audio downloading.
- Uses [tqdm](https://github.com/tqdm/tqdm) for progress bars.

---

Happy ripping with VidRip! For issues or feature requests, please open an [issue](https://github.com/makalin/VidRip/issues).
