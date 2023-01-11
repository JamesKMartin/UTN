from flask import Flask, render_template, request
import json

content = []

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('index.html', data=content)
	
def get_data():
    with open('data.json', 'r') as f:
        jsons = json.load(f)
        global content
        content = list((jsons['content']))


def save_data():
	with open('data.json', 'w') as f:
		jsons = {
			'content': content
		}
		json.dump(jsons, f)

if __name__ == '__main__':
	get_data()
	print(str(content))
	app.run()

