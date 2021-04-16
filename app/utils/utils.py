import pytube
import urllib.parse as urlparse
import json
import hashlib
import os

def read_json_file(filename, path='app/streams/'):
    with open(f'{path}{filename}.json', 'r') as file:
        data = json.load(file)
        file.close()
        return data

def create_json_file(filename, data={}, path='app/streams/'):
    with open(f'{path}{filename}.json', 'w') as file:
        json.dump(data, file)
        file.close()
        return 0

def create_dict_stream_files(list_streams):
    for dict_stream in list_streams:
        create_json_file(dict_stream['id'], dict_stream)
    return 0

def is_youtube_url(url):
    youtube_urls = ['youtube.com', 'youtu.be', 'www.youtube.com']
    netloc = urlparse.urlparse(url).netloc
    if netloc in youtube_urls:
        return True
    return False

def pytube_stream_to_dict(stream):
    s = stream
    url_stream_hash = hashlib.sha256(bytes(s.url, encoding="utf-8"))
    id_stream = url_stream_hash.hexdigest()

    data_file = {'id':id_stream,
    'itag':s.itag,
    'stream_url':s.url,
    'mime_type':s.mime_type,
    'title':s.title,
    'type':s.type,
    'progressive':s.is_progressive,
    'filesize':s.filesize}
    if s.is_progressive or s.includes_video_track:
        data_file['quality'] = s.resolution
        data_file['fps'] = s.fps
        if not s.is_adaptive:
            data_file['vcodec'] = s.video_codec
            data_file['acodec'] = s.audio_codec
        else:
            data_file['vcodec'] = s.video_codec
    else:
        data_file['quality'] = s.abr
        data_file['acodec'] = s.audio_codec

    return data_file


def get_list_of_dict_streams(url):
    list_streams = []
    pytube_streams = get_all_pytube_streams(url)
    for stream in pytube_streams:
        stream_dict = pytube_stream_to_dict(stream)
        list_streams.append(stream_dict)

    return list_streams


def get_all_pytube_streams(url):
    http_proxy = os.environ.get('PYTUBE_PROXY_HTTP')
    https_proxy = os.environ.get('PYTUBE_PROXY_HTTPS')
    proxy_dict = {}
    if http_proxy:
        proxy_dict['http'] = http_proxy
    if https_proxy:
        proxy_dict['https'] = https_proxy

    streams = pytube.YouTube(url, proxies=proxy_dict).streams
    return streams


def request_stream(url_stream):
    return pytube.request.stream(url_stream)
