from datetime import datetime


class ScrapingContent:
    title: str
    content_url: str
    published_at: datetime
    domain: str

    def __init__(self,
                 title,
                 content_url,
                 published_at,
                 domain):
        self.title = title
        self.content_url = content_url
        self.published_at = published_at
        self.domain = domain
