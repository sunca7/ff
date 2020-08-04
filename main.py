import os
import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from save import save_to_file

LIMIT = 20
db = {}
level_four_db = [{'company': '삼성전자', 'company_url': '/item/main.nhn?code=005930'}, {'company': 'NAVER', 'company_url': '/item/main.nhn?code=035420'}, {'company': '셀트리온', 'company_url': '/item/main.nhn?code=068270'}, {'company': '현대모비스', 'company_url': '/item/main.nhn?code=012330'}, {'company': '엔씨소프트', 'company_url': '/item/main.nhn?code=036570'}, {'company': 'POSCO', 'company_url': '/item/main.nhn?code=005490'}, {'company': 'KB금융', 'company_url': '/item/main.nhn?code=105560'}, {'company': '신한지주', 'company_url': '/item/main.nhn?code=055550'}, {'company': 'KT&G', 'company_url': '/item/main.nhn?code=033780'}, {'company': '넷마블', 'company_url': '/item/main.nhn?code=251270'}, {'company': '삼성생명', 'company_url': '/item/main.nhn?code=032830'}, {'company': '하나금융지주', 'company_url': '/item/main.nhn?code=086790'}, {'company': '삼성화재', 'company_url': '/item/main.nhn?code=000810'}, {'company': '고려아연', 'company_url': '/item/main.nhn?code=010130'}, {'company': '우리금융지주', 'company_url': '/item/main.nhn?code=316140'}, {'company': '기업은행', 'company_url': '/item/main.nhn?code=024110'}, {'company': '미래에셋대우', 'company_url': '/item/main.nhn?code=006800'}, {'company': '포스코케미칼', 'company_url': '/item/main.nhn?code=003670'}, {'company': '현대글로비스', 'company_url': '/item/main.nhn?code=086280'}, {'company': '현대건설', 'company_url': '/item/main.nhn?code=000720'}, {'company': '유한양행', 'company_url': '/item/main.nhn?code=000100'}, {'company': 'DB손해보험', 'company_url': '/item/main.nhn?code=005830'}, {'company': '삼성카드', 'company_url': '/item/main.nhn?code=029780'}, {'company': '삼성증권', 'company_url': '/item/main.nhn?code=016360'}, {'company': 'NH투자증권', 'company_url': '/item/main.nhn?code=005940'}, {'company': '일진머티리얼즈', 'company_url': '/item/main.nhn?code=020150'}, {'company': '농심', 'company_url': '/item/main.nhn?code=004370'}, {'company': '메리츠증권', 'company_url': '/item/main.nhn?code=008560'}, {'company': '현대해상', 'company_url': '/item/main.nhn?code=001450'}, {'company': '제일기획', 'company_url': '/item/main.nhn?code=030000'}, {'company': '동서', 'company_url': '/item/main.nhn?code=026960'}, {'company': 'LS ELECTRIC', 'company_url': '/item/main.nhn?code=010120'}, {'company': 'BNK금융지주', 'company_url': '/item/main.nhn?code=138930'}, {'company': '한올바이오파마', 'company_url': '/item/main.nhn?code=009420'}, {'company': '종근당', 'company_url': '/item/main.nhn?code=185750'}, {'company': 'HDC현대산업개발', 'company_url': '/item/main.nhn?code=294870'}, {'company': 'DB하이텍', 'company_url': '/item/main.nhn?code=000990'}, {'company': '한전KPS', 'company_url': '/item/main.nhn?code=051600'}, {'company': '영원무역', 'company_url': '/item/main.nhn?code=111770'}, {'company': '한국테크놀로지그룹', 'company_url': '/item/main.nhn?code=000240'}, {'company': '이노션', 'company_url': '/item/main.nhn?code=214320'}, {'company': '영풍', 'company_url': '/item/main.nhn?code=000670'}, {'company': '쿠쿠홈시스', 'company_url': '/item/main.nhn?code=284740'}, {'company': '보령제약', 'company_url': '/item/main.nhn?code=003850'}, {'company': '휴켐스', 'company_url': '/item/main.nhn?code=069260'}, {'company': '빙그레', 'company_url': '/item/main.nhn?code=005180'}, {'company': '락앤락', 'company_url': '/item/main.nhn?code=115390'}, {'company': '쿠쿠홀딩스', 'company_url': '/item/main.nhn?code=192400'}, {'company': '세방전지', 'company_url': '/item/main.nhn?code=004490'}]

company_list_url = f"https://finance.naver.com/sise/entryJongmok.nhn?&page="

company_info_base_url = "https://finance.naver.com" 

kosdaq_list_url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1&page="

app = Flask("ff")

# os.system('cls' if os.name=='nt' else 'clear')

def request_company_list():
  company_list = []
  # for nb in range(1,21):
  for nb in range(1,21):
    request_company_list = requests.get(f"{company_list_url}{nb}")
    soup = BeautifulSoup(request_company_list.text, "html.parser")
    company_table_list = soup.find_all("td", {"class":"ctg"})
    for info in company_table_list:
      company = info.find('a').text
      company_url = info.find('a')["href"]
      company_list.append({"company": company, "company_url": company_url})
  return company_list

def extract_indiv_table(company):
  request_company_info = requests.get(f"{company_info_base_url}{company.get('company_url')}")
  soup = BeautifulSoup(request_company_info.text, "html.parser")
  info_table = soup.find("table", {"class": "tb_type1_ifrs"})
  info_table_row = info_table.find_all("tr")
  return info_table_row

def level_one_extract(company):
  info_table_row = extract_indiv_table(company)
  net_income_ten = info_table_row[5].find_all("td")
  for net_income in net_income_ten:
    if "-" in net_income.text.strip():
      return -1
    else:
      result = 1
  return result

def level_one_company(company_list):
  print("request level one")
  level_one = []
  # for company in company_list:
  # for company in company_list[:1]:
  for company in company_list:
    one = level_one_extract(company)
    if one == 1:
      level_one.append(company)
  print("level 1 len: ", len(level_one))   
  return level_one

def four_extract_company(company):
  info_table_row = extract_indiv_table(company)
  debt_ratio_ten = info_table_row[9].find_all("td")
  for debt_ratio in debt_ratio_ten:
    nbr = debt_ratio.text.strip().split('.')[0].replace(',','')
    if nbr != '':
      if int(nbr) > 100:
        return -4
    else:
      result = 4
  return result

def four_second_extract_company(company):
  info_table_row = extract_indiv_table(company)
  checking_ratio_ten = info_table_row[10].find_all("td")
  for checking_ratio in checking_ratio_ten:
    nbr = checking_ratio.text.strip().split('.')[0].replace(',','')
    if nbr != '':
      if int(nbr) < 100:
        return -4
    else:
      result = 4
  return result

def level_four_company(company_list):
  print("request level four")
  level_four = []
  for company in company_list:
    four = four_extract_company(company)
    four = four_second_extract_company(company)
    if four == 4:
      level_four.append(company)
  print("level 4 len: ", len(level_four))
  return level_four  

def six_extract_company(company):
  pass


def request_kosdaq():
  kosdaq_list = []
  for nb in range(1,5):
    print(f"{nb}")
    request_kosdaq_list = requests.get(f"{kosdaq_list_url}{nb}")
    soup = BeautifulSoup(request_kosdaq_list.text, "html.parser")
    kosdaq_table_list = soup.find_all("tr")
    for info in kosdaq_table_list[7:-1]:
      if info.find("a"):
        company = info.find('a').text
        company_url = info.find('a')["href"]
        kosdaq_list.append({"company": company, "company_url": company_url})
      else :
        continue
  print(kosdaq_list)
  return kosdaq_list

def ff_program(company_list):
  level_one = level_one_company(company_list)
  level_four = level_four_company(level_one)
  return level_four

# @app.route("/")
# def kospi():
#   print("Level four len", len(level_four_db))
#   print(level_four_db)
#   save_to_file(level_four_db)
#   return render_template("index.html", level_four=level_four_db)


# def kosdaq():
#   kosdaq_list = request_kosdaq()
#   return kosdaq_list

@app.route("/")
def financial_freedom():
  # kospi_list = request_company_list()
  kosdaq_list = request_kosdaq()
  kosdaq_level_four = ff_program(kosdaq_list)
  print(kosdaq_level_four)
  save_to_file(kosdaq_level_four)


# app.run(host="0.0.0.0")

financial_freedom()

  # if "company" not in db:
  #   print("request company")
  #   db["company"] = request_company_list()
  # company_list = db["company"]
  # if "one" not in db:
  #   print("request level one")
  #   db["one"] = level_one_company(company_list)
  # level_one = db["one"]
  # print("Level one len ", len(level_one))
  # 