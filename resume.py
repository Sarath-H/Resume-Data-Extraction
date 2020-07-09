import re
#pip3 install docx2txt
import docx2txt
#pip3 install spacy
import spacy
#pip3 install pandas
from spacy.matcher import Matcher
#pip3 install pandas
import pandas as pd
#give input as a docx file
doc = docx2txt.process(input())
text = [line.replace('\t',' ') for line in doc.split('\n') if line]
text=' '.join(text)
#python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

def extract_details(text):
    nlp_text = nlp(text)
    name = re.search('^(Name:\s*)?[a-zA-Z]+(\s)+[a-zA-Z]+(\s)+[a-zA-Z]+(\s)',text).group() #^(Name:\s*)?(.+) #^\s?[a-zA-Z].[a-zA-Z]+$
    college = re.search(r'[a-zA-Z0-9-+.]+(\s)+(institute|college|university|school|vidyalaya|vidyalayam|Institute|College|University)+(\s)+[a-zA-Z0-9-+.]+(\s|\.|\,)',text).group()
    phone = re.findall("\d{10}",text)
    email = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.\w{3}',text).group()
    address= re.search(r'\w+[0-9]',text)
    percentage = re.findall(r'\d{2}%',text)
    try:
        D_O_B = re.search('\d{2}[.-/]\d{2}[.-/]\d{4}',text).group()
    except NoneTypeError:
        Print("None")

    # load pre-trained model


    #print(text)
    print("Name :",name)
    print("Phone:",phone)
    #print("Addres:",address)
    print("College:",college)
    print("Email:",email)
    print("Percentage:",percentage)
    print("D.O.B :",D_O_B)
    noun_chunks = nlp_text
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    # reading the csv file
    data = pd.read_csv("skills.csv")
    # extract values
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    print("Skills :",[i.capitalize() for i in set([i.lower() for i in skillset])])

extract_details(text)
