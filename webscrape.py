import time
import requests
from bs4 import BeautifulSoup
from csv import writer
import re

start=time.time()
base_url="https://www.imdb.com/search/title?groups=top_250&sort=user_rating"
with open('movies.csv','w') as csv_file:
    csv_writer=writer(csv_file)
    headers=['Movie_name','Release_year','Certificate','Runtime','Genre','Rating','Description','Directors','Stars']
    csv_writer.writerow(headers)
    for page in range(1,250,50):
        url=base_url+',desc&start='+str(page)+'&ref_=adv_nxt'
        response = requests.get(url)
        soup=BeautifulSoup(response.text,'html.parser')

        lists=soup.find_all(class_='lister-item-content')


        for movie in lists:
            #ttitle = list(movie.find(class_='lister-item-year').stripped_strings)
            #print(ttitle)
            #title=list(movie.h3.stripped_strings)
            movie_name=movie.a.string
            #release_year=title[2].replace('(','').replace(')','')
            release_year=movie.find(class_="lister-item-year").string.replace('(','').replace(')','')


            try:
                certificate=movie.p.find(class_='certificate').string
            except:
                certificate=None
            #certificate = movie.p.find(class_='certificate').string
            runtime=movie.find(class_='runtime').string
            genre=movie.find(class_='genre').string.strip('\n ')


            rating=movie.find(class_="imdb-rating").find_next_sibling("strong").string

            #rating=movie.div.find(attrs={"name":"ir"}).string
            description=movie.p.find_next_sibling('p').get_text().strip('\n ')



            directors_link=movie.p.find_next_sibling('p').find_next_sibling('p').find('span').find_previous_siblings('a')
            director_list=[]
            for dir in directors_link:
                director_list.append(dir.string)

            directors=','.join(director_list)


            stars_link = movie.p.find_next_sibling('p').find_next_sibling('p').find('span').find_next_siblings('a')
            stars_list=[]
            for star in stars_link:
                stars_list.append(star.string)

            stars=','.join(stars_list)
            info_imdb=[movie_name,release_year,certificate,runtime,genre,rating,description,directors,stars]
            #print(info_imdb)
            csv_writer.writerow(info_imdb)

end=time.time()
print(end-start)






