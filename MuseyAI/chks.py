      
arr = [135, 101, 170, 125, 79, 159, 163, 65, 106, 146, 82, 28, 162, 92, 196, 143, 28, 37, 192, 5, 103, 154, 93, 183, 22,117, 119, 96, 48, 127, 172, 139, 70, 113, 68, 100, 36, 95, 104, 12, 123, 134]
n = 42 
s = 468 
pairlist = []
def main(): 
    for i in range(1,n+1): 
        pairlist = []
        startindext = i
        counter = i 
        for j in range(i,n+1): 
            
            pairlist.append(arr[j-1])
            if sum(pairlist) == s: 
              return str(i)+str(counter)  
            if sum(pairlist)>s:
                break
            counter+=1
print(main())    