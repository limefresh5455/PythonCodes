import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib
import PyPDF2
from io import BytesIO
from openai import OpenAI
import math
import concurrent.futures
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapconfig import WEBSITES
class AdapterTemplate: 
    def __init__(self,site):
        self.site = site
        self.sites = [] 
        self.filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+'/TaxGPTList.xlsx'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self.max_tokens = 500
    def read_all_site_based_urls(self): 
        df = pd.read_excel(self.filepath)
        result_list = df.to_dict(orient='records')
        for url in result_list: 
            if self.site.lower() in url['Owner'].lower(): 
               self.sites.append(url)       
        return self.sites


    def scrap_webiste(self): 
        try: 
            filename = self.sites[0]["Owner"]+'.txt'
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+'/datascrap/'+filename
            print(file_path)
            if os.path.exists(file_path):
                # Remove the file
                os.remove(file_path)
            for url in self.sites: 
                response = requests.get(url['Website link'],headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text()
                for element in soup(['header', 'footer', 'nav']):
                    element.decompose()
                text = soup.get_text(strip=True)
                cleaned_text = self.clean_html(text)
                file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+'/datascrap/'+url['Owner']+'.txt'
                with open(file_name, 'a', encoding='utf-8') as file:
                    file.write(cleaned_text)
            return True      
        except Exception as e: 
            print("Error: ",e)
            return False

    def clean_html(self,text):
        text_lines = [line for line in text.splitlines() if line.strip()]
        cleaned_text = '\n'.join(text_lines)
        formated_text = self.openai_generate_qa_pairs_from_text(cleaned_text)
        print(formated_text)
        return formated_text
    
    def openai_generate_qa_pairs_from_text(self,text): 
        num_chunks = math.ceil(len(text) / self.max_tokens)
        text_chunks = [text[i * self.max_tokens:(i + 1) * self.max_tokens] for i in range(num_chunks)]
        
        output_format_openai = ''
        with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the process_chunk function to each chunk in parallel
            results = list(executor.map(self.process_chunk, text_chunks))

        # Concatenate the results
        output_format_openai = "\n".join(results)
        print(output_format_openai)
        return output_format_openai
    
    def process_chunk(self,chunk):
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Please provide answers in a consistent format of Q:[Question] A:[Answer]"
                    },
                    {
                        "role": "user",
                        "content": "Create question and answer pairs from this text:" + chunk
                    }
                ],
            )
            return response.choices[0].message.content.strip()