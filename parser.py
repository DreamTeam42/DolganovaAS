import requests
from bs4 import BeautifulSoup





def get_html(url):
	r = requests.get(url)
	return r.text

	def get_total_pages(html)
	soup = BeautifulSoup(html, 'lxml')

	pages = soup.find('div', class_ ='only_desktops').find('a', class_='only_desktops')[-1].get('href')
	total_pages = pages.split('=')[1].split('&')[0]

	return int(total_pages)


def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')

	ads = soup.find('div', class_='ob2_bl__content').finf_all('div', class_'content')
	for ad  in ads:
		# main_title, descr, price price3, text_bottom, ?top_right?
		try: 
			main_title = ad.find



def main():
	url = 'https://volg.kvadroom.ru/kupit-kvartiru/?page=4'
	base_url = 'https://volg.kvadroom.ru'
	page_part = '?page='

	total_pages = get_total_pages(get_html(url))

	for i in range(1, total_pages):
		url_gen = base_url + page_part + str(i)
		print(url_gen)
		html = get_html(url_gen)
		get_page_data(html)



if __name__== '__main__'
    main()
