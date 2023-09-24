import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from fake_useragent import UserAgent


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': UserAgent().random,
}


def get_all_categories(link):
    req = requests.get(url=link, headers=headers)
    if req.status_code == 200:
        src = req.text

        soup = bs(src, "lxml")
        all_catalogue_dl = soup.find(class_="rcpf").find_all(class_="catalogue")
        for item_dl in all_catalogue_dl:
            all_dd_elements = item_dl.find_all("dd")
            for item_dd in all_dd_elements:
                all_a_tags = item_dd.find_all(class_="resList")
                for item in all_a_tags:
                    sleep(10)
                    link_on_category = f'https://www.russianfood.com{item.get("href")}'
                    count_pages = get_pages_count(link_on_category)

                    print(f'link - {link_on_category} | count_pages - {count_pages}')

                    get_links_on_goods(link_on_category, count_pages)

    else:
        print(f"error accept to url. status {req.status_code}")


def get_pages_count(link):
    link = f'{link}&page=10000'
    req = requests.get(url=link, headers=headers)
    src = req.text

    soup = bs(src, "lxml")
    try:
        pages_counter = soup.find("div", class_="pages").find_all("a")
        return int(pages_counter[len(pages_counter)-1].text)+1
    except:
        return 1

def get_links_on_goods(link, count_pages):

    for i in range(count_pages):
        print(f'    page number {i+1} | link - {link}&page={i+1}')
        
        req = requests.get(url=f'{link}&page={i+1}', headers=headers)
        src = req.text

        soup = bs(src, "lxml")
        recipe_list = soup.find(class_="recipe_list_new").find_all("div", class_="title_o")
        for item in recipe_list:
            sleep(10)

            get_info_about_recipe(f'https://www.russianfood.com{item.find("a").get("href")}')

def get_info_about_recipe(link):
    req = requests.get(url=link, headers=headers)
    src = req.text
    soup = bs(src, "lxml")

    recipe_name = soup.find('h1').text
    try:
        portion_count = soup.find('div', class_='sub_info').find('div', class_='el').text
        if 'порц' not in portion_count: portion_count = 'no info'
    except:
        portion_count = 'no info'

    ingredients = soup.find('table', class_='ingr').find_all('tr')
    print(f'        recipe_name - {recipe_name} | portion_count - {portion_count} | link - {link}')
    ingredients.pop(0)
    # for item in ingredients:
    #     print(item.text)

link = "https://www.russianfood.com/recipes/"
get_all_categories(link)
