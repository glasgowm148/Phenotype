from flask import Flask, render_template, request, send_file, send_from_directory, jsonify
import base64
from DataScraper import SNPCrawl
import os
import io
from pathlib import Path

app = Flask(__name__, template_folder='templates')



@app.route("/", methods=['GET', 'POST'])
def main():

    print(vars(request.form))
    filepath = Path(__file__).resolve().with_name('templates') / 'snp_resource.html'
    return render_template('snp_resource.html')

@app.route("/excel", methods=['GET', 'POST'])
def create_file():
    content = request.form

    filename = content['fileName']
    filecontents = content['base64']
    filecontents = base64.b64decode(filecontents)

    bytesIO = io.BytesIO()
    bytesIO.write(filecontents)
    bytesIO.seek(0)

    return send_file(bytesIO,
                     attachment_filename=filename,
                     as_attachment=True)


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('images', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route("/api/rsids", methods=['GET'])
def get_types():
    return jsonify({"results":dfCrawl.rsidList})

if __name__ == "__main__":
    filepath = Path(__file__).resolve().with_name('data') / 'scrapedData.json'
    snppath = Path(__file__).resolve().with_name('data') / 'yourData.json'

    if filepath.is_file():
        if snppath.is_file():
            dfCrawl = SNPCrawl(filepath=filepath, snppath=snppath)
    else:
        dfCrawl = SNPCrawl(filepath=filepath)
    app.run(debug=True)
