from pytube import Playlist, YouTube
from moviepy.editor import *
import youtube_dlc
import os
from tkinter import *
from tkinter.ttk import Progressbar
import re

def sanitize_filename(filename):
    # Remove caracteres inválidos
    filename = re.sub(r'[\\\\/*?:"<>|]', "", filename)
    # Limita o tamanho do nome do arquivo a 144 caracteres
    filename = filename[:144]
    return filename

def check_url_video(url):
    ydl = youtube_dlc.YoutubeDL({'quiet': True})
    try:
        info = ydl.extract_info(url, download=False)
        return True
    except Exception:
        return False

def download():
    link.config(state=DISABLED)
    playlist_link = link.get()
    playlist = Playlist(playlist_link)

    # Baixa apenas o áudio de cada vídeo da playlist
    total_videos = len(playlist.video_urls)
    progress['maximum'] = total_videos
    for i, video_url in enumerate(playlist.video_urls, start=1):
        try:
            if check_url_video(video_url):
                video = YouTube(video_url)
                audio_stream = video.streams.filter(only_audio=True).first()
                audio_file = audio_stream.download()
                audio = AudioFileClip(audio_file)
                video_title = sanitize_filename(video.title)
                audio.write_audiofile(video_title + ".mp3", bitrate="192k")
                os.remove(video_title + ".mp4")
            else:
                continue
        except Exception:
            continue
        progress['value'] = i
        progress.update()

root = Tk()
root.title("Baixa Playlist do Youtube")
root.resizable(True, True)
root.geometry("500x500")

link_label = Label(root, text="Link da playlist:")
link_label.config(font=("Arial", 25))
link_label.pack()

link = Entry(root)
link.config(font=("Arial", 16), width=50)
link.pack()

download_button = Button(root, text="Baixar", command=download)
download_button.config(font=("Arial", 26))
download_button.pack()

progress = Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
progress.pack(pady=10)

root.mainloop()
