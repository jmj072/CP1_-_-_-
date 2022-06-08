# 서울시 강남구 아파트 실거래가 예측하기

- 부동산 투자에 대한 관심이 높아지면서, 아파트 거래 가격의 상승과 하락을 예측하고자 하는 시도들이 많음
- 특히 서울은 아파트 가격의 변화가 매우 크며, 다른 지역에 비해 높은 가격대를 형성함
- 그중 강남3구(강남, 서초, 송파)에 속하는 **강남구**는 서울시 내 다른 지역보다 **높은 가격대를 형성**함
- 따라서 강남구는 **서울 지역의 아파트 거래 현황을 대표**할 수 있음 => 가격대를 높게 형성하게 하는 요인을 분석하여 강남구 뿐만 아니라 **다른 지역의 아파트 거래 현황의 이해도를 높일 수 있음**
- [[프로젝트 상세] 발표 PPT File 링크](https://drive.google.com/file/d/1mo3khiYjkwgXJSDIPR528bEF0EDocwLX/view?usp=sharing)

<br>

## 파일 구성
- Dataset
	- `강남_아파트_실거래가예측_최종_2017_2020.csv` : EDA와 Feature Engineering에 사용된 데이터셋. 좌표 정보와 raw data가  통합되어 있음
	- `강남_아파트_실거래가예측_for_modeling_2017_2020.csv` : 모델링에 사용된 데이터셋
- 데이터 전처리
	- `RoadAddress_to_Geocode.py` : 도로명 주소를 위도, 경도 좌표(X, Y 좌표)로 변환
	- `Calculate_distance.py` : 위도, 경도좌표를 기반으로 아파트와 각 시설들의 거리를 계산
- `EDA_and_FeatureEngeneering.ipynb` : EDA 및 Feature Engineering 진행
- `Modeling.ipynb` : Modeling 진행

<br>

## 개발 환경
- Python 3.8
- Google Colab

## Pipeline
![image](https://user-images.githubusercontent.com/77204538/172564269-b53d8a03-1726-47d2-9c40-fe43b66138f0.png)

<br>

## DataSet

- 국토교통부 실거래가 공개 시스템 (http://rtdown.molit.go.kr/)
	- 2017년~2020년 까지의 강남구 아파트에 대한 실거래현황 데이터 확보
	- 거래된 아파트의 주소, 전용면적, 층수, 건축년도, 계약날짜,실거래가 데이터 확보

- 서울 열린 데이터광장 (https://data.seoul.go.kr/)
	- 2017년~2020년 서울시 연별 인구밀도 (동별) 통계 데이터 확보
	- 2017년~2020년 서울시 월별 혼인건수 통계 데이터 확보
	- 2017~2020년 서울시 월별 소비자 물가지수 데이터 확보
	- 서울교통공사 지하철역 주소 (강남, 서초, 송파) 데이터 확보
	- 서울시 문화시설,주요 공원 주소 (강남, 서초, 송파) 데이터 확보
	- 서울시 유치원, 학원, 학교 주소 (강남, 서초, 송파) 데이터 확보

- 주택금융통계시스템(https://www.hf.go.kr/research/portal/main/indexPage.do)
	- 2017~2020년 서울시 월별 가계대출 데이터 확보
	- 2017~2020년 한국은행 기준금리 데이터 확보

<br>

### 데이터 전처리
#### 도로명 주소를 경도와 위도로 좌표 변환
- 아파트 도로명 주소, 강남구,송파구, 서초구 내에 있는 지하철역, 문화시설, 유치원, 학원, 학교의 도로명 주소를 **경도와 위도 좌표로 변환** 
- 오픈 API의 Geocoder를 이용한 변환 ([링크](https://www.vworld.kr/dev/v4api.do))
- **[API를 활용한 변환과정]**
	```python
	def  Roadaddress_to_Geocode (addr):
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

			if  rescode == 200:
				response_body = response.read().decode('utf-8')
				jsonData = json.loads(response_body)
			try:
				lat = float(jsonData['response']['result']['point']['y'])
				lng = float(jsonData['response']['result']['point']['x'])
				return  lat, lng

			except:
				print('error')
				return  None, None

		else:
			print('error code:', rescode)
			return  None, None
			except:
			print('5초 뒤에 다시 실행합니다.')
			time.sleep(5)
			return  Roadaddress_to_Geocode(addr)
	```

<br>

#### 좌표 변환 후, 좌표간 거리를 계산
- Python 라이브러리인 `haversine` 을 이용함
- **[라이브러리 설치]**
	```python
	pip install haversine
	```
- **[거리 계산 과정]**
	```python
	result = []

	for  inx, row  in  df.iterrows():
		lat_1 = row['위도'] #아파트 latitude (위도)
		lon_1 = row['경도'] #아파트 longitude (경도)
		start = (lat_1, lon_1)
		print(f'{inx}번째 아파트 계산 시작')
		  
		distance_result = []
		for  inx, row  in  df_kinder.iterrows():
		lat_2 = row['위도']
		lon_2 = row['경도']
		end = (lat_2, lon_2)
		distance = haversine(start, end) #기본단위 : km
		if  distance <= 1.0:
			distance_result.append(distance)

		else:
			continue
			
		try:
			min_distance = min(distance_result)
			Nums_in_1km = len(distance_result)
			temp_array = [Nums_in_1km, min_distance]
			result.append(temp_array)
			print(result[-1])

		except: # 가까운 유치원이 없을경우..
			min_distance = 0
			Nums_in_1km = 0
			temp_array = [Nums_in_1km, min_distance]
			result.append(temp_array)
			print(result[-1])

	df_temp = pd.DataFrame(result, columns = ['1km내_유치원수','유치원_최소거리'])
	df['1km내_유치원수'] = df_temp['1km내_유치원수']
	df['유치원_최소거리'] = df_temp['유치원_최소거리']
	```
- 이후 데이터 통합 후 최종 Dataset 형성

<br>

### 데이터 구성
> 가정 : 아파트 정보, 인구학적 정보, 지리적 정보, 경제지표가 강남구 아파트 실거래가에 영향을 줄 것이다.
- Target
	- 2017년 ~ 2020년의 강남구 아파트 실거래가
- Feature
	- 아파트 정보 (위치, 전용면적, 층, 건축년도)
	- 강남구 인구학적 정보 (인구밀도, 혼인건수)
	- 경제지표 (소비자물가, 가계대출, 기준금리)
	- 지리적 정보(아파트 주변의 유치원, 학교, 학원, 지하철역, 문화시설, 공원의 수, 거리)

<br>

## Modeling
- 교차검증을 통해 Extra Tree Model로 선정함

![image](https://user-images.githubusercontent.com/77204538/172564576-9ca559fe-15f1-4b6b-8fbc-25f620348da8.png)

<br>

- Grid Search CV를 이용해 Hyper Parameter tuning 진행, 모델 성능을 개선함
- Mean Absolute Error : 15.32 => 15.22 (0.1 감소)

![image](https://user-images.githubusercontent.com/77204538/172564642-eb353272-c307-4bf1-bd8d-7addf436ea4c.png)

