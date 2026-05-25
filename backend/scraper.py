import requests
from bs4 import BeautifulSoup

urls = [
    "https://www.cloudinvent.co/",
    "https://www.cloudinvent.co/about/",
    "https://www.cloudinvent.co/security/",
    "https://www.cloudinvent.co/trust/",
    "https://www.cloudinvent.co/privacy-policy/"
]

all_text = ""

for url in urls:

    try:

        response = requests.get(url, timeout=30)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        all_text += text + "\n\n"

        print(f"Scraped: {url}")

    except Exception as e:

        print(f"Error scraping {url}: {e}")

with open(
    "../data/cloudinvent_docs.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(all_text)

print("Website data extracted successfully.")