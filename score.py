import textstat as ts
import utils

def seventeen(num):
    if num>17:
        return 17
    return num

def readabilityScore(text):
  #how difficult a passage in English is to understand (more)
  fre = ts.flesch_reading_ease(text) #0-121.22
  '''
    0-30: College graduate
    30-50: College
    50-60: 10th - 12th grade
    60-70: 8th - 9th grade
    70-80: 7th grade
    80+: 5th - 6th grade 

    The idea is that shorter words and shorter sentences are easier to read.
  '''

  fre = seventeen(int((100-fre)*0.17))
#   print("FRE: ", fre)

  #how difficult a passage in English is to understand (more)
  fkg = ts.flesch_kincaid_grade(text) #0-121.22
  '''
    0-10: Professional
    10-30: College graduate
    30-50: College
    50-60: 10th - 12th grade
    60-70: 8th - 9th grade
    70-80: 7th grade
    80+: 5th - 6th grade 
  '''
  fkg = seventeen(int((100-fkg)*0.17))
#   print("FKG: ", fkg)

  #Year of education needed to understand (less)
  si = ts.smog_index(text) #0-
  '''
    0-6: 5th - 6th grade
    7-7: 7th grade
    8-9: 8th - 9th grade
    10-12: 10th - 12th grade
    12-15: College
    16-17: College graduate
    17+: Professional
  '''

  si = seventeen(int(si))
#   print("SI: ", si)


  #gauge the understandability of a text (less)
  cli = ts.coleman_liau_index(text) #0-
  '''
    0-6: 5th - 6th grade
    7-7: 7th grade
    8-9: 8th - 9th grade
    10-12: 10th - 12th grade
    12-15: College
    16-17: College graduate
    17+: Professional
  '''
  cli = seventeen(int(cli))
#   print("CLI: ", cli)

  #gauge the understandability of a text (less)
  ari = ts.automated_readability_index(text) #0-
  '''
    1	Kindergarten
    2	First Grade
    3 Second Grade
    4 Third Grade
    5 Fourth Grade
    6	Fifth Grade
    7	Sixth Grade
    8	Seventh Grade
    9	Eighth Grade
    10 Ninth Grade
    11 Tenth Grade
    12 Eleventh Grade
    13 Twelfth Grade
    14 College student
    15 College graduate
    16+ Professional
  '''
  ari = seventeen(int(ari*1.0625))
#   print("ARI: ", ari)

  #gauge of the comprehension difficulty that readers come upon when reading a text (less)
  dcrs = ts.dale_chall_readability_score(text) #0-10
  '''
    0.0-4.9	4th-grade or lower
    5.0-5.9	5th or 6th-grade
    6.0-6.9	7th or 8th-grade
    7.0-7.9	9th or 10th-grade
    8.0-8.9	11th or 12th-grade
    9.0-9.9	College
  '''
  dcrs = seventeen(int(dcrs*1.7))
#   print("DCRS: ", dcrs)

  #based on sentence length and the number of words used that have three or more syllables (less)
  lwf = ts.linsear_write_formula(text) #0-
  '''
    0-6: 5th - 6th grade
    7-7: 7th grade
    8-9: 8th - 9th grade
    10-12: 10th - 12th grade
    12-15: College
    16-17: College graduate
    17+: Professional
  '''
  lwf = seventeen(int(lwf))
#   print("LWF: ", lwf)


  #The index estimates the years of formal education a person needs to understand the text on the first reading (less)
  gf = ts.gunning_fog(text) #0-
  '''
    0-6 5th - 6th grade
    7 7th grade
    8 8th grade
    9 9th grade
    10 10th grade
    11 11th grade
    12 12th grade
    13-15 College
    15-16 College graduate
    17+ Professional
  '''
  gf = seventeen(int(gf))
#   print("GF: ", gf)

  #score for the readability of an english text for a foreign learner or English, focusing on the number of miniwords and length of sentences (less)
  mce = ts.mcalpine_eflaw(text)
  '''
    1-20: Very Easy
    21-25: Understandable
    26-29: Difficult
    30+: Very Confusing
  '''
  mce = seventeen(int(mce*0.567))
#   print("MCE: ", mce)

  scoreMatrix = [fre, fkg, si, cli, ari, dcrs, lwf, gf, mce]

  score = int((fre + fkg + si + cli + ari + dcrs + lwf + gf + mce)/(9))
#   print("AVG :: ", avg)

  #   #grade level of english text (less)
  #   sr = ts.spache_readability(text)
  
  #   print("SR: ", sr)

  #   #Number of difficult words in the text (less)
  #   dw = dw = ts.difficult_words(text)

  #   print("DW: ", dw)  

  #   #how difficult the text is (less)
  #   tes = ts.text_standard(text)
  #   print("TES: ", tes)

  #reading time (less) (mins)
  time = ts.reading_time(text, ms_per_char=14.69)

  flags, date = utils.redFlags(text)

  return (scoreMatrix, score, time, flags//2, date)