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

capital_ques = ['রাজধানীর নাম কি', 'রাজধানী', 'রাজধানীর']


class QA:
    def __init__(self, cd):
        self.cd = cd


        if 'রাজধানীর নাম কি' in self.cd or 'রাজধানী' in self.cd or 'রাজধানীর' in self.cd:
            self.country_capital()

        for i in bn_date_ques:
            if i in self.cd:
                self.date_in_bangla()

        for i in en_date_ques:
            if i in self.cd:
                self.date_in_english()

        for i in questions:
            if i in self.cd:
                self.what_ans()


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

    def country_capital(self):
        capitals = pd.read_csv('country_capital.csv')
        country_name = capitals["Country"].to_list()
        capital_name = capitals['Capital'].to_list()

        ques = add_affix(main=['এর রাজধানীর', 'রাজধানী'], pre=country_name)

        for i in ques:
            if i in self.cd:
                matched_country_index = ques.index(i) // 2
                answer_capital = capital_name[matched_country_index]
                playaudio(answer_capital)


while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='bn-BD')
        print(f"User said: {query}\n")
        if ' ' in query:
            QA(query)
    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
