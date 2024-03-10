#
import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import unicodedata2
from tqdm import tqdm
from pprint import pprint

def gen_headers():
    headers = Headers(browser='chrome', os='win')
    return headers.generate()

url = 'https://spb.hh.ru/search/vacancy?L_save_area=true&text=python&search_field=name&search_field=company_name&search_field=description&excluded_text=&area=2&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=100&hhtmFrom=vacancy_search_filter'
response = requests.get(url, headers=gen_headers())

if 200 <= response.status_code <= 300:
    print(f'ok', {response.status_code})
else:
    print(f'error', {response.status_code})

main_html = response.text
main_soup = BeautifulSoup(main_html, "lxml")
vacancy_list_tag = main_soup.find('div', id="a11y-main-content")
vacancy_tags = vacancy_list_tag.find_all('div', class_="vacancy-serp-item__layout")
print(f'{len(vacancy_tags)} !!!!!!!!!')
all_vc = []
for vacancy_tag in tqdm(vacancy_tags):
    link_a = vacancy_tag.find('a')
    link_vс = link_a['href']
    response_vacancy = requests.get(link_vс, headers=gen_headers())
    vacancy_soup = BeautifulSoup(response_vacancy.text, "lxml")
    vacancy_1block = vacancy_soup.find('div', class_="bloko-column bloko-column_container bloko-column_xs-4 bloko-column_s-8 bloko-column_m-12 bloko-column_l-10")
    vacancy_content = vacancy_1block.find('div',class_="g-user-content")
    if ('Flask' in vacancy_content.text) or ('Django' in vacancy_content.text):
        vacancy_2block = vacancy_soup.find('div', class_="vacancy-company-redesigned")
        vc_city = vacancy_2block.find('p')
        if vc_city != None:
            vc_city = vc_city.text
            # print(vc_city.text)
        elif vc_city == None:
            vc_city = vacancy_2block.find('a', class_="bloko-link bloko-link_kind-tertiary bloko-link_disable-visited")
            vc_city = vc_city.text.split(',')
            vc_city = vc_city[0]

        vc_cash = vacancy_tag.find('span', class_="bloko-header-section-2")
        if vc_cash != None:
            vc_cash = unicodedata2.normalize("NFKC", vc_cash.text)
        else:
            vc_cash = 'None'

        name_company = vacancy_tag.find('div', class_="bloko-text")
        name_company = unicodedata2.normalize("NFKC", name_company.text)
        article_dict = {
            "link_vс": link_vс,
            "vc_cash": vc_cash,
            "name_company": name_company,
            'vc_city': vc_city
        }
        all_vc.append(article_dict)

# pprint(all_vc)
json_string = json.dumps(all_vc, ensure_ascii=False)
pprint(json_string)