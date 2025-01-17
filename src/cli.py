# cli.py
import argparse
import sys
import os
from y2lib import Video, Converter

def simple_convert(url):
    """Single URL conversion"""
    try:
        print(f"Processing URL: \033[94m{url}\033[0m\n")
        video = Video(url)
        print(f"Downloading: \033[95m{video.name}\033[0m\n")
        video.download()
        
        converter = Converter(video)
        if converter.convert():
            print(f"\033[92mSuccess!\033[0m Converted to MP3: {video.name}\n")
        else:
            print(f"\033[91mFailed to convert {video.name}\033[0m\n")
    except Exception as e:
        print(f"\033[91mError: {str(e)}\033[0m\n")
    os.system("timeout /t 1 > nul")
    os.system("cls" if os.name == "nt" else "clear")

def interactive_mode():
    """Interactive CLI mode"""
    print("\n")
    os.system("cls" if os.name == "nt" else "clear")
    while True:
        print("\033[95m=== py2mate ===\033[0m")
        print("\nOptions:")
        print("\033[90m1.\033[0m \033[94mConvert single video\033[0m")
        print("\033[90m2.\033[0m \033[94mConvert multiple videos\033[0m")
        print("\033[90m3.\033[0m \033[94mExit\033[0m")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            os.system("cls" if os.name == "nt" else "clear")
            print("\033[95m=== py2mate ===\033[0m")
            url = input("\nEnter YouTube URL: ")
            simple_convert(url)
        
        elif choice == "2":
            os.system("cls" if os.name == "nt" else "clear")
            print("\033[95m=== py2mate ===\033[0m")
            urls = []
            print("\nEnter YouTube URLs (one per line, empty line to start conversion):")
            while True:
                url = input()
                if not url:
                    break
                urls.append(url)
            
            print(f"\nProcessing {len(urls)} videos...")
            for i, url in enumerate(urls, 1):
                print(f"\n[{i}/{len(urls)}]")
                simple_convert(url)
        
        elif choice == "3":
            os.system("cls" if os.name == "nt" else "clear")
            print("\033[94mGoodbye!\033[0m")
            sys.exit(0)
        
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print("\033[91mInvalid choice. Please try again.\033[0m")

def main():
    parser = argparse.ArgumentParser(description="Convert YouTube videos to MP3")
    parser.add_argument("-u", "--url", help="YouTube URL to convert")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")   
    args = parser.parse_args()
    
    if args.url:
        simple_convert(args.url)
    elif args.interactive:
        interactive_mode()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
