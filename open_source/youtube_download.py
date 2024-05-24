from pytube import YouTube
import sys
import os

def main():
    yt = prompt_url('URL: ')
    stream = file_extension("Video or Audio? (Type: 'V' or 'A'): ", yt)
    print("Downloading:", stream.default_filename)
    download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    stream.download(output_path=download_path)
    print("\nDownload complete! Path:", download_path)
    exit = input("Exit? Press 'ENTER'")
    

def prompt_url(url):
    try:
        link = input(url)
        yt = YouTube(link, on_progress_callback=progress_callback)
        print("Video's name:", yt.title)
        return yt
    except:
        sys.exit("URL is not valid.")

def file_extension(voa, url):
    type = input(voa)
    try:
        if type.lower() == 'a':
            stream = url.streams.filter(only_audio=True, file_extension='webm').first()
        elif type.lower() == 'v':
            stream = url.streams.get_highest_resolution()    
        else:
            raise Exception
        return stream
    except:
        sys.exit(f"Could Not Complete Action. {type} is not a valid argument.")

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