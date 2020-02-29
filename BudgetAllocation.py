# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 19:05:50 2020

@author: Ankit
"""


import json
import requests
import urllib.parse
from pandas.io.json import json_normalize 
import pandas as pd
import numpy as np
import copy
from datetime import datetime



from aes256 import aes256


    
class BudgetAllocation:
    
    def allocate(self ,month,year, band,amount,l0amount,levels,cityid,warehouseid):
    
    
    ## getting data:- reading data from the api in json format and converting it into python dataframe using json_normalize
    
    
        # url = "http://111.118.252.170:8181/api/Customers/GetCustDetailLabel?month=%s&year=%s" % (month, year)
        # url = "http://192.168.1.113/api/Customers/GetCustDetailLabel?month=%s&year=%s" % (month, year)
    
        url = "https://uat.shopkirana.in/api/Customers/GetCustDetailLabel?month=%s&year=%s" % (month,year)
        resp = requests.get(url)
        json_data = resp.json()
    
    
        if(json_data['Status'] =="OK"):
            redisAesKey = datetime.today().strftime('%Y%m%d') + "1201"
            jso = aes256().decrypt(json_data["Data"],redisAesKey)
            js = json.loads(jso)
            df = json_normalize(js)
            df=df.loc[df['IsActive'] == True]
    
    
    ##  levelling :- segregating the customers into levels using definition below and storing each level into the list
    
        df.loc[df.Volume == 0, 'levels'] = 'level_0'
        df.loc[df.Volume >= 1, 'levels'] = 'level_1'
        df.loc[(df.Volume >= 10000) & (df.OrderCount >= 3) & (df.BrandCount  >= 5), 'levels'] = 'level_2'
        df.loc[(df.Volume >= 20000) & (df.OrderCount >= 5) & (df.BrandCount  >= 10) & (df.kkVolumn >= 2000), 'levels'] = 'level_3'
        df.loc[(df.Volume >= 30000) & (df.OrderCount >= 8) & (df.BrandCount  >= 20) & (df.kkVolumn >= 8000) & ((df.Selfordercount/(df.Salespersonordercount+df.Selfordercount))*100 > 30), 'levels'] = 'level_4'
        df.loc[(df.Volume >= 75000) & (df.OrderCount >= 12) & (df.BrandCount >= 40) & (df.kkVolumn >= 15000) & ((df.Selfordercount/(df.Salespersonordercount+df.Selfordercount))*100 > 60), 'levels'] = 'level_5'
        
        dfL0 = df.loc[df.levels == 'level_0']
        dfL1 = df.loc[df.levels == 'level_1'] 
        dfL2 = df.loc[df.levels == 'level_2']
        dfL3 = df.loc[df.levels == 'level_3']
        dfL4 = df.loc[df.levels == 'level_4']
        dfL5 = df.loc[df.levels == 'level_5']
        
        l = (dfL0 , dfL1 , dfL2 , dfL3 , dfL4 ,dfL5)
    
    
    
    ## Status :- based on the bands giving status to the skcode (promotion , retention , consistent) . bands are based on percentile . 
    # for example : - in band1 above 90 percentile is promotion and below 10% is retention and between 90 - 10 percentile is consistent 
    
        b = band
        l = list(l) 
        i = level
        df1 = copy.deepcopy(l[i])
    
        if (b == 1):
                
                df1.loc[(df1.Volume >= df1.Volume.quantile(0.9)) , 'status'] = 'Promotion'   #  Above 90 percentile Promotion              
                df1.loc[(df1.Volume <= df1.Volume.quantile(0.1)) , 'status'] = 'Retention'   #  Below 10 percentile Retention
                df1.loc[(df1.Volume > df1.Volume.quantile(0.1)) & (df1.Volume < df1.Volume.quantile(0.9)), 'status'] = 'Consistent' # between 90 and 10 percentile is consistent
                
         
        elif (b == 2):
                  
                df1.loc[(df1.Volume >= df1.Volume.quantile(0.8)) , 'status'] = 'Promotion'   #  Above 80 percentile Promotion
                df1.loc[(df1.Volume <= df1.Volume.quantile(0.2)) , 'status'] = 'Retention'   #  Below 20 percentile Retention  
                df1.loc[(df1.Volume > df1.Volume.quantile(0.2)) & (df1.Volume < df1.Volume.quantile(0.8)), 'status'] = 'Consistent' # between 80 and 20 percentile is consistent
    
            
            
        elif (b == 3):
             
                df1.loc[(df1.Volume >= df1.Volume.quantile(0.7)) , 'status'] = 'Promotion'    #  Above 70 percentile Promotion
                df1.loc[(df1.Volume <= df1.Volume.quantile(0.3)) , 'status'] = 'Retention'    #  Below 30 percentile Retention
                df1.loc[(df1.Volume > df1.Volume.quantile(0.3)) & (df1.Volume < df1.Volume.quantile(0.7)), 'status'] = 'Consistent'  # between 70 and 30 percentile is consistent
    
      
            
                
        elif(b == 4):
       
                df1.loc[(df1.Volume >= df1.Volume.quantile(0.6)) , 'status'] = 'Promotion'     #  Above 60 percentile Promotion
                df1.loc[(df1.Volume <= df1.Volume.quantile(0.4)) , 'status'] = 'Retention'     #  Above 40 percentile Promotion
                df1.loc[(df1.Volume > df1.Volume.quantile(0.4)) & (df1.Volume < df1.Volume.quantile(0.6)), 'status'] = 'Consistent'  # between 60 and 40 percentile is consistent
    
       
    
    
    
    ##  allocation :-  allocating the amount based on the proportion of share in total volume during the month
    
    
        Total = 0
        
        for i in range(0,6): 
        
            Total = Total + l[i]['Volume'].sum()
    
               
        if (level != 0):
            l_amount = (df1['Volume'].sum() / Total) * amount      # each level will be allocated based on the proportion of share in total volume
            pro_c=df1.loc[df1.status == 'Promotion']['SkCode'].count()
            ret_c=df1.loc[df1.status == 'Retention']['SkCode'].count()
    
            
            pro_am = l_amount / 2                            # promotion amount and retention amount will be 50% i.e half of total volume 
            
            
            if ((pro_c != 0) & (ret_c != 0)):
                pro_all=int(pro_am / pro_c)                    #promotion amount will be distributed equally among  promotion customers similar is case with retention customers
                ret_all=int(pro_am / ret_c)
                
            else :
                pro_all = 0
                ret_all = 0
                           
            
            df1.loc[df1.status == 'Promotion', 'allocation'] = str(pro_all)
            df1.loc[df1.status == 'Retention', 'allocation'] = str(ret_all)
            df1.loc[df1.status == 'Consistent', 'allocation'] = str(0)
    
    
        else:
            pro_c0 = df['SkCode'].count()                                 # for level0 (l0) there will be seperate allocation and it will be allocated equally among customers
            l0_all = l0amount/pro_c0
            df1.loc[df1.status == 'Promotion', 'allocation'] = str(l0_all)
            df1.loc[df1.status == 'Retention', 'allocation'] = str(l0_all)
            df1.loc[df1.status == 'Consistent', 'allocation'] = str(l0_all)

    
            
        df1 = df1.loc[(df1.Cityid == cityid) & (df1.WarehouseId == warehouseid)]
        df1= df1.to_json(orient='records')
        return df1 

        





















