print("DANG CHAY PHYSICAL TECH")
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

url = "https://www.sciencedaily.com/news/top/technology/"

response = requests.get(url)
response.encoding = "utf-8"

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a", href=True)

articles = []
seen = set()

for link in links:
    href = link["href"]
    title = link.get_text(" ", strip=True)

    if "/releases/" in href and href not in seen and title:
        full_url = urljoin(url, href)

        articles.append({
            "title": title,
            "url": full_url,
            "category": "Physical/Tech"
        })

        seen.add(href)

    if len(articles) >= 100:
        break

print("Số bài tìm được:", len(articles))

for article in articles:
    try:
        article_response = requests.get(article["url"], timeout=10)
        article_response.encoding = "utf-8"

        article_soup = BeautifulSoup(article_response.text, "html.parser")

        summary = article_soup.find("meta", attrs={"name": "description"})

        if summary:
            article["summary"] = summary["content"]
        else:
            article["summary"] = ""

    except Exception as e:
        print("Lỗi:", article["url"])
        print(e)
        article["summary"] = ""

with open("physical_tech_news.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)

    writer.writerow([
        "title",
        "summary",
        "category",
        "url"
    ])

    for article in articles:
        writer.writerow([
            article["title"],
            article["summary"],
            article["category"],
            article["url"]
        ])

print("Đã lưu dữ liệu vào physical_tech_news.csv")