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
        r = await client.get("https://www.zoomit.ir/")
    soup = BeautifulSoup(r, "lxml")
    with open("content.html", "w") as content:
        content.write(soup.prettify())
    boxes = soup.find_all(
        "div",
        class_="box__BoxBase-sc-1ww1anb-0 kXWFxm BrowseArticleListItemDesktop__ContentBox-sc-1szqe4e-5 gpOrSi",
    )
    with open("tags.txt", "w") as tags_txt:
        for box in boxes:
            tags_txt.write(f"{box.a.span.text}\n")
            tags_txt.write(f"\t{box.p.text}\n\n")


if __name__ == "__main__":
    asyncio.run(main())
