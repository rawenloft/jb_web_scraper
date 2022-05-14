
import bs4 as b_soup
import os
import requests
import string


page_nums = int(input())
tag_search = input()  # Input topic for article search
base_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
data_list = []


def get_url(base_url, page_nums):
    """Get input number of pages to scrape int"""
    for i in range(1, page_nums + 1):
        payload = {"page": i}
        r = requests.get(base_url, payload)
        make_folder(i)
        get_articles(r, i)
    print(f"Stored all articles.")


def make_folder(i):
    """Create folder for every page"""
    current_dir = os.getcwd()
    try:
        os.mkdir(current_dir + f"\\Page_{i}")
    except FileExistsError:
        print(f"Directory Page_{i} already exist")


def get_articles(r, i):
    """Parse articles by page and search name of article"""
    if r.status_code != 200:
        err_x = r.status_code
        print(f"The URL returned {err_x}")
    else:
        soup = b_soup.BeautifulSoup(r.content, "html.parser")
        articles = soup.find_all("article")
        for article in articles:
            article_t = article.find("span", "c-meta__type").text
            if article_t == tag_search:
                find_article_text = article.find_all("a", {"data-track-action": "view article"})
                for page in find_article_text:
                    my_text = page.get("href")
                    get_data(my_text, i)


def get_data(my_text, j):
    """Get text of desired article if such article exists"""
    res_articles = requests.get(f"https://www.nature.com{my_text}")
    if res_articles.status_code != 200:
        err_x = res_articles.status_code
        print(f"The URL returned {err_x}")
    else:
        soup = b_soup.BeautifulSoup(res_articles.content, "html.parser")
        title = soup.find("h1").text
        for i in string.punctuation:
            if i in title:
                title = title.replace(i, '')
        title = title.split()
        title = "_".join(title)
        article = soup.find("div", {"class": "c-article-body u-clearfix"})
        body = article.text.strip()
        body = body.replace("\n", "")
        if title:
            with open(f"Page_{j}\\{title}.txt", "w", encoding="utf-8") as f:
                f.write(body)
        data_list.append(f"{title}.txt")


if __name__ == '__main__':
    get_url(base_url, page_nums)
