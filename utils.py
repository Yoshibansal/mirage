from decimal import ROUND_UP
import re
from tkinter.messagebox import QUESTION
from newspaper import Article, fulltext
from bs4 import BeautifulSoup as bs
from datetime import datetime
from dateutil.parser import parse
from summarizer import Summarizer



# get html file
def getHTML(url):
  '''
    Use: To get the HTML file of the privacy policy page
    Parameter: 
          url: Link of the page
    Return:
          HTML in form of string
  '''
  web_privacy = Article(url)
  web_privacy.download()
  web_privacy.parse()

  web_html = web_privacy.html

  return web_html


# extracting headings from the page
def extractHeadings(web_html):
  '''
    Use: To extract the headings from the page.
    Parameter: 
          web_html -> HTML file of the privacy policy page

    Return:
          headings -> headers extracted from the page
          sub -> Strong text in the page
  '''
  soup = bs(web_html, 'lxml')

  tags = ['h5', 'h4', 'h3', 'h2']
  tag_b = ['strong']

  headings, sub = [], []
  for i in soup.find_all(tags):
      # print(i.name)
      if (i.string):
        headings.append(i.string)
      else:
        headings.append(i.text.strip())

  for i in soup.find_all(tag_b):
      sub.append(i.text.strip())

  return headings, sub



# extracting everything between two same tags
def divideIntoQnA(web_html):
  '''
    Use: Divide the privacy policies into subheadings
    and return a dictinary of heading as a key, and data as value.

    Parameter: 
          web_html -> HTML file of the privacy policy page
          headings -> 
  '''
  headings, _ = extractHeadings(web_html)
  qna = {}

  for i in range(len(headings)):
    if(i == len(headings)-1):
      try:
        qna[headings[i].strip()] = fulltext(web_html[web_html.index(headings[i])+len(left):])
      except:
        pass
    else:  
      left = headings[i]
      right = headings[i+1]

      try:
        qna[headings[i].strip()] = fulltext(web_html[web_html.index(left)+len(left) : web_html.index(right)])
      except:
        pass

  return qna








# Convert Date to single format
def to_date(string):
    '''
        Utility for flag calculator
    '''
    if not string:
        return None
    try:
        if "-" in string or "/" in string:
            string = string.split(" ")[0]
        check = datetime.strptime(string, '%d-%m-%Y')
        return check
    except ValueError:
        try:
            check = datetime.strptime(string, '%d/%m/%Y')
            return check
        except ValueError:
            try:
                check = datetime.strptime(string, '%Y-%m-%d')
                return check
            except ValueError:
                try:
                    return parse(string, fuzzy=False, dayfirst=True).date()
                except Exception as e:
                    return None



def redFlags(text):
  '''
    Use: Count for flags in privacy policy of terms and conditions
    return:
        flags: Total number of flags per question
        Date: Last updated 
  '''
  flags = 0

  #Keyword such as is a flag
  if('such as' in text):
    flags += text.count('such as')


  #if not updated recently is also a flag
  date = re.search(r'\w+ \d{1}, \d{4}', text)
  if(date):
    # Date Privacy Policy Updated
    date = to_date(date.group())
    # print(date)

    # Today's Date
    today_date = datetime.date(datetime.now())
    # print(today_date)

    # Difference Between the dates
    dif = today_date - date
    # print(dif)

    flags += dif.days//365
  else:
    date = None
    # print("Not Found")
  
  return flags, date

model = Summarizer()

# Summarizer of privacy policy using bert model
def summarize(text):
    '''
        Using the BERT model
        It summarizes our text
    '''
    global model
    result = model(text, min_length=round(len(text.split())*(0.40)))
    full = ''.join(result)
    return full



# Questions to map on
def mapQues(que):
  '''
    return ques if one of the followings
    else return 0
  '''

  # collect info
  q1 = [["information"], ["collection", "collect"]]

  # use info
  q2 = [["information"], ["use"]]

  # store info
  q3 = [["information"], ["store"]]

  # access
  q4 = [['access'], ['information', 'profile', 'account']]

  # share info
  q5 = [['information'], ['share', 'disclosure']]

  # change
  q6 = [['privacy'], ['change', 'update', 'changes']]

  # contact
  q7 = [['us'], ['contact', 'contacting']]

  f = 0
  # QUESTION = [q1, q2, q3, q4, q5, q6, q7]
  QUES = [["information", "access", "manage", "privacy", "policy", "us", "how to", "deleting"], ["collection", "collect", "use", "store", 'profile', 'account', 'share', 'shared', 'disclosure', 'change', 'changes', 'update', 'changes', 'contact', 'contacting', "access", "manage", "deleting"]]
  for q in QUES:
    for i in q:
      if(i in que.lower()):
        f += 1
        break

  if(f==2):
    print(que)
    return que

  return 0

