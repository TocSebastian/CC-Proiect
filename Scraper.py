import pandas as pd
import requests
from bs4 import BeautifulSoup


url = 'https://www.imdb.com/search/title/?title_type=feature&user_rating=8.0,&num_votes=10000,&languages=en&sort=user_rating,desc&count=100&start=101&ref_=adv_nxt'
page = requests.get(url).text
doc = BeautifulSoup(page, 'html.parser')

number_of_pages = int(doc.find_all(class_="desc")[0].find('span').text.split()[2].replace(',',''))//100


mov ={}
l ='https://www.imdb.com/'
i = 1
for x in range(0,number_of_pages+1):
  url = 'https://www.imdb.com/search/title/?title_type=feature&user_rating=8.0,&num_votes=10000,&languages=en&sort=user_rating,desc&count=100&start='+str(x)+'01&ref_=adv_nxt'
  # url = 'https://www.imdb.com/search/title/?title_type=feature&num_votes=10000,&languages=en&view=simple&sort=user_rating,desc&count=100&start='+str(x)+'01&ref_=adv_nxt'
  page = requests.get(url).text
  doc = BeautifulSoup(page, 'html.parser')
  movies_page = doc.find('div', class_="lister-list").find_all(class_="lister-item mode-advanced")
  for movies in movies_page:
    link = l + movies.a['href']
    nume = movies.a.find('img', alt=True)['alt']
    
    mov[i] = {'Name':nume, 'link':link}
    i+=1
  # print('='*80+'>'+str(x*100))



df = pd.DataFrame(data = mov.values())
new_links = df['link'].to_list()

df_movies = pd.read_csv('/content/drive/MyDrive/CC/CC data/data.csv')
old_links = df_movies['link'].to_list()


links_to_scrape = []
for link in new_links:
  if link not in old_links:
    links_to_scrape.append(link)


scraped_movies = {}
nume = []
year = []
duration = []
nota = []
votes = []
links = []
for link in links_to_scrape:
  page = requests.get(link).text
  movies = BeautifulSoup(page, 'html.parser')
   
  nume.append(movies.find(class_="sc-94726ce4-1 iNShGo").find('h1').text)
  try:
    year.append(movies.find_all('span',class_="sc-8c396aa2-2 itZqyK")[0].text)
  except:
    year= None

  try:
    duration.append(movies.find_all("li",role="presentation",class_="ipc-inline-list__item")[2].text)
  except:
    duration = None
  
  try:
    nota.append(movies.find("span",class_="sc-7ab21ed2-1 jGRxWM").text)
  except:
    nota=None

  try:
    votes.append(movies.find("div",class_="sc-7ab21ed2-3 dPVcnq").text)
  except:
    votes = None
  
  links.append(link)


scraped_movies = {'name':nume, 'year':year, 'duration':duration, 'nota':nota, 'votes':votes, 'link':links}

df_scraped_movies = pd.DataFrame(scraped_movies)
df_movies = pd.concat([df_movies,df_scraped_movies])
df_movies = df_movies.set_index('name').reset_index()
df_movies[['year','nota']] = df_movies[['year','nota']].apply(pd.to_numeric)
df_movies.to_csv('/content/drive/MyDrive/CC/CC data/data.csv', index = False)
