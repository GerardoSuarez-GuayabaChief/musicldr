import customtkinter as ctk
import requests

from PIL import Image
from io import BytesIO


class SearchCard(ctk.CTkFrame):

    def __init__(self, master, song_data, add_callback):
        super().__init__(
            master,
            corner_radius=20,
            fg_color="#181818",
            border_width=1,
            border_color="#2a2a2a"
        )

        self.song_data = song_data
        self.add_callback = add_callback

        self.configure(fg_color="#1e1e1e")

        self.build_card()
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def build_card(self):

        # DOWNLOAD THUMBNAIL
        image_url = self.song_data.get("thumbnail", "")

        try:

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(
                image_url,
                headers=headers,
                timeout=10
            )

            image = Image.open(BytesIO(response.content))

            image = image.resize((160, 90))

            self.thumbnail = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(160, 90)
            )

        except Exception as e:

            print("Thumbnail error:", e)

            self.thumbnail = None

        # THUMBNAIL
        self.image_label = ctk.CTkLabel(
            self,
            image=self.thumbnail,
            text=""
        )
        self.image_label.pack(side="left", padx=15, pady=15)
        self.image_label.image = self.thumbnail

        # INFO FRAME
        self.info_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.info_frame.pack(side="left", fill="both", expand=True)

        # TITLE
        self.title_label = ctk.CTkLabel(
            self.info_frame,
            text=self.song_data.get("title", "Unknown"),
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        self.title_label.pack(fill="x", pady=(20, 5))

        # CHANNEL
        self.channel_label = ctk.CTkLabel(
            self.info_frame,
            text=self.song_data.get("channel", "Unknown artist"),
            text_color="#B3B3B3",
            anchor="w"
        )
        self.channel_label.pack(fill="x")

        # ADD BUTTON
        self.add_button = ctk.CTkButton(
            self,
            text="+ Agregar",
            width=120,
            fg_color="#1DB954",
            hover_color="#169c46",
            command=self.add_song
        )
        self.add_button.pack(side="right", padx=20)

    def add_song(self):
        self.add_callback(self.song_data)

    def on_hover(self, event):
        self.configure(fg_color="#242424")
    
    def on_leave(self, event):
        self.configure(fg_color="#181818")
    