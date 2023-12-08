from cx_Freeze import setup, Executable

# Configuração das opções
options = {
    'build_exe': {
        'packages': ['os', 'tkinter', 'youtube_dlc', 'moviepy', 'pytube', 're', 'sys', 'subprocess', 'threading'],  # inclua todas as bibliotecas que você está usando no seu script
        'include_files': []  # se houver arquivos adicionais (como imagens, ícones, etc.) que você deseja incluir no executável, adicione-os aqui
    },
}

executables = [
    Executable('PlaylistDownloader.py', base='Win32GUI')  # substitua 'nome_do_seu_script.py' pelo nome do seu script Python
]

setup(
    name='Playlist Downloader',  # substitua 'NomeDoSeuPrograma' pelo nome que você deseja dar ao seu programa
    version='0.1',
    description='Realiza o download de playlist inteira do youtube, mesmo que ela tenha mais de 100 musicas',  # substitua 'Descrição do seu programa' por uma descrição do seu programa
    options=options,
    executables=executables
)
