import requests
from jinja2 import Environment, FileSystemLoader


def get_articles():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }

    url = "https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed"
    payload = {
        "sort_type": 200,
        "limit": 20,
        "cursor": "0",
        "id_type": 2,
        "client_type": 2608
    }

    res = requests.post(url, json=payload, headers=headers)
    data = res.json().get("data", [])

    articles = []
    for i in data:
        if i["item_type"] == 2:
            title = i["item_info"]["article_info"]["title"]
            url = "https://juejin.cn/post/{}".format(i["item_info"]["article_id"])
        elif i["item_type"] == 14:
            title = i["item_info"]["title"]
            url = i["item_info"]["url"]
        else:
            title = i["item_info"]["article_info"]["title"]
            url = i["item_info"]["article_info"]["url"]
        articles.append({
            "title": title,
            "url": url
        })
    from pprint import pprint
    pprint(articles)
    return articles


if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader("./"))
    template = env.get_template("template.html")
    with open("hot_articles.html", "w") as f:
        f.write(template.render(articles=get_articles()))