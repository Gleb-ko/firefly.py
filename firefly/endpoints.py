class Endpoints:
    tasks = "api/v2/taskListing/view/self/tasks/filterBy"

def headers(url,content,cookies,content_type="json",accept="application/json, text/plain, */*"):
    """
    url must be in the form http(s)://(domain)/
    """
    return {
        "Accept": accept,
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/"+content_type,
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/74.0.3729.169 Chrome/74.0.3729.169 Safari/537.36",

        "Cookie": cookies,
        "Content-Length": str(len(content)),
        "Host": url.replace("https://","").replace("http://","").split("/")[0],
        "Origin": "/".join(url.split("/")[:3]),
        "Referer": url
    }
