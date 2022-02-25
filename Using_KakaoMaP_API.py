

def find_numbers_and_min_distance_from_keyword (keyword,x, y, radius):
    """
    중심좌표로 부터 반경 내  keyword에 해당하는 지역을 검색하여 시설 갯수와 가장 가까운 시설의 거리를 반환
    [input]
    keyword = 검색 키워드 ex)공원, 주소 등..
    x = 중심 좌표의 X값 혹은 longitude
    y = 중심 좌표의 Y값 혹은 latitude
    radius = 중심 좌표부터의 반경거리, 단위 meter, 0~20000 사이의 값

    [return]
    numbers = 반경내 시설의 개수
    min_distance = 반경 내 시설 중, 제일 짧은 거리 (단위 : meter)
    """

    headers = {"Authorization": "KakaoAK ed025c9a98d54138f67d57df53724d89"}
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json' 
    params = {'query' : keyword,
              'x': x,
              'y': y,
              'radius': radius, #기준거리 (단위 : meter)
              'sort':'distance' #거리가 가까운 순서대로 보여줘
              }
    try:  
        json_data = requests.get(url, headers = headers, params = params).json()
        numbers = json_data['meta']['total_count']
        min_distance = json_data['documents'][0]['distance']
        return numbers, min_distance
    except:
        print(f'좌표가 존재하지 않습니다. None을 반환합니다.')
        return None, None

##################################
            
def find_numbers_and_min_distance_from_category_code (x, y, category_group_code, radius):
    """
    [input]
    x = 중심 좌표의 X값 혹은 longitude
    y = 중심 좌표의 Y값 혹은 latitude
    category_group_code = {MT1 : 대형마트, CS2 : 편의점, PS3 : 어린이집, 유치원, SC4 :학교, AC5 : 학원,
    PK6 :주차장, OL7: 주유소, 충전소, SW8 :지하철역, BK9:은행,CT1:문화시설,AG2:중개업소,PO3:공공기관,
    AT4 : 관광명소, AD5:숙박, FD6:음식점, CE7: 카페,HP8:병원, PM9:약국}
    radius = 중심 좌표부터의 반경거리, 단위 meter, 0~20000 사이의 값

    [return]
    numbers = 반경내 시설의 개수
    min_distance = 반경 내 시설 중, 제일 짧은 거리 (단위 : meter)
    """
    headers = {"Authorization": "KakaoAK bb5eebc45372a1047d206f308f89ce66"}
    url = 'https://dapi.kakao.com/v2/local/search/category.json' 
    params = {'category_group_code' : category_group_code,
                    'x': x,
                    'y': y,
                    'radius':radius, #기준거리 (단위 : meter)
                    'sort':'distance' #거리가 가까운 순서대로 보여줘
                    }
    try:  
        json_data = requests.get(url, headers = headers, params = params).json()
        numbers = json_data['meta']['total_count']
        min_distance = json_data['documents'][0]['distance']
        return numbers, min_distance
    except:
        print(f'좌표가 존재하지 않습니다. None을 반환합니다.')
        return None, None            

################################################################################
            
import requests
import pandas as pd
import numpy as np

df = pd.read_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_아파트_실거래가예측_좌표추가_2018_2020.csv')

# 학교
arr = []
for index, row in df.iterrows() :
    temp_array = np.array(find_numbers_and_min_distance_from_category_code(row['X좌표'], row['Y좌표'], 'SC4', 1000)) #1km 내 학교
    arr.append(temp_array)
    df_temp = pd.DataFrame(arr, columns = ['1km내_학교수','학교_최소거리'])
    print()
    print(df_temp.tail())
df['1km내_학교수'] = df_temp['1km내_학교수']
df['학교_최소거리'] = df_temp['학교_최소거리']

df_temp.to_csv('G:\내 드라이브\CodeStates\CP1\데이터_병합_수정\강남_아파트_실거래가예측_예비2_2018_2020.csv',encoding='utf-8-sig')