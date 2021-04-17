from flask import Flask, render_template, request, make_response, jsonify
from flask import Response, stream_with_context, flash, redirect, url_for
import os
import os.path
from app.utils import utils

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    APP_PATH = os.path.abspath(os.path.dirname(__file__))
    app.config['STREAMS_PATH'] = os.path.join(APP_PATH, 'streams')
    @app.route('/')
    def index():
        return render_template('index.html', pagetitle='ytdownloader')

    @app.route('/download/file/<filename>', methods=['GET'])
    def download_file(filename):
        def generate(stream_url):
            for chunk in utils.request_stream(stream_url):
                yield chunk
                
        filepath = os.path.join(app.config['STREAMS_PATH'], filename+'.json')
        if os.path.exists(filepath):
            stream = utils.read_json_file(filepath)
            response = Response(stream_with_context(generate(stream['stream_url'])), mimetype=stream['mime_type'])
            response.headers['Content-Disposition'] = f"attachment; filename={stream['title']}.{stream['mime_type'].split('/')[1]}"
            return response

        return redirect(url_for('index'))

    @app.route('/sendurl', methods=['GET'])
    def send_url():
        url = request.args.get('url')
        json_response = {'status':'NOT OK', 'status_message':'URL Not found!'}
        if url:
            if utils.is_youtube_url(url):
                list_streams = utils.get_list_of_dict_streams(url)
                streams_path = app.config['STREAMS_PATH']
                utils.create_dict_stream_files(streams_path, list_streams)

                json_response['status'] = 'OK'
                json_response['status_message'] = 'success'
                json_response['download_options'] = {}

                for s in list_streams:
                    option = json_response['download_options'][s['id']] = {}
                    option['type'] = s['type']
                    option['mime_type'] = s['mime_type']
                    option['quality'] = s['quality']
                    option['filesize'] = s['filesize']
                    option['download_url'] = f"/download/file/{s['id']}"
            else:
                json_response['status_message'] = f'Invalid Youtube URL!'

        response = make_response(jsonify(json_response), 200)
        return response


    return app


