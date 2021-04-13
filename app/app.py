from flask import Flask, render_template, request, make_response, jsonify
import os

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    
	@app.route('/')
	def index():
		return render_template('index.html', pagetitle="ytdownloader")

	@app.route('/sendurl', methods=['GET'])
	def send_url():
		url = request.args.get('url')
		json_response = {'status':'NOT OK', 'status_message':'URL Not found!'}
		if url:
			json_response['status'] = 'OK'
			json_response['status_message'] = 'success'
			json_response['url'] = url
		

		response = make_response(jsonify(json_response), 200)
		return response


	return app


