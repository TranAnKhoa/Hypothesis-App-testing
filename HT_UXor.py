from HTmodule import *
import numpy as np
path="HTdata 4 (3popu).csv"
arr_int1,arr_int2,arr_int3,arr_int4=readfile(path)

alpha=float(input("Enter the level of significance: "))

mode=int(input("You want to test 1 tail or 2 tails (1/2): "))
if len(arr_int1)!=0:
    std1=input("Enter the std1 (if not enter None):" )
    std=std1.lower()
    n1=np.size(arr_int1)
    print("n1=: ",n1)
    smean1=np.mean(arr_int1)
    print("Mean1: ",smean1)
else:
    n1=0;std1=0
    
if len(arr_int2)!=0:
    std2=input("Enter the std2 (if not enter None):" )
    std2=std2.lower()
    n2=np.size(arr_int2)
    print("n2=: ",n2)
    smean2=np.mean(arr_int2)
    print("Mean2: ",smean2)        
else:
    n2=0;std2=0
    
if len(arr_int1)!=0 and len(arr_int2)!=0:
    choose=input("The sample are independent or pair: ")
    choose=choose.lower()
    if choose=="pair":
        muyd=smean1-smean2
        D=float(input("Enter the difference: "))
        arr_int=arr_int1-arr_int2
        print("Array diffenrence: ",arr_int,"\n")
        std=np.std(arr_int,ddof=1) #1
        print(std)
        n=n1
    else:
        eVar=input("Does equal variance assumption is given or not (yes/no): ")
else:   
    muy=float(input("Enter the value u want to test(Ho): "))
    arr_int1=arr_int2;arr_int2=[]
    std1=std2;std2=0
    n1=n2;n2=0
    smean1=smean2;smean2=0
    choose=[]
#Calculate
if n1>=30 or std1!="none":
    if (n2>=30 or std2!=0) and choose=="independent":
        if std1=="none":
            std1=np.std(arr_int1,ddof=1) #2
            std2=np.std(arr_int1,ddof=1) #3
        else:
            std1=float(std1);std=float(std2)
        y=Twopopu(smean1,smean2,0,alpha,std1,std2,n1,n2,mode)
        print(y.indeZ())
    elif (n2>=30 or std2!=0) and choose=="pair":
        std1=float(std1);std2=float(std2)
        y=depend(muyd,D,std,n,mode,alpha)
        print(y.zdepend())
    elif n1>=0 and n2==0:
        if std1=="none":
            std1=np.std(arr_int1,ddof=1) #6 #ddof=1 là sample std, ddof=0 là population std
            y=Onepopu(muy,alpha,std1,n1,smean1,mode)
            print(y.onep_zdis())
        else:
            print("step3")
            std1=float(std1)
            y=Onepopu(muy,alpha,std1,n1,smean1,mode)
            print(y.onep_zdis())
elif n1<30 and std1=="none":
    std1=np.std(arr_int1,ddof=1) #4
    std2=np.std(arr_int1,ddof=1) #5
    if choose=="independent":
        y=Twopopu(smean1,smean2,0,alpha,std1,std2,n1,n2,mode)
        print(y.indeT(eVar))
    else: #choose==pair
        y=depend(muyd,D,std,n,mode,alpha)
        print(y.tdepend())

else: #if n1<30 and n2==0
    std1=np.std(arr_int1,ddof=1)
    print("Sample std: ",std1)
    y=Onepopu(muy,alpha,std1,n1,smean1,mode)
    print(y.onep_tdis())

