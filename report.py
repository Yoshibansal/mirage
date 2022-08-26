import utils, score, json

def generate_report(qna, state=0):
    scores_qna = {}
    time, flags, date, total_score, emp = 0, 0, 0, 0, 0
    step = len(qna.keys())
    max_score = step*17
    c = 1
    for k,v in qna.items():
        print(f"Calculating..... Step: {c}/{step}")
        c += 1

        (_, s, t, f, d) = score.readabilityScore(v)

        if(state==1):
            summary = utils.summarize(v)
        else:
            # summarize only the headings that matters
            summary = ""
            mq = utils.mapQues(que = k)
            if(mq):
                summary = utils.summarize(v)
            else:
                emp += 1

            if(emp >= step-5):
                return generate_report(qna, state=1)
                

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

    report = dict({ 'status':'DONE',
                    'time':round(time/60),
                    'flags': flags,
                    'date':str(date),
                    'totalRisk':total_score,
                    'maxScore':max_score,
                    'ques': scores_qna})


    return report