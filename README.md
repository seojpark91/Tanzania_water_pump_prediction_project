# 지속가능한 식수 사업을 위한 탄자니아 수도 펌프 작동 여부 분류 프로젝트
## Water Pump Functionality Prediction Project for sustainable water supply in Tanzania
<img src="img/pumping.jpg" width="600" height="300" />


## Objective : How to solve a problem of unsustainable water supply service?
어떤 요인들이 고장난 식수 펌프 작동 고장에 영향을 주는 것일까?

- 목적: 식수 펌프가 언제 지어졌는지, 누가 관리를 해오고 있는지, 무엇으로 지어졌는지, 지어진 지역/마을의 정보, 물의 질과 양 등의 40개의 각 식수 펌프에 대한 피쳐들로 식수 펌프의 작동 여부 예측하여 어떤 피쳐가 가장 큰 영향을 주는지를 알아보자

- Objective: Predict the operating condition of a water pump ( one of three target classes: 'funcional', 'functional needs repair', 'nonfunctional') based on a number of variables about what kind of pump is operating, when it was installed, and how it is managed, and more.


- 백그라운드 : 2009년도 UNICEF 데이터에 따르면 이남 아프리카 (sub-Saharan Africa) 에 매년 60,000개 정도의 식수 펌프가 다양한 비영리단체/ 국제기구/ 정부단체에 의해 지어진다 (Sansom and Koestler 2009). 하지만 [Rural Water Supply Network](www.rural-water-supply.net)에 의하면 이렇게 식수 사업으로 아프리카에 설치된 식수펌프 중 30-40%가 작동 하지 않는다. 세계 은행 [World Bank](https://www.theguardian.com/global-development-professionals-network/2016/mar/22/how-do-you-solve-a-problem-like-a-broken-water-pump)은 약 12억 달러의 투자금이 지난 20여년 동안 고장나서 버려진 식수 펌프로 인해 낭비되어왔다고 예측한다. 전문가들은 쉽게 망가지는 식수 펌프에 영향을 주는 요인을 크게 3가지로 보고 있다. (1) 식수 펌프가 저렴한 금속으로 해외에서 제작되어 오기에 고장 나기 쉽다. (2) 식수 펌프와 지하수를 연결하기 위해 드릴을 하는 장소가 잘못 되었거나, 잘못된 방법으로 드릴을 했기 때문이며, (3) 지속적으로 관리를 해주는 on site supervisor가 존재하지 않기 때문이라고 말한다. 주어진 데이터를 통해 어떤 요인들이 식수 펌프 작동에 큰 영향을 주는지를 알아보는 것이 이 프로젝트의 목적이다. 

- Background : According to a study conducted in 2009 by UNICEF, around 60,000 handpumps are installed across sub-Saharan Africa every year. However, about 30 to 40% of those in the region do not work at any one time. The World Bank estimated that over the last 20 years, waterpump failure represents a loss of investment of more than 1.2 billion dollar. Experts point at 3 major reasons behind water pump failure. First, most waterpumps are manufactured with poor quality metal outside of the region (usually manufactured in India), which makes it hard to enforce quality control. Moreover, water pumps stop working because the borehole which a pump extracts groundwater through was drilled in the wrong place or the wrong way. Lastly, a lack of on site supervisors and skilled drillers exacerbates the problem of unsustainable water supply service. Therefore, given a set of variables of the data, I would like to explore which factors affect the functionality of water pumps the most. 

Reference: [The Guardian](https://www.theguardian.com/global-development-professionals-network/2016/mar/22/how-do-you-solve-a-problem-like-a-broken-water-pump)

## The Data
#### Source : DrivenData, Basic Statistics Portal of Tanzania 
사용된 데이터는 [Drivendata](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/page/23/)에서 현재 competition 진행 중인 데이터이며, [Taarifa](http://taarifa.org/)라는 크라우드 소싱 리포팅 오픈 소스 플랫폼과 탄자니아 정부에서 제공한 탄자니아에 지어진 59,400개의 식수 펌프 데이터 이다. 또한, 누락 데이터로 인한 정보의 손실을 탄자니아 통계 포털 [Basic Statistics Portal](http://statistics.go.tz/dataset/idadi-ya-watu-kwa-ngazi-ya-vijiji-mtaa-kwa-sensa-ya-mwaka-2012) 에서 2012년도 마을 별 인구 자료를 사용하여 변환하였다. 

The data comes from [Drivendata](https://www.drivendata.org/competitions/7/pump-it-up-data-mining-the-water-table/page/23/), which is provided by [Taarifa](http://taarifa.org/) (an open source platform for the crowd sourced reporting and triaging of infrastructure related issues) and the Tanzanian Ministry of Water. Additionally, in order to impute missing values, I used a 'villaage-statistics' data of 2012 from [Basic Statistics Portal](http://statistics.go.tz/dataset/idadi-ya-watu-kwa-ngazi-ya-vijiji-mtaa-kwa-sensa-ya-mwaka-2012).

#### Feature information : 
| type | name | count |
|-|-|-|
| string | <small> date recorded, funder, installer, managing group, quality, name of pump, geographic location (region, lga, ward, village), recorded by, extraction type, group, and class, payment, quality, source, water point type </small> | <small> 29 </small> |
| int | <small> construction year, quantity, population, region code, district code, id</small> | <small>7 </small> 
| float | <small> longitude, latitude, amount of water, height of pump </small> | <small> 3 </small> |
| Boolean | <small> permit </small> | <small>1</small> |
| &nbsp;| &nbsp;| <small>40</small> |


`amount_tsh` - 우물에 있는 물의 양, amount of water   
`date_recorded` - 데이터가 기록된 날짜 (년/월/일), The date the row was entered   
`funder` - 우물 설치 자금 지원자/기관, Who funded the well   
`gps_height` - 우물의 높이, Altitude of the well  
`installer` - 우물 설치자/기관, Organization that installed the well  
`longitude` - 경도  
`latitude` - 위도  
`wpt_name` - 우물 이름, Name of the waterpoint if there is one  
`num_private` - 정보 없음, no information available for this feature    
`basin` - 가까운 분지, Geographic water basin  
`subvillage` - 서브빌리지, subvillage   
`region` - 지역, Geographic location  
`region_code` - 지역 코드, Geographic location (coded)   
`district_code` - 지구 코드, Geographic location (coded)   
`lga` - 지방 정부, Local Government Authorization  
`ward` - 행정 구역, Geographic location  
`population` - 우물 주변 인구 수, Population around the well  
`public_meeting` - 우물 주변이 마을 모임 장소로 열리는지 유무, True/False  
`recorded_by` - 작성자/기관, Group entering this row of data  
`scheme_management` - 우물 운영 기관, Who operates the waterpoint  
`scheme_name` - 우물 운영 기관, Who operates the waterpoint  
`permit` - 우물의 허가증 유무, If the waterpoint is permitted  
`construction_year` - 우물 지어진 년도, Year the waterpoint was constructed  
`extraction_type` - 펌프 종류, The kind of extraction the waterpoint uses  
`extraction_type_group` - 파이프 종류, The kind of extraction the waterpoint uses   
`extraction_type_class` - 파이프 종류, The kind of extraction the waterpoint uses   
`management` - 우물 운영 기관, How the waterpoint is managed   
`management_group` - 우물 운영 기관, How the waterpoint is managed   
`payment` - 우물 관리 비 지불 방식, What the water costs   
`payment_type` - 우물 관리 비 지불 방식, What the water costs  
`water_quality` - 물의 질, The quality of the water  
`quality_group` - 물의 질, The quality of the water  
`quantity` - 물의 양, The quality of the water  
`quantity_group` - 물의 양, The quality of the water  
`source` - 식수원, The source of the water  
`source_type` - 식수원, The source of the water  
`source_class` - 식수원, The source of the water  
`waterpoint_type` - 펌프 종류, The kind of waterpoint  
`waterpoint_type_group` - 펌프 종류, The kind of waterpoint  

#### Target - 3 classes

| Target | percentage |
|-|-|
| functional | <small> 54.31 </small> | 
| non functional | <small> 38.42 </small> | 
| functional needs repair | <small> 7.27 </small> | 