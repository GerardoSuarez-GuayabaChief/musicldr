import yt_dlp


def search_youtube(query):

    ydl_opts = {
        'quiet': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        results = ydl.extract_info(
            f"ytsearch35:{query}",
            download=False
        )

        videos = []

        for entry in results['entries']:
            videos.append({
                'title': entry.get('title'),
                'url': f"https://youtube.com/watch?v={entry.get('id')}",
                'thumbnail': entry.get('thumbnails', [{}])[-1].get('url', ''),
                'channel': entry.get('channel', 'Unknown')
            })

        return videos