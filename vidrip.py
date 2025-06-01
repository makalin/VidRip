import os
import argparse
import json
from yt_dlp import YoutubeDL
import sys
from tqdm import tqdm
import urllib.request

def setup_arguments():
    parser = argparse.ArgumentParser(
        description="VidRip: A terminal-based video/audio downloader for YouTube, Twitter (X), Facebook, and more.",
        epilog="Examples:\n  python vidrip.py https://www.youtube.com/watch?v=example -o ripped_videos\n  python vidrip.py -b urls.txt -a -t -m",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("url", nargs="?", help="URL of the video to download (optional if -b is used)")
    parser.add_argument("-b", "--batch-file", help="Text file with list of URLs to download")
    parser.add_argument("-o", "--output", default="ripped_videos", help="Output directory (default: ripped_videos)")
    parser.add_argument("-f", "--format", default="best", help="Video format (e.g., 'best', 'mp4', or code like '22')")
    parser.add_argument("-l", "--list-formats", action="store_true", help="List available formats for the video")
    parser.add_argument("-a", "--audio", action="store_true", help="Extract audio only (MP3 format)")
    parser.add_argument("-t", "--thumbnail", action="store_true", help="Download video thumbnail")
    parser.add_argument("-m", "--metadata", action="store_true", help="Save video metadata to JSON")
    return parser.parse_args()

def create_output_directory(output_dir):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except OSError as e:
        print(f"Error creating output directory: {str(e)}")
        sys.exit(1)

def list_formats(url):
    ydl_opts = {'listformats': True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Error fetching formats: {str(e)}")
        sys.exit(1)

def get_progress_hook(pbar):
    def progress_hook(d):
        if d['status'] == 'downloading':
            pbar.update(1)
        elif d['status'] == 'finished':
            pbar.close()
    return progress_hook

def download_thumbnail(info, output_dir):
    thumbnail_url = info.get('thumbnail')
    if thumbnail_url:
        thumbnail_path = os.path.join(output_dir, f"{info['title']}_thumbnail.jpg")
        try:
            urllib.request.urlretrieve(thumbnail_url, thumbnail_path)
            print(f"Thumbnail saved to {thumbnail_path}")
        except Exception as e:
            print(f"Error downloading thumbnail: {str(e)}")

def save_metadata(info, output_dir):
    metadata = {
        'title': info.get('title'),
        'description': info.get('description'),
        'uploader': info.get('uploader'),
        'duration': info.get('duration'),
        'upload_date': info.get('upload_date'),
        'view_count': info.get('view_count')
    }
    metadata_path = os.path.join(output_dir, f"{info['title']}_metadata.json")
    try:
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        print(f"Metadata saved to {metadata_path}")
    except Exception as e:
        print(f"Error saving metadata: {str(e)}")

def download_media(url, output_dir, format_code, audio_only, thumbnail, metadata):
    ydl_opts = {
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'format': 'bestaudio/best' if audio_only else format_code,
        'noplaylist': True,
        'quiet': False,
        'progress_hooks': [get_progress_hook(tqdm(total=100, desc="Downloading", unit="%"))],
    }
    if audio_only:
        ydl_opts.update({
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])
            if thumbnail:
                download_thumbnail(info, output_dir)
            if metadata:
                save_metadata(info, output_dir)
        print(f"Media downloaded successfully to {output_dir}")
    except Exception as e:
        print(f"Error downloading media: {str(e)}")
        return False
    return True

def process_batch_file(batch_file, output_dir, format_code, audio_only, thumbnail, metadata):
    try:
        with open(batch_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading batch file: {str(e)}")
        sys.exit(1)
    
    successes = 0
    total = len(urls)
    for i, url in enumerate(urls, 1):
        print(f"\nProcessing URL {i}/{total}: {url}")
        if download_media(url, output_dir, format_code, audio_only, thumbnail, metadata):
            successes += 1
    print(f"\nBatch download complete: {successes}/{total} URLs processed successfully")

def main():
    args = setup_arguments()
    create_output_directory(args.output)
    
    if args.list_formats and args.url:
        print(f"Fetching available formats for {args.url}...")
        list_formats(args.url)
    elif args.batch_file:
        process_batch_file(args.batch_file, args.output, args.format, args.audio, args.thumbnail, args.metadata)
    elif args.url:
        print(f"Ripping {'audio' if args.audio else 'video'} from {args.url}...")
        download_media(args.url, args.output, args.format, args.audio, args.thumbnail, args.metadata)
    else:
        print("Error: Please provide a URL or a batch file with -b")
        sys.exit(1)

if __name__ == "__main__":
    main()