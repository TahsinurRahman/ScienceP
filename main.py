import speech_recognition as sr
import pandas as pd
import bangla
import datetime
from utils import add_affix, playaudio


df = pd.read_csv('qa.csv')
questions = df["Questions"].to_list()
answers = df["Answers"].to_list()


bn_today_prefixes = ['আজ', 'আজকে', 'আজকের', 'এখন', 'আজি']
date_q_suf = ['কত', 'কি']

bn_date_q = ['তারিখ কত', 'তারিখ কি', 'তারিখ', 'কি তারিখ', 'বাংলা তারিখ', 'বাংলা সন', 'বাংলা দিন']
bn_date_ques = add_affix(bn_date_q, bn_today_prefixes, date_q_suf)

en_date_q = ['ইংরেজি তারিখ', 'ইং তারিখ', 'ইংরেজি সন', 'ইংরেজি বর্ষ']
en_date_ques = add_affix(en_date_q, bn_today_prefixes, date_q_suf)


class QA:
    def __init__(self, cd):
        self.cd = cd
        if self.cd in bn_date_ques:
            self.date_in_bangla()
        elif self.cd in en_date_ques:
            self.date_in_english()
        elif self.cd in questions:
            self.what_ans()
        else:
            playaudio("আমি জানি না")
            

    def date_in_bangla(self):
        bangla_date = bangla.get_date()
        date_in_bn = "{} {}, {}".format(bangla_date['date'], bangla_date['month'], bangla_date['year'])
        response = f"আজকে বাংলা তারিখ {date_in_bn}"
        print(response)
        playaudio(response)

    def date_in_english(self):
        date = datetime.datetime.now().strftime('%d %m %Y')
        bangla_date = bangla.convert_english_digit_to_bangla_digit(date)
        bangla_date_list = bangla_date.split(' ')
        month = bangla_date_list[1]
        num_months = ['০১', '০২', '০৩', '০৪', '০৫', '০৬', '০৭', '০৮', '০৯', '১০', '১১', '১২']
        word_months = ['জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন', 'জুলাই', 'আগস্ট', 'সেপ্টেম্বর',
                       'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর']

        for num_month in num_months:
            if month == num_month:
                num_month_index = num_months.index(num_month)
                bangla_date_list[1] = word_months[num_month_index]
        bangla_date_string = " ".join([str(elem) for elem in bangla_date_list])
        response = f"আজকে ইংরেজি তারিখ {bangla_date_string}"
        print(response)
        playaudio(response)

    def what_ans(self):
        # get the matched question index
        matched_question_index = questions.index(self.cd)
        # get the desired answer for the asked question
        desired_answer = answers[matched_question_index]
        response = desired_answer
        print(response)
        playaudio(response)


while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='bn-BD')
        print(f"User said: {query}\n")
        QA(query)
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
