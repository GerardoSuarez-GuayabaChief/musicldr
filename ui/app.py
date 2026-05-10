import customtkinter as ctk
import threading
import os

from tkinter import filedialog
from downloader.download_manager import DownloadManager

from downloader.youtube import search_youtube
from ui.search_card import SearchCard
from player.audio_player import AudioPlayer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Music Downloader and Player")
        self.geometry("1400x850")
        self.minsize(1200, 700)

        self.download_path = ""
        self.download_queue = []
        self.player = AudioPlayer()

        self.build_ui()

    def build_ui(self):

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="Music Downloader",
            font=("Arial", 24, "bold")
        )
        self.logo.pack(pady=20)

        # MAIN AREA
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.main_frame.grid_columnconfigure(0, weight=4)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=0)

        # SEARCH BAR
        self.search_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Buscar canción o artista",
            height=40
        )
        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=20
        )

        # SEARCH BUTTON
        self.search_button = ctk.CTkButton(
            self.main_frame,
            text="Buscar",
            command=self.search_music
        )
        self.search_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=20,
            sticky="n"
        )

        # RESULTS FRAME
        self.results_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Resultados"
        )
        self.results_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10
        )

        # QUEUE PANEL
        self.queue_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Cola de Descargas",
            width=300
        )

        self.queue_frame.grid(
            row=1,
            column=1,
            sticky="ns",
            padx=10,
            pady=10
        )

        # LIBRARY FRAME
        self.library_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Biblioteca",
            height=250
        )
        self.library_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10
        )

        # BOTTOM FRAME
        self.bottom_frame = ctk.CTkFrame(self.main_frame, height=120)
        self.bottom_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=20,
            pady=10
        )

        # PATH BUTTON
        self.path_button = ctk.CTkButton(
            self.bottom_frame,
            text="Seleccionar carpeta",
            command=self.select_folder
        )
        self.path_button.pack(side="left", padx=10, pady=20)

        # DOWNLOAD BUTTON
        self.download_button = ctk.CTkButton(
            self.bottom_frame,
            text="Descargar",
            fg_color="#1DB954",
            command=self.start_downloads
        )
        self.download_button.pack(side="right", padx=10, pady=20)

        # PLAYER CONTROLS
        self.player_frame = ctk.CTkFrame(
            self.bottom_frame,
            fg_color="#181818"
        )
        self.player_frame.pack(fill="x", padx=10, pady=10)

        # CURRENT SONG
        self.current_song_label = ctk.CTkLabel(
            self.player_frame,
            text="No reproduciendo",
            font=("Arial", 14)
        )
        self.current_song_label.pack(side="left", padx=20)

        # PLAY BUTTON
        self.play_button = ctk.CTkButton(
            self.player_frame,
            text="▶",
            width=50,
            command=self.resume_song
        )
        self.play_button.pack(side="right", padx=5)

        # PAUSE BUTTON
        self.pause_button = ctk.CTkButton(
            self.player_frame,
            text="⏸",
            width=50,
            command=self.pause_song
        )
        self.pause_button.pack(side="right", padx=5)

        # STOP BUTTON
        self.stop_button = ctk.CTkButton(
            self.player_frame,
            text="■",
            width=50,
            command=self.stop_song
        )
        self.stop_button.pack(side="right", padx=5)

        # PROGRESS BAR
        self.progress = ctk.CTkProgressBar(self.bottom_frame)
        self.progress.pack(fill="x", padx=20, pady=10)
        self.progress.set(0)

        #Status label
        self.status_label = ctk.CTkLabel(self.bottom_frame, text="Esperando...")
        self.status_label.pack(pady=5)

    def search_music(self):

        query = self.search_entry.get()

        results = search_youtube(query)

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for song in results:

            card = SearchCard(
                self.results_frame,
                song,
                self.add_to_queue
            )

            card.pack(
                fill="x",
                padx=10,
                pady=10
            )

    def select_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.download_path = folder
            self.status_label.configure(text=f"Destino: {folder}")

    def add_to_queue(self, song):
        self.download_queue.append(song)
        queue_item = ctk.CTkFrame(
            self.queue_frame,
            fg_color="#202020",
            corner_radius=12
        )
        queue_item.pack(
            fill="x",
            padx=5,
            pady=5
        )
        title = ctk.CTkLabel(
            queue_item,
            text=song['title'],
            wraplength=220,
            justify="left"
        )
        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 2)
        )
        artist = ctk.CTkLabel(
            queue_item,
            text=song['channel'],
            text_color="#B3B3B3"
        )
        artist.pack(
            anchor="w",
            padx=10,
            pady=(0, 10)
        )
        self.status_label.configure(
            text=f"Agregado a cola"
        )
    
    def start_downloads(self):

        if not self.download_queue:
            self.status_label.configure(
                text="La cola está vacía"
            )
            return

        if not self.download_path:
            self.status_label.configure(
                text="Selecciona una carpeta"
            )
            return

        threading.Thread(
            target=self.download_queue_songs,
            daemon=True
        ).start()
    
    def download_queue_songs(self):

        manager = DownloadManager(
            progress_callback=self.update_progress,
            status_callback=self.update_status
        )

        total = len(self.download_queue)

        for index, song in enumerate(self.download_queue):

            self.update_status(
                f"Descargando {index + 1} de {total}: {song['title']}"
            )

            manager.download_song(
                song,
                self.download_path
            )

        self.update_status("Todas las descargas terminaron")
        self.load_library()
    
    def update_progress(self, value):
        self.progress.set(value)

    def update_status(self, text):
        self.status_label.configure(text=text)
    
    def load_library(self):

        for widget in self.library_frame.winfo_children():
            widget.destroy()

        if not self.download_path:
            return

        files = os.listdir(self.download_path)

        mp3_files = [
            file for file in files
            if file.endswith('.mp3')
        ]

        for song in mp3_files:

            song_path = os.path.join(
                self.download_path,
                song
            )

            button = ctk.CTkButton(
                self.library_frame,
                text=song,
                anchor="w",
                command=lambda p=song_path: self.play_song(p)
            )

            button.pack(
                fill="x",
                padx=10,
                pady=5
            )
    
    def play_song(self, song_path):

        self.player.load(song_path)
        self.player.play()
        song_name = os.path.basename(song_path)

        self.current_song_label.configure(
            text=song_name
        )

    def pause_song(self):
        self.player.pause()

    def resume_song(self):
        self.player.resume()

    def stop_song(self):
        self.player.stop()
        self.current_song_label.configure(
            text="No reproduciendo"
        )
    
