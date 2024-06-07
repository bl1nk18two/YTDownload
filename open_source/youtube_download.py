from pytube import YouTube
import sys
import os

def main():
    # Prompt for the video URL
    yt = prompt_url('URL: ')
    # Prompt for the download type
    stream = file_extension("Video or Audio? (Type: 'V' or 'A'): ", yt)
    print("Downloading:", stream.default_filename)
    # Set the download path forthe user's downloads folder
    download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    stream.download(output_path=download_path)
    print("\nDownload complete! Path:", download_path)
    # Prompt for exit
    exit = input("Exit? Press 'ENTER'")
    
# URL Prompt
def prompt_url(url):
    try:
        link = input(url)
        # Callback for download progress
        yt = YouTube(link, on_progress_callback=progress_callback)
        print("Video's name:", yt.title)
        return yt
    except:
        # If URL is not correct, the program print this message and shuts down.
        sys.exit("URL is not valid.")

# Donwload Type
def file_extension(voa, url):
    type = input(voa)
    try:
        # Audio Type
        if type.lower() == 'a':
            stream = url.streams.filter(only_audio=True, file_extension='webm').first()
        # Video Type
        elif type.lower() == 'v':
            stream = url.streams.get_highest_resolution()    
        # If a no valid type is written, program raise a exception and shuts down
        else:
            raise Exception
        return stream
    except:
        sys.exit(f"Could Not Complete Action. {type} is not a valid argument.")

# Progress bar when downloading video or audio 
def progress_callback(stream, chunk, bytes_remaining):
    global filesize
    if not hasattr(progress_callback, 'filesize'):
        progress_callback.filesize = stream.filesize
    current = ((progress_callback.filesize - bytes_remaining) / progress_callback.filesize)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()
          
if __name__ == "__main__":
    main()