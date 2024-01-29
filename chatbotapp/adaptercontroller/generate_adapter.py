import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrapconfig import WEBSITES
print(WEBSITES)
url = ''
file_content_first = f"""\
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""

file_content_second = f"""\
from adaptercontroller.adapter_template import AdapterTemplate
adapter = AdapterTemplate(site)
adapter.read_all_site_based_urls()
adapter.scrap_webiste()
"""

class GenerateAdapter: 

    def generate_adapter(self):
        try: 
            for website in WEBSITES: 
                url = website['url']
                site = website['site']
                if self.is_adapter_exists(website['site']) == False:  
                    file_name = os.path.dirname(os.path.dirname(__file__))+'/adapter/'+website['site'].lower()+".py"
                    with open(file_name, "w") as file:
                        #file_content.append("url")
                        content = file_content_first+f"url = '{url}'\nsite = '{site}' \n"+file_content_second
                        print(content)
                        file.write(content) 
                    print("Adapter Created")
        except Exception as e: 
                print(f"Error: {e}")
            
        

    def is_adapter_exists(self,site): 
        site  = str(site).lower()
        dirlist =  os.listdir(os.path.dirname(os.path.dirname(__file__))+'/adapter')

        for file in dirlist:    
            filename  = file[0:len(file)-3]
            if filename == site: 
                return True
               
        return False
gencheck = GenerateAdapter()
gencheck.generate_adapter()