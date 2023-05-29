import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd

REVIEW_URL_START = 'https://www.imdb.com'
REVIEW_URL_END = 'reviews'
RATING_URL = 'ratingFilter='
RATING = ['6','7','8','9','10']
SORT_URL = 'sort='
SORT_METHOD = ['totalVotes', 'reviewVolume']

class MovieReviewDataset:
    def __init__(self):
        self.dataset = np.array(["movie_index", "link", "rating", "date", "review"],str).reshape(1,5)
        self.movie_index=None

    def _parse_review_data(self, movie_url:str, sort_method:str="curated", rating_filter:str='0'):
        try:
            input_url = REVIEW_URL_START+movie_url+REVIEW_URL_END+'?'+SORT_URL+sort_method+'&'+RATING_URL+rating_filter
            response = requests.get(input_url)
            soup = BeautifulSoup(response.text, "html.parser")
            print(input_url)

            reviews = soup.select('div.review-container')
            for review in reviews:
                # 리뷰 link
                review_link = review.select_one('a.title')
                review_link = review_link.attrs.get('href')
                # print(review_link)

                # 날짜
                review_date = review.select_one('.review-date')
                if review_date == None:
                    review_date = ""
                else:
                    review_date = review_date.get_text()
                # print(review_date)

                # 리뷰
                review_content = review.select_one('div.text.show-more__control')
                review_content = review_content.get_text()
                # print(review_content)

                result = np.array([self.movie_index, review_link, rating_filter, review_date, review_content],dtype=str).reshape(1,5)
                self.dataset = np.append(self.dataset, result, axis=0)
            print(self.dataset.shape)

        except Exception as e:
            print(e)
            print("Fail to parse web :"+input_url)
            # raise Exception("Fail to parse web :"+input_url)

    def parseMovieData(self, movie_index:str, movie_url:str):
        self.movie_index = movie_index
        
        for sort in SORT_METHOD:
            for rating in RATING:
                self._parse_review_data(movie_url, sort, rating)

    def saveMovieData(self):
        df = pd.DataFrame(self.dataset)
        file_name = 'movie_'+self.movie_index+'.xlsx'
        df.to_excel(file_name, index=False)
        # np.savetxt(file_name,self.dataset, delimiter=',',fmt='%s')

    @staticmethod
    def mergeMovieData(target, file_list):
        merged_data = pd.read_excel(target)
        print(merged_data.shape)

        for file in file_list:
            data = pd.read_excel(file)
            print(data.shape)
            merged_data = pd.concat([merged_data,data])

        merged_data.to_excel("merged_file.xlsx", index=False)

if __name__ == "__main__":
    # movies = pd.read_excel('Data/Top250_Movies.xlsx')
    # movies = movies[1:251]
    # print(movies)
    
    # for i, row in movies.iterrows():
    #     movie_index = row[0]
    #     movie_name = row[1]
    #     movie_url = row[2]
    #     print("*************** Movie:{0} **********************".format(movie_name))
    #     dataset = MovieReviewDataset()
    #     dataset.parseMovieData(movie_index,movie_url)
    #     dataset.saveMovieData()
    
    # 파일 합치기
    import time
    for i in range(190,250):
        print(i)
        time.sleep(1)
        MovieReviewDataset.mergeMovieData("merged_file.xlsx", [f'movie_{i}.xlsx'])
    