import os
import requests
from bs4 import BeautifulSoup


def find_articles(article_type, page_number):
    url = f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={page_number}"
    articles = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})

    if articles.status_code == 200:
        soup = BeautifulSoup(articles.content, 'html.parser')
        news_type = soup.findAll('span', {'class': 'c-meta__type'}, text=article_type)

        os.mkdir(f"Page_{page_number}")
        for news in news_type:
            link = news.parent.parent.parent.find(attrs={"data-track-action": "view article"})
            article = requests.get(f"https://www.nature.com{link.get('href')}",
                                   headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup = BeautifulSoup(article.content, 'html.parser')

            article_content = soup.find("p", {"class": "article__teaser"})
            filename = f"{soup.title.string.replace(' ', '_').strip()}.txt"

            file = open(os.path.join(f"Page_{page_number}", filename), "w", encoding='UTF-8')
            file.write(article_content.text)
            file.close()

        print("Content saved.")
    else:
        print(f"The URL {url} returned {articles.status_code}")


if __name__ == "__main__":
    page_number = int(input())
    article_type = input()

    for i in range(1, page_number + 1):
        find_articles(article_type, i)
