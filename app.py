import utils, score, json
from transformers import logging
logging.set_verbosity_error()
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def generate_report():
    #?url=
    url = request.args.get('url')
    web_html = utils.getHTML(url)
    qna = utils.divideIntoQnA(web_html)

    scores_qna = {}
    time, flags, date, total_score = 0, 0, 0, 0
    step = len(qna.keys())
    max_score = step*17
    c = 1
    for k,v in qna.items():
        print(f"Calculating..... Step: {c}/{step}")
        c += 1
        (_, s, t, f, d) = score.readabilityScore(v)
        summary = utils.summarize(v)

        total_score += s
        time += t
        flags += f
        if (d):
            date = d

        scores_qna[k] = dict({'score': s,
                                'summary':summary})

    # print("Time (mins): ", round(time/60))
    # print("Flags: ", flags)
    # print("Last Updated: ", date)

    # print(scores_qna)

    report = dict({'time(mins)':round(time/60),
                    'flags': flags,
                    'date':str(date),
                    'total_risk':total_score,
                    'max_score':max_score,
                    'ques': scores_qna})



    return f"{json.dumps(report, indent=4)}"


if __name__ == '__main__':
    app.run()