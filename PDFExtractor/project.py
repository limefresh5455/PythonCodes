import os
from flask import Flask, render_template, request
# from flask_uploads import UploadSet, configure_uploads, ALL
import pdfplumber
import pdb 
import copy
import pandas as pd
app = Flask(__name__)
app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
# uploads = UploadSet(extensions=ALL)
# configure_uploads(app, uploads)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        pdf_file = request.files['file']
        uploaded_file = request.files['file']
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = uploaded_file.filename
            print("File",filename)
            pdf_path = os.path.join('uploads', filename)
            error = '' 
            success = '' 
            uploaded_file.save(pdf_path)
            
            extracted_text = extract_text_from_pdf(pdf_path)  
            df = pd.DataFrame(extracted_text)
            newfile = filename[0:len(filename)-5]
            print("File",newfile)
            csv_path = os.path.join('csvs', newfile+'.csv')
            excelpath = os.path.join('xlsfiles', newfile+'.xlsx')
            
            df.to_excel(excelpath, index=False)
            df.to_csv(csv_path, index=False)
            print("Save the file ",excelpath)
            print("Save the file ",csv_path)
            success = "Csv Saved to the folder, please check xlsfiles and csvs folders to check csv and excel file"
        
            error = "Something went wrong"
            os.remove(pdf_path)
            return render_template('index.html', success=success,error=error)
    return render_template('index.html', extracted_text=None)

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        #pdb.set_trace()
        oveflowcsv = []
        bagcsv = []
        totallength =  len(pdf.pages)
        finalcsvbags = []
        for i in range(totallength):
            page = pdf.pages[i]  # Adjust as needed
            if page.extract_text()!='':
                totaldata = extract_table(page)
                mainobject = totaldata.copy()
                del mainobject["packagedata"]
                for bag in totaldata['packagedata']:  
                    bagobj = mainobject.copy()
                    bagobj['bag_line_no'] = bag['bag_line_no']
                    bagobj['bag_sort_zn'] = bag['bag_sort_zn']
                    bagobj['bag_id'] = bag['bag_id']
                    bagobj['bag_pkgs'] = bag['bag_pkgs']
                    bagobj['overflow_line_no'] = bag['overflow_line_no']
                    bagobj['overflow_sort_zn'] = bag['overflow_sort_zn']
                    bagobj['overflow_pkgs'] = bag['overflow_pkgs']
                    finalcsvbags.append(bagobj)    
               
        return finalcsvbags

def extract_table(page):
    pdfData = {
        "stage_cd":'',
        "route_cd":'',
        "dsp_cd":'', 
        "van_type":'', 
        "station_cd":'',	
        "route_dt":'',
        "cycle_cd":'',
        "loadout_tm":'', 
        "bags_tot":'', 
        "overflow_tot":'', 
        "packages_tot":'', 
        "commercial_packages_tot":'',
        "packagedata":[],
        }
    bagspackages = {
        "bag_line_no":'',
        "bag_sort_zn":'',
        "bag_id":'',
        "bag_pkgs":'',
        "overflow_line_no":'',	
        "overflow_sort_zn":'', 
        "overflow_pkgs":'',    
    }
   
    text = page.extract_text()
    table = [line.split(' ') for line in text.split('\n') if line.strip() != '']
    counter = 0 

    # for lineindex in range(0,4):
    #     tablejoin = ' '.join(table[lineindex])
    #     if  'bags' in tablejoin:
    #         break
    #     counter+=1
    istitle = False
    for lineindex in range(0,3): 
        tablejoin = ' '.join(table[lineindex])
        if table[lineindex][0].count('.')==2 or table[lineindex][0].count('·')==2:
                pdfData['stage_cd'] = table[lineindex][0]
                print("Title: ",tablejoin)
                istitle = True
        
        if table[lineindex][0].count('.')!=2 or table[lineindex][0].count('·')!=2:
                if  'bags' in tablejoin:
                    break
                if  'CYCLE' in tablejoin:
                    pdfData['station_cd'] = table[lineindex][0]
                    pdfData['route_dt'] = ' '.join(table[lineindex][2:6])
                    pdfData['cycle_cd'] = ' '.join(table[lineindex][7])
                    if  ':' in tablejoin:
                        pdfData['loadout_tm']  = ' '.join(table[lineindex][len(table[lineindex])-2:])
        
                if '·' in  tablejoin and 'CYCLE' not in tablejoin:
                 
                    if '·' in table[lineindex][0]:
                       
                        pdfData['dsp_cd'] = table[lineindex][0]
                        pdfData['van_type'] = ' '.join(table[lineindex][2:])
                    else: 
                       
                        pdfData['route_cd'] = table[lineindex][0]
                        pdfData['dsp_cd'] = table[lineindex][1]
                        pdfData['van_type'] = ' '.join(table[lineindex][3:])
                if "·" not in tablejoin: 
                    
                     pdfData['route_cd'] =  table[lineindex][0]
                      
        if  'bags' in tablejoin:
            pdfData['bags_tot']  = table[lineindex][0]
            pdfData['overflow_tot']  = table[lineindex][2]
    bagfound = False
    for lineindex in range(1,len(table)): 
        tablejoin = ' '.join(table[lineindex])
        if  'bags' in tablejoin and 'over' in tablejoin:
            bagfound = True
            pdfData['bags_tot']  = table[lineindex][0]
            pdfData['overflow_tot']  = table[lineindex][2]  
        if "Total" in tablejoin:
            pdfData['packages_tot'] = table[lineindex][2]
        if "Commercial" in tablejoin:
            pdfData['commercial_packages_tot'] = table[lineindex][2]
            
        if bagfound == True: 
            if len(table[lineindex])==8:
                copydata = bagspackages.copy()
                overflowdata = {}
                copydata["bag_line_no"] = table[lineindex][0]
                copydata["bag_sort_zn"] = table[lineindex][1]
                copydata["bag_id"] = ''.join(table[lineindex][2:4])
                copydata["bag_pkgs"] = table[lineindex][4]
                copydata["overflow_line_no"] = table[lineindex][5]
                copydata["overflow_sort_zn"] = table[lineindex][6]
                copydata["overflow_pkgs"] = table[lineindex][7]
                pdfData['packagedata'].append(copydata)
                
            if len(table[lineindex])==5:
                copydata = bagspackages.copy()
                copydata["bag_line_no"] = table[lineindex][0]
                copydata["bag_sort_zn"] = table[lineindex][1]
                copydata["bag_id"] = ''.join(table[lineindex][2:4])
                copydata["bag_pkgs"] = table[lineindex][4]
                copydata["overflow_line_no"] = ''
                copydata["overflow_sort_zn"] = ''
                copydata["overflow_pkgs"] = ''
                pdfData['packagedata'].append(copydata)
   
    return pdfData
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
    #leasypridictor