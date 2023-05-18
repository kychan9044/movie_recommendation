import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd

REVIEW_URL_START = 'https://www.imdb.com/review/rw'
REVIEW_URL_END = '/?ref_=tt_urv'
MIN_RATING = 6

class MovieReviewDataset:
    def __init__(self):
        self.dataset = np.array(["index","name","link","rating","review"],str).reshape(1,5)
        # self.dataset = np.array([])
    
    def _parse_review_data(self, index:int):
        try:
            index_num = str(index).zfill(7)
            response = requests.get(REVIEW_URL_START+index_num+REVIEW_URL_END)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 평점
            rating = soup.select_one('span.rating-other-user-rating span')
            rating = rating.get_text()
            # print(rating.get_text())

            # 평점 7점 이상만 수집
            if int(rating) < MIN_RATING:
                print("rating is too low : ", rating)
                return

            # 영화 제목, 링크
            movie = soup.select_one('div.lister-item-header a')
            link = movie.attrs.get('href')
            movie_name = movie.get_text()
            # print(movie_name, link)

            # 리뷰
            review = soup.select_one('div.text.show-more__control')
            review = review.get_text()
            # print(review.get_text())
            result = np.array([index_num, movie_name, link, rating, review],dtype=str).reshape(1,5)
            self.dataset = np.append(self.dataset, result, axis=0)

        except Exception as e:
            print(e)
            print("Fail to parse web :"+REVIEW_URL_START+index_num+REVIEW_URL_END)
            # raise Exception("Fail to parse web :"+REVIEW_URL_START+index_num+REVIEW_URL_END) 
    
    def saveMovieData(self, start_num:int, end_num:int):
        for i in range(start_num, end_num+1):
            self._parse_review_data(i)

        df = pd.DataFrame(self.dataset)
        file_name = 'moview_'+str(start_num)+'_'+str(end_num)+'.xlsx'
        df.to_excel(file_name, index=False)
        # np.savetxt(file_name,self.dataset, delimiter=',',fmt='%s')

if __name__ == "__main__":
    dataset = MovieReviewDataset()
    dataset.saveMovieData(6506000,6507000)