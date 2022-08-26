import utils, scraper, report, json
from flask import Flask, request
from firebase import firebase
firebase = firebase.FirebaseApplication("FIREBASE_KEY", authentication=None)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def genReport():
    #?url=
    url = request.args.get('url')
    #?id=
    id = request.args.get('id')

    try:
        web_html = utils.getHTML(url)
        qna = utils.divideIntoQnA(web_html)
        output = report.generate_report(qna)
        firebase.put('/privacy/'+id, 'data', json.dumps(output))
        firebase.put('/privacy/'+id, 'status', 'DONE')
    except:
        firebase.put('/privacy/'+id, 'status', 'ERROR')
    return "True"


@app.route("/api2/", methods=['GET'])
def scaperApi():
    #?url=
    url = request.args.get('url')
    #?id=
    id = request.args.get('id')
    try:
        output2 = scraper.scrap(url)
        firebase.put('/gdpr/'+id, 'data', json.dumps(output2))
        firebase.put('/gdpr/'+id, 'status', 'DONE')
    except:
        firebase.put('/gdpr/'+id, 'status', 'ERROR')
    return "True"

if __name__ == '__main__':
    app.run(debug=True, host="172.16.4.24")