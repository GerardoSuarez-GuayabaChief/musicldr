import customtkinter as ctk
from tkinter import filedialog

from downloader.youtube import search_youtube
from ui.search_card import SearchCard

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
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # SEARCH BAR
        self.search_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Buscar canción o artista",
            height=40
        )
        self.search_entry.pack(fill="x", padx=20, pady=20)

        # SEARCH BUTTON
        self.search_button = ctk.CTkButton(
            self.main_frame,
            text="Buscar",
            command=self.search_music
        )
        self.search_button.pack(pady=10)

        # RESULTS FRAME
        self.results_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Resultados"
        )
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # BOTTOM FRAME
        self.bottom_frame = ctk.CTkFrame(self.main_frame, height=120)
        self.bottom_frame.pack(fill="x", padx=20, pady=10)

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
            fg_color="#1DB954"
        )
        self.download_button.pack(side="right", padx=10, pady=20)

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
        self.status_label.configure(
        text=f"Agregado: {song['title']}"
        )
        print(self.download_queue)
