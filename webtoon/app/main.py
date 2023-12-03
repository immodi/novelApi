import sys
import requests
from .helper import *
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
import os
from shutil import rmtree
from pathlib import Path

CURRENT_DIR = os.path.join(os.getcwd(), "webtoon", "app")

class WebtoonScrapper():
    def __init__(self, series_name: str, link: str, starting_chapter: int, total_chapters: int, target_website: str):
        self.link = link
        self.starting_chapter = starting_chapter
        self.total_chapters = total_chapters
        self.series_name = series_name
        self.target_website = target_website
        self.webtoon_path = Path(CURRENT_DIR, self.series_name)

    def execute(self):
        selectors = {
            # webtoon_source: (parent_element, next_chapter)
            "hiperdex": ('page-break', 'next_page'),
            "manga18fx": ('page-break', 'navi-change-chapter-btn-next'),
            "toonily": ('page-break', 'next_page'),
        } 

        make_dir(self.webtoon_path)

        for current_chapter in range(self.total_chapters):
            try:
                request = requests.get(self.link)          
                response = HtmlResponse(url=self.link, body=request.text, encoding="utf-8")
            
                images_url = Selector(response=response).response.css(f'.{selectors[self.target_website][0]} img::attr(src)').extract()
                self.save_all_images(images_url, self.starting_chapter)
                
                if self.target_website == "manga18fx":
                    self.link = "https://manga18fx.com/" + self.link
                    self.link = "-".join(self.link.split("-")[0:-1]) + f"-{self.starting_chapter+1}"
                    
                try: 
                    self.link = Selector(response=response).css(f".{selectors[self.target_website][1]}::attr(href)").extract()[0]
                except IndexError:
                    break
                    
                print(f"next_url => {self.link}")
                self.starting_chapter += 1
                
            except Exception as e:
                print(e)
                continue

        zip_dir(self.webtoon_path)

    def save_all_images(self, images_url_arr: list, chapter_num: int):
        # current_dir = f"{self.series_name}\\{chapter_num}"
        current_dir = os.path.join(self.webtoon_path, str(chapter_num))
        make_dir(current_dir)
        
        for i in range(images_url_arr.__len__()):
            get_image(str(i+1), images_url_arr[i], current_dir)


    def clean_up(self):
        rmtree(self.webtoon_path)
            


# webtoon = WebtoonScrapper(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
# webtoon.execute()

