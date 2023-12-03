import os
import re
import glob
from enum import Enum
import requests
from fpdf import FPDF
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
import shutil
import os

CURRENT_DIR = os.path.join(os.getcwd(), "novels", "app")
class Website(Enum):
    Bednovel = 0,
    AllnovelUpdates = 1,
    Bakapervert = 2


class NovelChaptersLoader():
    def __init__(self, series_name: str, link: str, starting_chapter: int, target_website: int):
        self.link = link
        self.starting_chapter = starting_chapter
        # self.total_chapters = total_chapters
        self.series_name = series_name
        self.target_website = target_website
        self.seperator = "\n========================================================\n"
        
    def execute(self):
        selectors = (
            # novel_source: (chapter_name, chapters_container, next_chapter)
            ('//*[@id="main1"]/div/div/div[1]/span', '//*[@id="article"]', '//*[@id="main1"]/div/div/div[3]/ul/li[4]/a'), # bednovel
            ('//*[@id="main1"]/div/div/div[1]/span', '//*[@id="main1"]/div/div/div[2]', '//*[@id="next"]'), # allnovelupdates
        )     

        while True:
            try:
                try: os.mkdir(os.path.join(CURRENT_DIR, self.series_name))
                except OSError: pass
                request = requests.get(self.link)          
                response = HtmlResponse(url=self.link, body=request.text, encoding="utf-8")
            
                chapter_name = Selector(response=response).xpath(selectors[self.target_website][0]).css("::text").extract()[0]
                chapter_content = Selector(response=response).xpath(selectors[self.target_website][1]).css("p::text").extract()
                self.link = Selector(response=response).xpath(selectors[self.target_website][2]).css("a::attr(href)").extract()[0]

                chapter_paras = [chapter_name, "\n"]
            
                for i in chapter_content:
                    chapter_paras.append(i)
                    chapter_paras.append("\n")
            
                chapter_paras.append(self.seperator)
        
                self.downloader(chapter_paras, self.series_name, self.starting_chapter)

                if self.target_website == "bednovel":
                    self.link = "https://bednovel.com" + self.link
            
                print(self.link)
                self.starting_chapter += 1  
            except Exception:
                break
           
           
        return self.combine()


    def downloader(self, chapter_paras: list, series_name: str, starting_chapter: int):
        novel_folder = os.path.join(CURRENT_DIR, series_name)
        if not os.path.exists(novel_folder):
            os.makedirs(novel_folder)
        with open(os.path.join(f"{novel_folder}", f"{starting_chapter}.txt"), "w", encoding="utf-8") as f:
            f.writelines(chapter_paras)
        return
 
    def combine(self):
        filenames = glob.glob(os.path.join(CURRENT_DIR, self.series_name, "*.txt"))
        filenames = sorted(filenames, key=lambda s: int(re.search(r'\d+', s).group()))
        with open(os.path.join(CURRENT_DIR, f"{self.series_name}.txt"), 'wb') as outfile:
            for f in filenames:
                with open(f, 'rb') as infile:
                    outfile.write(infile.read())
        return self.convert()
    

    def convert(self):       
        pdf = FPDF()
        pdf.set_page_background((0, 0, 0))
        pdf.set_text_color(255, 255, 255)    
        pdf.add_page()
        pdf.add_font("OpenSans", "", os.path.join(CURRENT_DIR, 'OpenSans.ttf'))
        pdf.set_font("OpenSans", '', size=22)

        with open(os.path.join(CURRENT_DIR, f"{self.series_name}.txt"), 'r', encoding="utf-8") as f:
            for x in f.readlines():
                if x in self.seperator or x == self.seperator:
                    pdf._perform_page_break()
                    continue
                pdf.multi_cell(w=0, h=16 ,txt=x, align='L', fill=True)
        pdf.output(os.path.join(CURRENT_DIR, f"{self.series_name}.pdf"))
        shutil.rmtree(os.path.join(CURRENT_DIR, self.series_name))
        os.remove(os.path.join(CURRENT_DIR, f"{self.series_name}.txt"))
        return




# novel = NovelChaptersLoader("Arifureta After Story", "https://bakapervert.wordpress.com/arifureta-chapter-437/", 437, Website.Bakapervert.value)
# novel.execute()