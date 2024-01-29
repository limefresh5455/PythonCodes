import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
url = 'tax.hawaii.gov'
site = 'Hawaii' 
from adaptercontroller.adapter_template import AdapterTemplate
adapter = AdapterTemplate(site)
adapter.read_all_site_based_urls()
adapter.scrap_webiste()
