from bs4 import BeautifulSoup
import os
import re
import requests


def main():
    '''
    download musics from playlists of vmusic.ir, by changing the playlist
    you can download any playlists is avalable in this website
    '''
    playlist = input('enter your playlist name: ')
    req = requests.get(f'https://vmusic.ir/playlist/{playlist}/')
    file_name = f'{playlist}_need_fix.txt'
    get_musics_and_write(file_name, req)
    fix_file_and_downlad_musics(playlist, file_name)


def get_musics_and_write(file_name, req):
    soup = BeautifulSoup(req.content, 'html.parser')
    i = 0
    for a in soup.find_all('a', href=re.compile('http.*\.mp3')):
        i += 1
        url = a['href'].replace(" ", "%20").split()
        for j in url:
            # download just 320KB quality
            if "320k" in j:
                with open(file_name, 'a') as f:
                    f.write(j)
                    f.write('\n')


def fix_file_and_downlad_musics(playlist, file_name):
    path = '/home/core/mydir/music'
    os.system(f'uniq {file_name} > {playlist}.txt')
    os.system(f'mkdir {path}/{playlist}')
    os.system(
        f'wget --retry-connrefused --waitretry=1 --read-timeout=20 --timeout=15 -t 0 -P {path}/{playlist} -i {playlist}.txt'
    )


if __name__ == '__main__':
    main()
