import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import joblib
from urllib.parse import urlparse
import re
np.random.seed(42)
tf.random.set_seed(42)
tld_file = open('Backend/tlds.txt', 'r')
def fix_url(url): # если протокол (схема) не используется, предположим, что это общий случай http, это необходимо для работы функции urlparse
  if not urlparse(url).scheme:
        return f"http://{url}"
  return url
"""# Извлечение компонентов URL"""
def get_protocol(url):
  protocol, _, _, _, _, _ = urlparse(url.replace("[","").replace("]","").strip() )
  return protocol
def get_host(url):
  _, host, _, _, _, _ = urlparse(url.replace("[","").replace("]","").strip())
  return host
def get_path(url):
  _, _, path, _, _, _ = urlparse(url.replace("[","").replace("]","").strip())
  return path
def get_parameters(url):
  _, _, _, parameters, _, _ = urlparse(url.replace("[","").replace("]","").strip())
  return parameters
def get_query(url):
  _, _, _, _, query, _ = urlparse(url.replace("[","").replace("]","").strip())
  return query
def get_fragment(url):
  _, _, _, _, _, fragment = urlparse(url.replace("[","").replace("]","").strip())
  return fragment
"""# Функции URL-адреса"""
def ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
        '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
        '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
    if match:
        return 1
    else:
        return 0
def specialSymbols(df):
  symbolsList = ['_','&','~','"',"'",'@','?','-','=','.','#','%','+','$','!','*',',','//','/',';',':','>','<','^','[',']','{','}','(',')']
  for symbol in symbolsList:
     df[f"URL_{symbol}"] = df['url'].apply(lambda i: i.count(symbol))
def getLength(url):
  return len(url)
def Shortining_Service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 1
    else:
        return 0
def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits
def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters
def EmailAddress(url):
    if re.findall(r'[\w\.-]+@[\w\.-]+', url):
        return 1
    else:
        return 0
def vowels_count(url):
    vowels = ['a', 'e', 'i', 'o', 'u']
    count = 0
    for i in vowels:
        count += url.lower().count(i)
    return count
def TLD_count(url):
    tldcount = 0
    tld_list=tld_file.readlines()
    line=0
    while (line < len(tld_list)):
       if tld_list[line].rstrip() in url :
          tldcount+=1
          line+=10
       line+=1
    if(".php" in url):
      tldcount-=1;
    if(".html" in url):
      tldcount-=1;
    tld_file.seek(0)
    return tldcount
def check_word_server_client(url):
    if "server" in url.lower() or "client" in url.lower():
        return 1
    return 0
def https(url):
    if str(urlparse(url).scheme)=='https':
        return 1
    else:
        return 0
def http(url):
    if str(urlparse(url).scheme)=='http':
        return 1
    else:
        return 0
def ftp(url):
    if str(urlparse(url).scheme)=='ftp':
        return 1
    else:
        return 0
"""# Характеристики пути"""
def specialSymbols2(df):
  symbolsList = ['_','&','~','"',"'",'@','?','-','=','.','#','%','+','$','!','*',',','//','/',';',':','>','<','^','[',']','{','}','(',')']
  for symbol in symbolsList:
     df[f"path_{symbol}"] = df['path'].apply(lambda i: i.count(symbol))
"""# Характеристики хоста"""
def specialSymbols3(df):
  symbolsList = ['_','&','~','"',"'",'@','?','-','=','.','#','%','+','$','!','*',',','//','/',';',':','>','<','^','[',']','{','}','(',')']
  for symbol in symbolsList:
     df[f"host_{symbol}"] = df['host'].apply(lambda i: i.count(symbol))
def predict_malicious(url):
  df = pd.DataFrame([url], columns = ['url'])
  df["original_url"]=df["url"]
  df["url"]=df["url"].apply(fix_url)
  df["protocol"]=df["url"].apply(get_protocol)
  df["host"]=df["url"].apply(get_host)
  df["path"]=df["url"].apply(get_path)
  df["parameters"]=df["url"].apply(get_parameters)
  df["query"]=df["url"].apply(get_query)
  df["fragment"]=df["url"].apply(get_fragment)
  df = df.replace('', np.nan) # заполните пустые значения Nan
  df.drop(['parameters', 'query','fragment'], axis = 1,inplace=True)
  df.dropna(subset = ['host'],inplace=True)
  df.fillna("",inplace=True)
  df.reset_index(drop=True,inplace=True)
  df['ip_address'] = df['url'].apply(ip_address)
  specialSymbols(df)
  df["length"] = df["url"].apply(getLength)
  df['Shortining'] = df['url'].apply(Shortining_Service)
  df['digits_in_url']= df['url'].apply(digit_count)
  df['letters_in_url']= df['url'].apply(letter_count)
  df['email_address']= df['url'].apply(EmailAddress)
  df['vowels_url']= df['url'].apply(vowels_count)
  df['tld_count']= df['url'].apply(TLD_count)
  df['server_client']= df['url'].apply(check_word_server_client)
  df['https'] = df['original_url'].apply(https)
  df['http'] = df['original_url'].apply(http)
  df['ftp'] = df['original_url'].apply(ftp)
  specialSymbols2(df)
  df["path_length"] = df["path"].apply(getLength)
  df['path_digits_in_url']= df['path'].apply(digit_count)
  df['path_letters_in_url']= df['path'].apply(letter_count)
  df['path_vowels_url']= df['path'].apply(vowels_count)
  specialSymbols3(df)
  df["host_length"] = df["host"].apply(getLength)
  df['host_digits_in_url']= df['host'].apply(digit_count)
  df['host_letters_in_url']= df['host'].apply(letter_count)
  df['host_vowels_url']= df['host'].apply(vowels_count)
  df.drop(["path_?","path_#","path_[","path_]","host_?","host_#","host_,","host_//","host_/","host_[","host_]",],axis=1,inplace=True)
  df.drop(["protocol"],axis=1,inplace=True)
  df.drop(["url","path","host","original_url"],axis=1,inplace=True)
  df["host_><^{}()!;:~"]=df["host_<"]+df["host_>"]+df["host_^"]+df["host_}"] +df["host_{"]+df["host_("] +df["host_)"]+df["host_!"]+df["host_;"]+df["host_:"]+df["host_~"]
  df.drop(["host_<","host_>","host_^","host_}","host_{","host_(","host_)","host_!","host_:","host_;"],axis=1,inplace=True)
  df["path_><^{}()!;:'~"]=df["path_<"]+df["path_>"]+df["path_^"]+df["path_}"] +df["path_{"]+df["path_("] +df["path_)"]+df["path_!"]+df["path_;"]+df["path_:"]+df["path_'"]+df['path_"']+df['path_~']
  df.drop(["path_<","path_>","path_^","path_}","path_{","path_(","path_)","path_!","path_:","path_;",'path_"',"path_'",'path_~'],axis=1,inplace=True)
  df["URL_><^{}()[]!;:'~"]=df["URL_<"]+df["URL_>"]+df["URL_^"]+df["URL_}"] +df["URL_{"]+df["URL_("] +df["URL_)"]+df["URL_["]+df["URL_]"]+df["URL_!"]+df["URL_;"]+df["URL_:"]+df["URL_'"]+df['URL_"']+df['URL_~']
  df.drop(["URL_<","URL_>","URL_^","URL_}","URL_{","URL_(","URL_)","URL_!","URL_:","URL_;","URL_[","URL_]","URL_'",'URL_"','URL_~'],axis=1,inplace=True)
  df['https+ftp']=df['https']+df['ftp']
  df.drop(["https","ftp"],axis=1,inplace=True)
  columns=df.columns
  # Загрузить масштабатор из файла
  scaler = joblib.load('Backend/scaler.joblib')
  # Преобразовать новые данные с помощью загруженного масштабатора
  df = scaler.transform(df)
  df=pd.DataFrame(df,columns=columns)
  keras.backend.clear_session()
  model = keras.models.load_model("Backend/my_model_tf_16_1.keras")
  predictions = model.predict(df)
  predictions = np.argmax(predictions)
  if predictions == 0:
    u_type = 'Benign'
  elif predictions == 1:
    u_type = 'Defacement'
  elif predictions == 2:
    u_type = 'Malware'
  elif predictions == 3:
    u_type = 'Phishing'
  #print("Имя класса:", u_type)
  return u_type


#some_url = 'https://www.sciencedirect.com/science/article/abs/pii/S1084804521002666#sec3'
#print(predict_malicious(some_url))