# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 17:24:20 2022

@author: skyto
"""
import pandas as pd
import numpy as np
from haversine import haversine

#df = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_아파트_실거래가예측_좌표추가_2018_2020.csv')
df = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_강북_아파트_실거래가예측_좌표추가_2017.csv')
df_kinder = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_송파_서초_유치원_좌표추가.csv')
df_study = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_송파_서초_학원_좌표추가.csv')
df_school = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_송파_서초_학교_좌표추가.csv')
df_sub = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_송파_서초_지하철역_좌표입력.csv')
df_culture = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_송파_서초_문화시설.csv')
df_park = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_송파_서초_공원.csv')

df.dropna(inplace=True)
df_kinder.dropna(inplace=True)
df_study.dropna(inplace=True)
df_school.dropna(inplace=True)
df_sub.dropna(inplace=True)
df_culture.dropna(inplace=True)
df_park.dropna(inplace=True)

df.reset_index(drop=True, inplace = True)


#df['경도']= df['X좌표']
#df['위도']= df['Y좌표']
df['경도']= df['Y좌표']
df['위도']= df['X좌표']

df_kinder['경도']= df_kinder['Y좌표']
df_kinder['위도']= df_kinder['X좌표']

df_study['경도']= df_study['Y좌표']
df_study['위도']= df_study['X좌표']

df_school['경도']= df_school['Y좌표']
df_school['위도']= df_school['X좌표']

df_culture['경도']= df_culture['Y좌표']
df_culture['위도']= df_culture['X좌표']

# =============================================================================
# haversine(lyon, paris)
# (lat, lon)
# 거리구하기
# 아파트 좌표를 기준으로, 거리를 계산함

result = []

for inx, row in df.iterrows():
    lat_1 = row['위도']  #아파트 latitude (위도)
    lon_1 = row['경도']  #아파트 longitude (경도)
    start = (lat_1, lon_1)
    print(f'{inx}번째 아파트 계산 시작')

    distance_result = []
    
    for inx, row in df_kinder.iterrows():
        lat_2 = row['위도']
        lon_2 = row['경도']
        end = (lat_2, lon_2)
        distance = haversine(start, end)  #기본단위 : km
        if distance <= 1.0:
            distance_result.append(distance)
        else:
            continue
    try:
        min_distance = min(distance_result)
        Nums_in_1km = len(distance_result)
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
    except:  # 가까운 유치원이 없을경우..
        min_distance = 0
        Nums_in_1km = 0
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
        

df_temp = pd.DataFrame(result, columns = ['1km내_유치원수','유치원_최소거리'])
df['1km내_유치원수'] = df_temp['1km내_유치원수']
df['유치원_최소거리'] = df_temp['유치원_최소거리']

#df.to_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_아파트_실거래가예측_유치원추가_2018_2020.csv',encoding='utf-8-sig')
# =============================================================================



result = []

for inx, row in df.iterrows():
    lat_1 = row['위도']  #아파트 latitude (위도)
    lon_1 = row['경도']  #아파트 longitude (경도)
    start = (lat_1, lon_1)
    print(f'{inx}번째 아파트 계산 시작')
    distance_result = []
    
    for inx, row in df_sub.iterrows():   # 이것만 수정할것
        lat_2 = row['위도']
        lon_2 = row['경도']
        end = (lat_2, lon_2)
        distance = haversine(start, end)  #기본단위 : km
        if distance <= 1.0:
            distance_result.append(distance)
        else:
            continue
    try:
        min_distance = min(distance_result)
        Nums_in_1km = len(distance_result)
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
    except:  # 가까운 유치원이 없을경우..
        min_distance = 0
        Nums_in_1km = 0
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
        
        
df_temp_sub = pd.DataFrame(result, columns = ['1km내_지하철역수','지하철역_최소거리'])
df['1km내_지하철역수'] = df_temp_sub['1km내_지하철역수']
df['지하철역_최소거리'] = df_temp_sub['지하철역_최소거리']


# =============================================================================

result = []

for inx, row in df.iterrows():
    lat_1 = row['위도']  #아파트 latitude (위도)
    lon_1 = row['경도']  #아파트 longitude (경도)
    start = (lat_1, lon_1)
    print(f'{inx}번째 아파트 계산 시작')
    distance_result = []
    
    for inx, row in df_culture.iterrows():   # 이것만 수정할것
        lat_2 = row['위도']
        lon_2 = row['경도']
        end = (lat_2, lon_2)
        distance = haversine(start, end)  #기본단위 : km
        if distance <= 1.0:
            distance_result.append(distance)
        else:
            continue
    try:
        min_distance = min(distance_result)
        Nums_in_1km = len(distance_result)
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
    except:  # 가까운 유치원이 없을경우..
        min_distance = 0
        Nums_in_1km = 0
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
        
df_temp_culture = pd.DataFrame(result, columns = ['1km내_문화시설수','문화시설_최소거리'])
df['1km내_문화시설수'] = df_temp_culture['1km내_문화시설수']
df['문화시설_최소거리'] = df_temp_culture['문화시설_최소거리']

# =============================================================================

result = []

for inx, row in df.iterrows():
    lat_1 = row['위도']  #아파트 latitude (위도)
    lon_1 = row['경도']  #아파트 longitude (경도)
    start = (lat_1, lon_1)
    print(f'{inx}번째 아파트 계산 시작')
    distance_result = []
    
    for inx, row in df_park.iterrows():   # 이것만 수정할것
        lat_2 = row['위도']
        lon_2 = row['경도']
        end = (lat_2, lon_2)
        distance = haversine(start, end)  #기본단위 : km
        if distance <= 1.0:
            distance_result.append(distance)
        else:
            continue
    try:
        min_distance = min(distance_result)
        Nums_in_1km = len(distance_result)
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
    except:  # 가까운 유치원이 없을경우..
        min_distance = 0
        Nums_in_1km = 0
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
        
df_temp_park = pd.DataFrame(result, columns = ['1km내_공원수','공원_최소거리'])
df['1km내_공원수'] = df_temp_park['1km내_공원수']
df['공원_최소거리'] = df_temp_park['공원_최소거리']

# =============================================================================

result = []

for inx, row in df.iterrows():
    lat_1 = row['위도']  #아파트 latitude (위도)
    lon_1 = row['경도']  #아파트 longitude (경도)
    start = (lat_1, lon_1)
    print(f'{inx}번째 아파트 계산 시작')
    distance_result = []
    
    for inx, row in df_school.iterrows():   # 이것만 수정할것
        lat_2 = row['위도']
        lon_2 = row['경도']
        end = (lat_2, lon_2)
        distance = haversine(start, end)  #기본단위 : km
        if distance <= 1.0:
            distance_result.append(distance)
        else:
            continue
    try:
        min_distance = min(distance_result)
        Nums_in_1km = len(distance_result)
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
    except:  # 가까운 유치원이 없을경우..
        min_distance = 0
        Nums_in_1km = 0
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
        
df_temp_school = pd.DataFrame(result, columns = ['1km내_학교수','학교_최소거리'])
df['1km내_학교수'] = df_temp_school['1km내_학교수']
df['학교_최소거리'] = df_temp_school['학교_최소거리']

#=============================================================================

result = []

for inx, row in df.iterrows():
    lat_1 = row['위도']  #아파트 latitude (위도)
    lon_1 = row['경도']  #아파트 longitude (경도)
    start = (lat_1, lon_1)
    print(f'{inx}번째 아파트 계산 시작')
    distance_result = []
    
    for inx, row in df_study.iterrows():   # 이것만 수정할것
        lat_2 = row['위도']
        lon_2 = row['경도']
        end = (lat_2, lon_2)
        distance = haversine(start, end)  #기본단위 : km
        if distance <= 1.0:
            distance_result.append(distance)
        else:
            continue
    try:
        min_distance = min(distance_result)
        Nums_in_1km = len(distance_result)
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
    except:  # 가까운 유치원이 없을경우..
        min_distance = 0
        Nums_in_1km = 0
        temp_array = [Nums_in_1km, min_distance]
        result.append(temp_array)
        print(result[-1])
        
df_temp_study = pd.DataFrame(result, columns = ['1km내_학원수','학원_최소거리'])
df['1km내_학원수'] = df_temp_study['1km내_학원수']
df['학원_최소거리'] = df_temp_study['학원_최소거리']


#=============================================================================
# 최종 결과 저장
#df.to_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_아파트_실거래가예측_최종_2018_2020.csv',encoding='utf-8-sig')
df.to_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_아파트_실거래가예측_최종_2017.csv',encoding='utf-8-sig')
