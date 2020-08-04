import csv

def save_to_file(companies):
  file = open("ff_kosdaq.csv", mode="w")
  writer = csv.writer(file)
  writer.writerow(["company", "company_url"])
  for company in companies:
    writer.writerow(list(company.values()))