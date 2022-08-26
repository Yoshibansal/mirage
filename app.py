import utils, scraper, report
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=['GET'])
def genReport():
    #?url=
    url = request.args.get('url')
    web_html = utils.getHTML(url)
    qna = utils.divideIntoQnA(web_html)

    return (report.generate_report(qna))


@app.route("/api2/", methods=['GET'])
def scaperApi():
    #?url=
    url = request.args.get('url')
    return scraper.scrap(url)

if __name__ == '__main__':
    app.run(debug=True, host="172.16.4.24")