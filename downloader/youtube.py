import yt_dlp


def search_youtube(query):

    ydl_opts = {
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        results = ydl.extract_info(
            f"ytsearch30:{query}",
            download=False
        )

        videos = []

        for entry in results['entries']:

            thumbnail = ""

            thumbnails = entry.get("thumbnails", [])

            if thumbnails:
                thumbnail = thumbnails[-1].get("url", "")

            videos.append({
                'title': entry.get('title', 'Unknown'),
                'url': f"https://youtube.com/watch?v={entry.get('id')}",
                'thumbnail': thumbnail,
                'channel': entry.get('channel', 'Unknown')
            })

        return videos