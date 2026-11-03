"""Hürriyet search URL construction for the research notebook."""


def build_search_url(page, keywords, logic, start_date, finish_date, main_category):
    terms = "%20".join(keywords)
    return (
        f"https://www.hurriyet.com.tr/arama/#/?page={page}&key={terms}"
        f"&order=Yeniden%20Eskiye&where=hurriyet&how=Article&{logic}={terms}"
        f"&startDate={start_date}&finishDate={finish_date}&platform=hurriyet"
        f"&mainCategory=/{main_category}/&isDetail=true"
    )
