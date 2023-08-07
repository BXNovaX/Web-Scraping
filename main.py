from bs4 import BeautifulSoup
from persiantools.jdatetime import JalaliDate
from dotenv import load_dotenv
import smtplib, ssl, re, asyncio, httpx, os
import time

load_dotenv()


"""
TODO Clean this mess!

ou can use regular expressions to replace or remove the parts that are not integers. For example, ; new_string = re.sub (r'\D+', '', old_string)
"""


PORT = 587
SMTP_SERVER = "smtp.gmail.com"
USERNAME = "mhmk.nova"
PASSWORD = os.getenv("PASSWORD")
print(USERNAME, PASSWORD)
SENDER_EMAIL = f"{USERNAME}@gmail.com"
CONTEXT = ssl.create_default_context()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


def send_mail(receiver_mail, message):
    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls(context=CONTEXT)
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_mail, message)


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url="https://bama.ir/car?brand=quick,atfullplus,manualrplus(at)&priced=1&sort=4",
            headers=HEADERS,
            timeout=5.0,
        )
    if response.status_code == 200:
        soup = BeautifulSoup(response, "lxml")
        with open("index.html", "w") as index:
            index.write(soup.prettify())
        boxes = soup.find(
            "div",
            class_="bama-adlist-container",
        )
        with open("output.txt", "w") as output:
            for box in boxes.find_all("div", class_="bama-ad-holder"):
                model = box.a.find("div", class_="bama-ad__title-row").p.text.strip()
                year = box.a.find("div", class_="bama-ad__detail-row").span.text.strip()
                distance = re.sub(
                    r"\D+",
                    "",
                    box.a.find("div", class_="bama-ad__detail-row")
                    .find_all("span")[1]
                    .text.strip()
                    .replace(",", "_"),
                )
                detail = (
                    box.a.find("div", class_="bama-ad__detail-row")
                    .find_all("span")[2]
                    .text.strip()
                )
                price = (
                    box.a.find("div", class_="bama-ad__price-row")
                    .find("div", "bama-ad__price-holder")
                    .span.text.strip()
                ).replace(",", "")
                link = box.a["href"]
                output.write(
                    f"""
Model: {model}
Manufacture Year: {year}
Distance Passed: {0 if distance == "" else distance}
Detail: {detail}
Price: {price}
link: {f"https://bama.ir{link}"}
"""
                )
        return 0
    else:
        print(response)
        return 1


if __name__ == "__main__":
    # send_mail("mhmk.nova@pm.me", "Hello World!")
    start_time = time.time()
    asyncio.run(main())
    print("--- %s seconds ---" % (time.time() - start_time))
