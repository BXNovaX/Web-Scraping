from bs4 import BeautifulSoup
import httpx
import asyncio


"""
TODO Clean this mess!

typography__StyledDynamicTypographyComponent-t787b7-0 ibfopD BrowseArticleListItemDesktop___StyledTypography-sc-1szqe4e-0 hYItiO
typography__StyledDynamicTypographyComponent-t787b7-0 ibfopD BrowseArticleListItemDesktop___StyledTypography-sc-1szqe4e-0 hYItiO

box__BoxBase-sc-1ww1anb-0 kXWFxm BrowseArticleListItemDesktop__ContentBox-sc-1szqe4e-5 gpOrSi
box__BoxBase-sc-1ww1anb-0 kXWFxm BrowseArticleListItemDesktop__ContentBox-sc-1szqe4e-5 gpOrSi
"""


async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://bama.ir/car?transmission=automatic")
    soup = BeautifulSoup(r, "lxml")
    boxes = soup.find_all(
        "div",
        class_="bama-adlist-container",
    )
    with open("output.txt", "w") as tags_txt:
        for box in boxes:
            tags_txt.write(
                f"""
{box.a.find("div", class_="bama-ad__price-row").find("div", class_="bama-ad__price-holder").span.text}
\n\n
"""
            )


if __name__ == "__main__":
    asyncio.run(main())
