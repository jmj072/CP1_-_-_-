# 서울시 강남구 아파트 실거래가 예측하기

## 프로젝트 진행 배경
- 서울은 아파트 가격의 변화가 매우 크며, 다른 지역에 비해 높은 가격대를 형성함
	<img src="https://user-images.githubusercontent.com/77204538/177099290-e81bafb8-786f-4a72-b095-b212d56ccfc1.png" width=800>
	
- 그중 강남3구(강남, 서초, 송파)에 속하는 **강남구**는 서울시 내 다른 지역보다 **높은 가격대를 형성**함

	<img src="https://user-images.githubusercontent.com/77204538/177099294-ecc60dbf-81b4-40cb-be04-c845dc4bba70.png" height=400>
	
- 따라서 강남구는 **서울 지역의 아파트 거래 현황을 대표**할 수 있음

<br>

## 프로젝트 목표
> ☑ 강남구 지역의 아파트 실거래가를 예측하는 모델을 생성하여, **해당 지역에 대한 인사이트**를 얻고자 함  
> ☑ 강남구의 **아파트 정보, 인구학적 정보, 주변 지리적 정보, 경제지표** 가 강남구 **아파트 실거래가에 영향**을 줄 것으로 가정하여 프로젝트를 진행함

<br>

## 개발 환경
- Python 3.8
- Google Colab
- 사용된 library & Tools
  - `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `requests`

## 파일 구성
1. Dataset
   - `1_1_강남_아파트_실거래가예측_최종_2017_2020.csv`
     - EDA와 Feature Engineering에 사용된 데이터셋
     - 좌표 정보와 raw data가  통합되어 있음
   - `1_2_강남_아파트_실거래가예측_for_modeling_2017_2020.csv`
     - 모델링에 사용된 데이터셋

2. 데이터 전처리
	- `2_1_RoadAddress_to_Geocode.py`
    	- 도로명 주소를 위도, 경도 좌표(X, Y 좌표)로 변환
	- `2_2_Calculate_distance.py` 
    	- 위도, 경도좌표를 기반으로 아파트와 각 시설들의 거리를 계산
3. `3_EDA_and_FeatureEngeneering.ipynb`
   - EDA 및 Feature Engineering 진행
4. `4_Modeling.ipynb`
   - Modeling 진행

<br>

## Pipeline
![image](https://user-images.githubusercontent.com/77204538/172564269-b53d8a03-1726-47d2-9c40-fe43b66138f0.png)

<br>

## 1. DataSet

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

## 2. 데이터 전처리


1. 도로명 주소를 경도와 위도로 좌표 변환
   - 아파트 도로명 주소, 강남구,송파구, 서초구 내에 있는 지하철역, 문화시설, 유치원, 학원, 학교의 도로명 주소를 **경도와 위도 좌표로 변환** 
  
   - 오픈 API의 Geocoder를 이용한 변환 ([API 링크](https://www.vworld.kr/dev/v4api.do))
  
	<details>
	<summary>💻 웹 API를 활용한 좌표 변환하는 코드 </summary>
	<div markdown="1">    

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

	</div>
	</details>


<br>

2. 좌표를 기반으로 하여 아파트와 시설간의 거리를 계산
	<details>
	<summary>💻 좌표간 거리를 계산하는 코드 </summary>
	<div markdown="1">  
	
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

	</div>
	</details>
<br>

3. 이후 데이터 통합 후 최종 Dataset 형성

<br>

### 데이터셋 구성
- Target
	- 2017년 ~ 2020년의 강남구 아파트 실거래가
- Feature
	- 아파트 정보 (동, 전용면적, 층, 건축년도)
	- 강남구 인구학적 정보 (인구밀도, 혼인건수)
	- 경제지표 (소비자물가, 가계대출, 기준금리)
	- 아파트 주변 지리 정보(아파트 주변의 유치원, 학교, 학원, 지하철역, 문화시설, 공원의 수, 거리)

<br>

## 3. EDA 및 Feature Engineering

- TOP 10 브랜드 아파트 특성 생성 ([참고링크](http://www.gvalley.co.kr/news/articleView.html?idxno=583178
))
  - 자이, 푸르지오, 더샵, 롯데캐슬, e편한세상, 힐스테이트, 아이파크, 래미안, SKVIEW, 데시앙
  - 아파트 브랜드에 따라서도 아파트 실거래가에 영향을 주는지 살펴보고자 함


- 인구학적 정보 및 경제지표 특성들의 PCA 진행
  - 상관관계 분석 결과, 인구학적 정보 및 경제지표 특성 간의 연관 관계 확인 (상관계수 ≥ 0.3)
  - 다중 공선성 문제를 방지하기 위하여, 특성들의 PCA 진행 ⇒ PC1의 누적 기여율이 80%이므로, PC1만 선택


- 정규분포를 위한 변환
  - Boxcox 변환
    - `거래금액` 
    - Log 변환으로도 해결되지 않아, Boxcox 변환을 시행

  - Log 변환
    - `유치원_최소거리`, `학교_최소거리`, `학원_최소거리`, `문화시설_최소거리`, `공원_최소거리`,`지하철역_최소거리`
    - 정규분포를 나타내지 않아 변환함

- 시계열 데이터를 위한 Cross validation 사용 (TimeSeriesSplit)

<br>

## 4. Modeling
- Linear Regression, Ridge Regression, SVM, Decision Tree Regression, Random Forest Regression,ExtraTree Regression, AdaBoost, XGBoost Regression 모델 비교
- 아파트 가격이 점차 상승하며, Error를 그대로 반영해야 한다고 판단함 ⇒ **MAE를 기준**으로 모델 선택  
- 교차검증을 통해 **Extra Tree Model**로 선정함

![image](https://user-images.githubusercontent.com/77204538/172564576-9ca559fe-15f1-4b6b-8fbc-25f620348da8.png)

<br>

- Grid Search CV를 이용해 Hyper Parameter tuning 진행, 모델 성능을 개선함
  
	| Hyperparameter tuning 	| **조정 전** 	| **조정 후** 	|
	|:---------------------:	|:-----------:	|:-----------:	|
	|        **MAE**        	|    11.22    	|     4.36    	|
	|        **MSE**        	|    224.03   	|    41.10    	|
	|        **RMSE**       	|    14.97    	|     6.41    	|
	|         **R2**        	|     0.86    	|     0.97    	|

	- 예측모델 성능의 시각화 
  
		<img src="https://user-images.githubusercontent.com/77204538/175241625-b71264d9-5735-4cf0-b43c-2df995302c12.png" width="400" height="350">

	- y_true와 y_pred 값의 기울기가 거의 1을 형성

<br>

- Model의 Feature Importance 
  
	<img src="https://user-images.githubusercontent.com/77204538/175229841-c10d1eb6-fdd5-4af3-ad1f-b751c3d40aec.png" width="550" height="350"/>

  - **아파트의 특성(전용면적, 건축연도, 브랜드아파트)**, **아파트 위치에 대한 특성 (아파트가 위치한 동)**, **지역의 인구학적정보 및 경제지표**는 아파트 실거래가를 예측하는데 많은 영향을 준다.

	- `area_range_group(아파트 전용면적)`, `popul_pca(인구학적정보 및 경제지표)`,`construction_year_group(건축연도)`, `Dong_Group(아파트가 위치한 동)`, `top10(TOP10 브랜드아파트 여부)`

<br>

## 5. 결론
> ☑ 아파트 주변에 어떤 시설이 있는지 보다는, **아파트의 평수와 건축연도**, **현재 경제상황**과 **해당 지역의 인구정보**가 아파트 실거래가에 가장 큰 영향을 준다.

<br>

## 6. 한계점 및 개선사항

### 한계점
- 특성 중 아파트 평수에 대한 특성이 거래 금액 예측에 가장 큰 영향을 줌
  - 평수와 관련된 방의 개수, 화장실 개수 등 구체적인 특성으로 분리할 수 있어, 추가적인 데이터를 얻어 자세히 분석할 필요가 있음
  - 아파트 단지 시설 정보(주차장 크기, 개별난방/지역난방 여부, 복도식/계단식 현관 여부 등)를 추가로 수집하여 이러한 특성들도 아파트 실거래가에 영향을 주는지 확인할 필요가 있음
	- Feature Importance 에서 Top 10 브랜드 여부가 아파트 거래 가격에 영향을 주는 것을 확인 → 아파트 건설사에 대한 정보를 추가로 수집하여 확인할 필요가 있음

- 아파트 주변시설 (유치원/학교/학원/문화시설/공원/지하철역)이 아파트 실거래가에 영향을 줄것이라 예상했지만, 영향력이 그다지 크지 않았음
	- 강남구는 학구열이 강한 지역이라는 점을 가정하고 교육시설에 대한 데이터를 분석에 사용 → 주변시설 중에서는 교육시설들이 예측 모델 영향력이 강하게 나타남
	- 다른 편의시설인 병원, 대형마트, 동사무소에 대한 데이터를 추가로 수집하여 확인
	
	
- 인구학적 정보와 경제상황에 대한 특성을 PCA하여 모델에 적용
  -  인구학적 정보와 경제 상황 중 어떤 특성이 더 많이 아파트 가격에 영향을 주는지 알 수 없음
	
- 경제지표에 영향을 강하게 받기 때문에, 금리변동이나 부동산 정책에 의해 아파트 가격이 크게 변동될 수 있음
  - 외부 영향에 의해 아파트 실거래가를 정확히 예측하긴 어려움


### 개선 사항
- 아파트 평수와 관련된 방의 개수, 화장실 개수와 같은 데이터를 추가로 획득하여 아파트 실거래가와의 관계 확인
- 아파트 단지 시설 정보(주차장 크기, 개별난방/지역난방 여부, 복도식/계단식 현관 여부 등)를 추가로 얻어 아파트 실거래가와의 관계 확인
- 아파트 건설사에 대한 정보를 추가하여 건설사 자체도 아파트 실거래가에 영향을 주는 지 확인
- 인구학적 정보/경제상황에 대한 대표 특성을 각각 하나씩 골라 모델에 적용할 것
	- 각각의 대표 특성을 이용해 다중공선성을 최대한 방지하고 어떤 특성이 더 많은 영향을 주는지 확인할 수 있음
- 강남구 외 다른 서울 지역도 동일한 특성들이 강한 영향을 주는지 확인하여, 프로젝트 결과가 강남구만의 특징인지, 다른 지역에서도 나타나는지 확인

<br>

## 어려웠던점

- 프로젝트 초기단계시, 서울시 전체의 데이터셋을 이용해 분석을 진행하려 하였음
  - 서울시 전체에 대한 데이터셋은 약 30만 여개로, 예상보다 많은 데이터를 다루게 되었음
  - 그러나 구체적인 분석 지역의 선정없이, 대용량의 데이터를 목적없이 다루다보니 API 이용과 데이터에 대한 의미 파악이 쉽지않았음
  - 이후에 강남구 지역만을 특정하여 프로젝트를 진행하였으나, 초기에 시간을 많이 소요하여 EDA와 Feature engineering 까지만 진행해 제출함 (프로젝트 종료후 모델링 진행)
  - 어떤 것을 알아보고자 하는지, **명확한 문제 정의**의 중요성을 알게됨
  

- 카카오맵 API를 이용하려다, 제한 쿼리량 초과함
  - 급하게 진행하려다 소량의 데이터가 아닌, 전체 데이터를 일단 돌려보자라는 식으로 진행
  - 중간 중간 에러로인해 여러번 시도하게 되자, 제한 쿼리량을 초과함
  - 아무리 급하더라도 항상 할 수 있는 쿼리량을 확인하고, 테스트는 소량으로만 진행해야한다는 걸 느꼈음


<br>

*프로젝트의 자세한 사항은 다음 [PPT 자료](https://drive.google.com/file/d/1rcL3RpNgIwTMkS1siPjwHFb2W7jP-AIG/view?usp=sharing)를 확인해주세요*
