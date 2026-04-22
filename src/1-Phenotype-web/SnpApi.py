import base64
import io
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file, send_from_directory

from DataScraper import SNPCrawl


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"

app = Flask(__name__, template_folder="templates")
dfCrawl = None


def load_crawl():
    filepath = DATA_DIR / "scrapedData.json"
    snppath = DATA_DIR / "yourData.json"
    return SNPCrawl(
        filepath=filepath if filepath.is_file() else None,
        snppath=snppath if snppath.is_file() else None,
    )



@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("snp_resource.html")

@app.route("/excel", methods=['GET', 'POST'])
def create_file():
    content = request.form

    filename = content["fileName"]
    filecontents = content["base64"]
    filecontents = base64.b64decode(filecontents)

    bytesIO = io.BytesIO()
    bytesIO.write(filecontents)
    bytesIO.seek(0)

    return send_file(bytesIO,
                     download_name=filename,
                     as_attachment=True)


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory(APP_DIR / "images", path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(APP_DIR / "js", path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(APP_DIR / "css", path)


@app.route("/api/rsids", methods=['GET'])
def get_types():
    global dfCrawl
    if dfCrawl is None:
        dfCrawl = load_crawl()
    return jsonify({"results": dfCrawl.rsidList})

if __name__ == "__main__":
    dfCrawl = load_crawl()
    app.run(debug=True)
