# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 16:38:41 2022

@author: skyto
"""
import time
import requests
import pandas as pd
import numpy as np
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, quote

def Roadaddress_to_Geocode (addr):
    """
    [input]
    도로명 주소

    [return]
    위도, 경도
    """
    vworld_apikey = 'B1FBD8E3-4A8B-3427-97BF-767A7EC59EE5'
    url = "http://api.vworld.kr/req/address?service=address&request=getCoord&type=ROAD&refine=false&key=%s&" % (vworld_apikey) + urlencode({quote_plus('address'):addr}, encoding='UTF-8')
    
    try:
        request = Request(url)
        response = urlopen(request)
        rescode = response.getcode()
        print(response)
        
        if rescode == 200:
            response_body = response.read().decode('utf-8')
            jsonData = json.loads(response_body)
            try:
                lat = float(jsonData['response']['result']['point']['y'])
                lng = float(jsonData['response']['result']['point']['x'])
                return lat, lng
            except:
                print('error')
                return None, None
        else:
           print('error code:', rescode)
           return None, None
    except:
        print('5초 뒤에 다시 실행합니다.')
        time.sleep(5)
        return Roadaddress_to_Geocode(addr)


#print(Roadaddress_to_Geocode('서울특별시 송파구 위례북로2길 10'))

#df = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_송파_서초_학원.csv')
df = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_강북_아파트_실거래가예측_2017.csv')

arr = []
for index, row in df.iterrows() :
    temp_array = np.array(Roadaddress_to_Geocode(row['도로명주소']))
    arr.append(temp_array)
    df_cord = pd.DataFrame(arr, columns = ['X좌표','Y좌표'])
    print(df_cord.tail())
df['X좌표'] = df_cord['X좌표']
df['Y좌표'] = df_cord['Y좌표']
df.to_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_강북_아파트_실거래가예측_좌표추가_2017.csv',encoding='utf-8-sig')
