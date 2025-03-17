import numpy as np
from scipy.stats import norm
from scipy.stats import t
from math import floor
# 1 population - 1 tail


import numpy as np
from scipy.stats import norm
from scipy.stats import t
from math import floor
# 1 population - 1 tail


def readfile(filepath):
    file=open(filepath,mode='r', encoding="utf-8-sig")
    row=file.readline()
    dta1=[];dta2=[];dta3=[];dta4=[];dta=[];

    while row!="":
        row=row.strip()
        row=row.split(",")
        try:
            dta1.append(float(row[0]))
        except:
            pass
        if len(row)==2:
            try:
                dta2.append(float(row[1])) 
            except:
                pass
        elif len(row)==3:
            try:
                dta2.append(float(row[1])) 
                dta3.append(float(row[2])) 
            except:
                pass
        elif len(row)==4:
            try:
                dta2.append(float(row[1])) 
                dta3.append(float(row[2])) 
                dta4.append(float(row[3])) 
            except:
                pass
        row=file.readline()
    if len(dta4)!= 0:
        dta=[dta1,dta2,dta3,dta4]
    elif len(dta3)!= 0:
        dta=[dta1,dta2,dta3]
    elif len(dta2)!=0:
        dta=[dta1,dta2]
    print("dta: ",dta)
    for i in dta:
        arr_i=np.array(i)
        arr_inti=arr_i.astype(float)
    arr1=np.array(dta1)
    arr_int1=arr1.astype(float) # convert chuỗi từ string qua float, nếu k thể convert thì xóa bỏ
    if len(dta)==2:
        arr_int2=dta[1]
    else:
        arr_int2=[]
    if len(dta)==3:
        arr_int2=dta[1]
        arr_int3=dta[2]
    else:
        arr_int3=[]
    if len(dta)==4:
        arr_int2=dta[1]
        arr_int3=dta[2]
        arr_int4=dta[3]
    else:
        arr_int4=[]
    print("Arr1: ",arr_int1)
    print("Arr2: ",arr_int2)
    print("Arr3: ",arr_int3)
    print("Arr4: ",arr_int4)
    return arr_int1, arr_int2, arr_int3,arr_int4

class Onepopu:
    def __init__(self,muy,alpha,std1,n1,smean1,mode):
        self.muy=muy
        self.alpha=alpha
        self.std1=std1
        self.n1=n1
        self.smean1=smean1
        self.mode=mode
    def onep_zdis(self):
        zt=(self.smean1-self.muy)/(self.std1/np.sqrt(self.n1))
        print(self.smean1)
        print(self.muy)
        print(self.std1)
        print(self.n1)
        print("Zt: ",zt)
        if self.mode==1:
            zalpha=norm.ppf(self.alpha)
        else:
            zalpha=norm.ppf(self.alpha/2)
        print('Zaplha: ',zalpha)
        if zt<zalpha or zt>-zalpha:
            result = "Reject Ho"
        else:
            result = "Do not reject Ho" 
        #return result
       #ztt=str(zt);zalphaa=str(zalpha)
        a=["Using Z-test",result, f"Zt: {str(zt)}", f"Zalpha: {str(zalpha)}",f"Sample size: {str(self.n1)}",f"Mean: {self.smean1}"]
        return a
    def onep_tdis(self):
        tt=(self.smean1-self.muy)/(self.std1/np.sqrt(self.n1))
        print("Tt: ",tt)
        if self.mode==1:
            talpha=t.ppf(self.alpha,df=self.n1-1)           
        else:
            talpha=t.ppf(self.alpha/2,df=self.n1-1)
        print('Talpha: ',talpha)
        if (tt<talpha) or (tt>-talpha):
            result = "Reject Ho"
        else:
            result = "Do not reject Ho"
        #return result
        a=["Using T-test",result,f"Tt: {str(tt)}", f"Talpha: {str(talpha)}",f"Sample size: {str(self.n1)}",f"Mean: {self.smean1}"]
        return a
class Twopopu:
    def __init__(self,smean1,smean2,D,alpha,std1,std2,n1,n2,mode):
        self.smean1=smean1
        self.smean2=smean2
        self.D=0
        self.alpha=alpha
        self.std1=float(std1)
        self.std2=float(std2)
        self.n1=n1
        self.n2=n2
        self.mode=mode
    def indeZ(self):
        zt=(self.smean1-self.smean2-self.D)/np.sqrt((self.std1**2/self.n1)+(self.std2**2/self.n2))
        print("Zt: ",zt)
        if self.mode==1:
            zalpha=norm.ppf(self.alpha)
        else:
            zalpha=norm.ppf(self.alpha/2)
        print("zalpha: ",zalpha)
        if zt<zalpha or zt>-zalpha:
            result = "Reject Ho"
        else:
            result = "Do not reject Ho" 
        a=["Using Z-test",result, f"Zt: {str(zt)}", f"Zalpha: {str(zalpha)}",f"Sample size1: {str(self.n1)}",f"Sample size2: {str(self.n2)}",f"Mean: {self.smean1}"]
        return a
    def indeT(self,eVar):
        self.eVar=eVar.strip().lower()
        if self.eVar=="no":
            w1=self.std1**2/self.n1
            w2=self.std2**2/self.n2
            dof=floor((w1+w2)**2/(w1**2/(self.n1-1)+w2**2/(self.n2-1))) # Round down
            tt=(self.smean1-self.smean2-self.D)/np.sqrt((self.std1**2/self.n1)+(self.std2**2/self.n2))
            print("Tt: ",tt)
            if self.mode==1:
                talpha=t.ppf(self.alpha,df=dof)           
            else:
                talpha=t.ppf(self.alpha/2,df=dof)
            print('Talpha: ',talpha)
            if (tt<talpha) or (tt>-talpha):
                result = "Reject Ho"
            else:
                result = "Do not reject Ho"
            a=["Using T-test",result, f"Tt: {str(tt)}", f"Zalpha: {str(talpha)}",f"Sample size1: {str(self.n1)}",f"Sample size2: {str(self.n2)}",f"Mean: {self.smean1}"]
            return a
        else:
            sp=((self.n1-1)*(self.std1**2)+(self.n2-1)*(self.std2**2))/(self.n1+self.n2-2)
            dof=self.n1+self.n2-2
            tt=(self.smean1-self.smean2-self.D)/np.sqrt(sp*(1/self.n1+1/self.n2))
            print("Tt: ",tt)
            if self.mode==1:
                talpha=t.ppf(self.alpha,df=dof)           
            else:
                talpha=t.ppf(self.alpha/2,df=dof)
            print('Talpha: ',talpha)
            if (tt<talpha) or (tt>-talpha):
                result = "Reject Ho"
            else:
                result = "Do not reject Ho"
            a=["Using T-test",result, f"Tt: {str(tt)}", f"Talpha: {str(talpha)}",f"Sample size1: {str(self.n1)}",f"Sample size2: {str(self.n2)}",f"Mean: {self.smean1}"]
            return a 
class depend:
    def __init__(self,muyd,D,std,n,mode,alpha):
        self.muyd=muyd
        self.std=std
        self.D=D
        self.n=n
        self.mode=mode
        self.alpha=alpha
    def zdepend(self):
        zt=(self.muyd-self.D)/(self.std/np.sqrt(self.n))
        print("Zt: ",zt)
        if self.mode==1:
            zalpha=norm.ppf(self.alpha)
        else:
            zalpha=norm.ppf(self.alpha/2)
        print("zalpha: ",zalpha)
        if zt<zalpha or zt>-zalpha:
            result = "Reject Ho"
        else:
            result = "Do not reject Ho"

        a=["Using Z-test",result, f"Zt: {str(zt)}", f"Zalpha: {str(zalpha)}",f"Sample size: {str(self.n)}"]
        return a
    def tdepend(self):
        tt=(self.muyd-self.D)/(self.std/np.sqrt(self.n))
        print("Tt: ",tt)
        dof=self.n-1
        if self.mode==1:
            talpha=t.ppf(self.alpha,df=dof)           
        else:
            talpha=t.ppf(self.alpha/2,df=dof)
        print('Talpha: ',talpha)
        if (tt<talpha) or (tt>-talpha):
            result = "Reject Ho"
        else:
            result = "Do not reject Ho"
        a=["Using T-test",result, f"Tt: {str(tt)}", f"Talpha: {str(talpha)}",f"Sample size: {str(self.n)}"]
        return a
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        