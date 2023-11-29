# N = int(input())

# for i in range(N):
#     spaces = ''
#     T = N-i
#     while T>0:
#       spaces +=' '
#       T-=1
#     for j in range(i+1):
#         if j==0:
#          print(spaces+"*",end=" ")
#         else:
#          print("*",end=" ")
#     print()
  #Alphabets pattern
  #print A 


# height = 3
# width = (2 * height) - 1
# n = width // 2
# for i in range(0, height):
#     for j in range(0, width+1):  
#         #print(i,j,n,width-n,height//2)
#         if (j == n
#             or j == (width - n) 
#             or 
#             (i == (height // 2) 
#              and j > n 
#              and j < (width - n))):
#             print("*", end="")
            
#         else:
           
#             print(end=" ")
#     print()
#     n = n-1
# current date check  code for blocking request 
# from datetime import datetime
# print(datetime.today().date())
# a = [12,12] 
# test = [12,5,4,3,1]

# print(test[1:]+)sa
  

# moodboardlist = list(map(int,input().split())) 
# N = len(moodboardlist)
# #sudo code 
# #xoring list 
# mlist = []
# for i in range(N): 
#     newlist = moodboardlist[i+1:N]
#     # if i == 1: 
#     #     print(mlist)
#     #     break 
#     N1 = len(newlist)
#     k = 0
#     pairlist = []
#     pairlist.append(moodboardlist[i])
#     restart = True
#     while k != N1:
#       for j in range(N1): 
                
#                 if j <= k: 
#                       pairlist.append(newlist[j])                
#                 if j == k: 
#                       mlist.append(pairlist)
#                       pairlist = []  
#                       pairlist.append(moodboardlist[i])  
#                       k+=1  
#                       break             
# print(mlist)    

# def subArraySum(arr, n, s): 
#        #Write your code here
        
#         total = l = 0
#         for r in range(n):
#             # update total
#             total += arr[r]
#             print(r,l,total)
#             # adjust window size
#             while total > s and l < r:
#                 total -= arr[l]
#                 print(total)
#                 l += 1
#             # update res
#             if total == s:
#                 return [l + 1, r + 1]
#         return [-1] 
# print(subArraySum([1,4,4,7,6,5,4,3,8],9,26))
# total is 13 
# i = 0 pe 
# tempsum = 13-1 = 12
# rightsum = 12-0 = 12 
# leftsum = 1
# i = 1 
# tempsum = 10
# rightsum = 9
# leftsum = 4
# i = 2 
# tempsum  = 8
# rightsum = 8-4 = 4


# N = 5
# A = [1,3,5,2,2]
# if N == 1:
#   print(1)
# total = sum(A) 
# print(total)
# leftsum = 0
# rightsum = 0     
# for i in range(N): 
#   tempsum=total-A[i]
#   rightsum = tempsum-leftsum
#   if rightsum == leftsum:
#       print(i+1) 
#   else: 
#       leftsum += A[i]
#   print(-1)   

#     A = list(map(int,input().split()))
#     A.pop(0)
#     A.reverse()
#     reversestr = '' 
#     for i in A:  
#         reversestr += str(i)+' '
#     print(reversestr)  

# def main(): 
#     b = input()
#     b_split = b.split(" ")
#     res  = [eval(j) for j in b_split ]
#     rev1 = res[::-1]
#     a = " ".join([str(i) for i in rev1])
#     print(a+" ")
# if __name__ == "__main__": 
#     main()

# s = '123456'
# getlen = (len(s)//2)
# prefix = s[:getlen]
# suffix = s[getlen:]
# if int(prefix[::-1])>int(suffix):
#     nearestpal = prefix+prefix[::-1]
# else: 
#     prefix = str(int(prefix)+1)
#     nearestpal = prefix+prefix[::-1]
#     print(nearestpal)



# mlist = list(s[:getlen])
# mlist[len(mlist)-1] = str(int(mlist[len(mlist)-1])+1)
# rev  = mlist[::-1]
# rev.pop(0)
# nearestpal  = ' '.join(mlist+rev)
# print(nearestpal)


# import tabula
# Read a PDF File
# df = tabula.read_pdf("test.pdf", pages='all') 
# print(df)
# convert PDF into CSV 
# tabula.convert_into("test.pdf", "iplmatch.csv", output_format="csv", pages='all')
# print(df)


# import PyPDF2
  
# # creating a pdf file object
# pdfFileObj = open('test.pdf', 'rb')
  
# # creating a pdf reader object
# pdfReader = PyPDF2.PdfReader(pdfFileObj)
  
# # printing number of pages in pdf file
# #print(pdfReader.pages)
  
# # creating a page object
# pageObj = pdfReader.pages[0]
  
# # extracting text from page
# print(pageObj.extract_text())
  
# # closing the pdf file object
# pdfFileObj.close()



# import camelot
# tables = camelot.read_pdf('file:///home/vinayak/Moodboard/new%20pdfs/DPP7%20route%20sheets%2008.13.2023.pdf')
# print(tables)
# tables
# <TableList n=1>
# tables.export('foo.csv', f='csv', compress=True) # json, excel, html, markdown, sqlite
# tables[0]
# <Table shape=(7, 7)>
# tables[0].parsing_report
from flask import Flask, render_template, request, redirect, url_for
import os
import pdfplumber

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            
            pdf_text = parse_pdf_text(filename)
            
            return "Done" 
            
    
    return render_template('upload.html')

def parse_pdf_text(pdf_path):
    # pdf_text = ""
   
    with pdfplumber.open(pdf_path) as pdf:
        #print("Pages:",pdf.pages)
        length = 0 
        for page in pdf.pages:
          try:
          #print("Directory :",dir(page))
            pdf_text = page.extract_text()
            print("Data :",pdf_text)
            if length == 2: 
                return pdf_text
          
          except Exception as e:
            print("Error extracting text:", e)
          length+=1
      
            
    return pdf_text

if __name__ == '__main__':
    app.run(debug=True)
    