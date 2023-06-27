import requests

r = requests.get("https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/may-2023/6202022.xlsx")

print(r.status_code)

with open("abs_unemployment.xls", "wb") as fp:
    fp.write(r.content)