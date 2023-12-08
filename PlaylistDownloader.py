# Importando as bibliotecas necessárias
from pytube import Playlist, YouTube
from moviepy.editor import *
import youtube_dlc
import os
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
import threading
import re
import sys
import subprocess

# Variável global para controlar o download
stop_download = False

# Função para verificar a URL do vídeo
def check_url_video(url):
    ydl = youtube_dlc.YoutubeDL({'quiet': True})
    try:
        info = ydl.extract_info(url, download=False)
        return True
    except Exception:
        return False

# Função para limpar o nome do arquivo
def clean_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    return filename[:64]

# Função para baixar os vídeos
def download(update_progress):
    global stop_download
    stop_download = False
    link.config(state=DISABLED)
    playlist_link = link.get()
    playlist = Playlist(playlist_link)

    # Atualizando o campo do nome da playlist
    playlist_name = clean_filename(playlist.title)
    playlist_name_var.set(playlist_name)

    # Criando um diretório com o nome da playlist
    os.makedirs(playlist_name, exist_ok=True)

    total_videos = len(playlist.video_urls)
    progress['maximum'] = total_videos
    for i, video_url in enumerate(playlist.video_urls, start=1):
        if stop_download:
            break
        try:
            if check_url_video(video_url):
                video = YouTube(video_url)
                audio_stream = video.streams.filter(only_audio=True).first()
                audio_file = audio_stream.download(output_path=playlist_name)
                filename = clean_filename(video.title)
                try:
                    audio = AudioFileClip(audio_file)
                    audio.write_audiofile(os.path.join(playlist_name, filename + ".mp3"), bitrate="192k")
                    os.remove(os.path.join(playlist_name, filename + ".mp4"))
                    update_progress(True, filename)
                except Exception:
                    os.remove(audio_file)
                    update_progress(False, filename)
            else:
                update_progress(False, video.title)
        except Exception:
            update_progress(False, video.title)
        progress['value'] = i
        progress.update()

    # Apagar os arquivos de vídeo após a finalização dos downloads e conversões
    delete_files(playlist_name)
    # Exibir a janela pop-up
    show_popup()

# Função para parar o download
def stop():
    global stop_download
    stop_download = True

# Função para apagar os arquivos de vídeo
def delete_files(playlist_name):
    # Listar todos os arquivos no diretório
    files = os.listdir(playlist_name)

    # Filtrar os arquivos de vídeo
    video_files = [file for file in files if file.endswith('.mp4')]

    for video_file in video_files:
        # Obter o nome do arquivo de vídeo sem a extensão
        video_name = os.path.splitext(video_file)[0]

        # Verificar se existe outro arquivo com o mesmo nome, mas com extensão diferente
        other_files = [file for file in files if file.startswith(video_name) and file != video_file]

        if other_files:
            # Se existir outro arquivo com o mesmo nome, apagar tanto o arquivo de vídeo quanto o outro arquivo
            os.remove(os.path.join(playlist_name, video_file))
            for other_file in other_files:
                os.remove(os.path.join(playlist_name, other_file))
        else:
            # Se não existir outro arquivo com o mesmo nome, apagar o arquivo de vídeo
            os.remove(os.path.join(playlist_name, video_file))

    # Verificar novamente se existem arquivos de vídeo
    files = os.listdir(playlist_name)
    video_files = [file for file in files if file.endswith('.mp4')]

    # Se ainda existirem arquivos de vídeo, apagá-los
    for video_file in video_files:
        os.remove(os.path.join(playlist_name, video_file))

# Função para reiniciar o programa
def restart_program():
    python = sys.executable
    os._exit(0)  # fecha o programa atual
    subprocess.Popen([python, *sys.argv])  # inicia uma nova instância do programa

# Função para finalizar o programa
def close_program():
    root.destroy()

# Função para exibir a janela pop-up
def show_popup():
    answer = messagebox.askquestion("Tarefa concluída", "A tarefa foi concluída. Você gostaria de reiniciar o programa?", icon='warning')
    if answer == 'yes':
        restart_program()
    else:
        close_program()

# Configuração da interface gráfica
root = Tk()
root.title("Baixa Playlist do Youtube")
root.resizable(True, True)
root.geometry("500x500")

link_label = Label(root, text="Link da playlist:")
link_label.config(font=("Arial", 25))
link_label.pack()

link = Entry(root)
link.config(font=("Arial", 16))
link.place(x=10, y=50, width=200, height=50)
link.pack()

# Campo do nome da playlist
playlist_name_var = StringVar()
playlist_name_label = Label(root, textvariable=playlist_name_var)
playlist_name_label.config(font=("Arial", 16))
playlist_name_label.pack()

download_button = Button(root, text="Baixar", command=lambda: threading.Thread(target=download, args=(update_progress,)).start())
download_button.config(font=("Arial", 26))
download_button.pack()

stop_button = Button(root, text="Cancelar", command=stop)
stop_button.config(font=("Arial", 26))
stop_button.pack()

progress = Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
progress.pack(pady=10)

file_list = Listbox(root, width=500)
file_list.pack(pady=(0, 10))

# Criação do rodapé
footer = Label(root, text="Desenvolvido por Lucas Silva - (19) 98142-2055 __ Versão: 1.5", bd=1, relief=SUNKEN, anchor=W)
footer.pack(side=BOTTOM, fill=X)

# Função para atualizar o progresso do download
def update_progress(success, filename):
    if success:
        file_list.insert(END, filename)
        file_list.itemconfig(END, {'fg': 'green'})
    else:
        file_list.insert(END, filename)
        file_list.itemconfig(END, {'fg': 'red'})

# Iniciando a interface gráfica
root.mainloop()
