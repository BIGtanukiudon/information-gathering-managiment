from typing import List
from models.scraping import ScrapingContent as SC
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup


def scraping_contents(domain: str,
                      contents_attr_name: str,
                      title_attr_name: str,
                      published_date_attr_name: str,
                      content_url_attr_name: str) -> List[SC]:
    res = requests.get(domain)
    soup = BeautifulSoup(res.text, "html.parser")

    contents = soup.select(contents_attr_name)

    content_detail_list: List[SC] = []
    for content in contents:
        title_elements = content.select_one(title_attr_name)

        if published_date_attr_name != "":
            published_date_element = content.select_one(
                published_date_attr_name)
        else:
            published_date_element = content.find("time")

        # aタグが複数あり、別の要素内にネストしている場合
        if content_url_attr_name != "":
            content_url_element = content.select_one(content_url_attr_name)
            content_url_element = content_url_element.find("a")
        else:
            content_url_element = content.find("a")

        title: str = ""
        str_published_at: str = ""
        content_url: str = ""

        if title_elements is not None and title_elements.get_text() is not None:
            title = title_elements.get_text()

        published_at = ""
        if published_date_element is not None and published_date_element.get_text() is not None:
            str_published_at = published_date_element.get_text()

            if "-" in str_published_at:
                str_published_at = str_published_at.replace("-", "/")
            elif "." in str_published_at:
                str_published_at = str_published_at.replace(".", "/")

            str_published_at = str_published_at.strip()
            published_at = dt.strptime(str_published_at, "%Y/%m/%d")

        if content_url_element is not None and content_url_element.get(
                "href") is not None:
            content_url = content_url_element.get("href")
            if domain not in content_url:
                content_url = domain + content_url

        content_detail = SC(
            title=title,
            content_url=content_url,
            published_at=published_at,
            domain=domain
        )

        content_detail_list.append(content_detail)
    return content_detail_list
