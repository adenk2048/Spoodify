from yt_dlp import YoutubeDL
#print("EE")

confirm = ''
while confirm != "Y" and confirm != "y":
    url = input('url')
    name = input('name')
    confirm = input('confirm? y/n')


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl':name,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
