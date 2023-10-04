import os
import json
import config
import requests
import urllib.request
import subprocess
import re

from bs4 import BeautifulSoup
from Class.JJFPost import JJFPost

def create_folder(tpost):
    fpath = os.path.join(config.save_path, tpost.name, tpost.type)

    if not os.path.exists(fpath):
        os.makedirs(fpath)
    
    return fpath

def video_save(vpost):

    vpost.ext = 'mp4'
    vpost.prepdata()

    folder = create_folder(vpost)
    vpath = os.path.join(folder, vpost.title)

    if not config.overwrite_existing and os.path.exists(vpath):
        print(f'v: <<exists skip>>: {vpath}')
        return

    vidurljumble = vpost.post_soup.select('div.videoBlock a')[0].attrs['onclick']
    vidurl = json.loads(vidurljumble.split(', ')[1])

    vpost.url_vid = vidurl.get('1080p', '')
    vpost.url_vid = vidurl.get('540p', '') if vpost.url_vid == '' else vpost.url_vid

    print(f'v: {vpath}')

    folder_path = os.path.dirname(vpath)
    temp_m3u8_path = os.path.join(folder_path, 'playlist.m3u8')
    temp_video_file = os.path.join(folder_path, 'video.mp4')
    temp_audio_file = os.path.join(folder_path, 'audio.mp4')

    # Step 1: Download the m3u8 content to a temporary file
    urllib.request.urlretrieve(vpost.url_vid, temp_m3u8_path)

    # Step 2: Parse the m3u8 content and find audio and video URLs using regex
    audio_url = None
    video_url = None
    with open(temp_m3u8_path, 'r') as m3u8_file:
        m3u8_content = m3u8_file.read()
        audio_match = re.search(r'https://autograph\.xvid\.com/.*?audio\.m3u8', m3u8_content)
        video_match = re.search(r'https://autograph\.xvid\.com/.*?video\.m3u8', m3u8_content)
        if audio_match:
            audio_url = audio_match.group(0)
        if video_match:
            video_url = video_match.group(0)

    # Step 3: Use yt-dlp to download audio and video files
    if audio_url:
        subprocess.run(['yt-dlp', '-o', temp_audio_file, audio_url])
    if video_url:
        subprocess.run(['yt-dlp', '-o', temp_video_file, video_url])

    # Step 4: Use ffmpeg to merge audio and video
    subprocess.run(['ffmpeg', '-i', temp_video_file, '-i', temp_audio_file, '-c:v', 'copy', '-c:a', 'aac', vpath])

    # Step 5: Clean up temporary files
    os.remove(temp_m3u8_path)
    if audio_url:
        os.remove(temp_audio_file)
    if video_url:
        os.remove(temp_video_file)


def parse_and_get(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    # name
    name = soup.select('h5.mbsc-card-title.mbsc-bold span')[0].text
    # date
    post_date = soup.select('div.mbsc-card-subtitle')[0].text.strip()

    for pp in soup.select('div.mbsc-card.jffPostClass'):
        
        ptext = pp.select('div.fr-view')

        thispost = JJFPost()
        thispost.post_soup = pp
        thispost.name = pp.select('h5.mbsc-card-title.mbsc-bold span')[0].text
        thispost.post_date_str = post_date.strip()
        thispost.post_id = pp.attrs['id']
        thispost.full_text = ptext[0].text.strip() if ptext else ''
        thispost.prepdata()

        classvals = pp.attrs['class']
        
        if 'video' in classvals:
            thispost.type = 'video'
            video_save(thispost)

if __name__ == "__main__":

    uid = ""
    hsh = ""
    api_url = config.api_url

    loopit = True
    loopct = 0
    while loopit:

        geturl = api_url.format(userid=uid, seq=loopct, hash=hsh)
        html_text = requests.get(geturl).text

        if 'as sad as you are' in html_text:
            loopit = False
        else:
            try:
                parse_and_get(html_text)
            except:
                pass
            loopct += 10
