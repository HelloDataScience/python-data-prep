# 파이썬 데이터 수집과 전처리

파이썬으로 **웹 데이터를 수집하고, 분석할 수 있는 형태로 전처리하는 과정**을 다루는 강의 자료입니다.

2023년 9월부터 2026년 7월까지 삼성SDS 임직원을 대상으로 진행한 강의에서 사용한 강의안(PDF)과 실습 노트북, 데이터를 정리했습니다. 데이터 분석을 공부하는 대학생이나 취업준비생도 혼자 따라 할 수 있도록 모든 코드 셀에 무엇을 하는 코드인지 설명하는 주석을 달아두었습니다.

## 이런 분께 권합니다

- 파이썬 기초 문법(자료형, 반복문, 함수)은 알지만, 실제 데이터를 다뤄본 경험이 적은 분
- 웹 페이지나 Open API에서 데이터를 직접 수집해보고 싶은 분
- pandas로 데이터를 정리하고 가공하는 방법을 체계적으로 익히고 싶은 분
- 상품 리뷰 같은 한글 텍스트를 분석에 쓸 수 있는 형태로 바꾸는 방법이 궁금한 분

## 강의 구성

강의안 [SDS Python Data Preprocessing.pdf](note/SDS%20Python%20Data%20Preprocessing.pdf)(218쪽)를 함께 보면서 노트북을 번호 순서대로 학습하는 것을 권장합니다. 크게 **데이터 수집(01~06)** 과 **데이터 전처리(07~09)** 두 부분으로 나뉩니다.

### Part 1. 데이터 수집

| 번호 | 노트북 | 주요 내용 |
|:---:|:---|:---|
| 01 | [네이버 금융: 현재 주가 수집](code/01_Naver_Stock_Price.ipynb) | HTTP 요청과 응답, BeautifulSoup으로 HTML 처리, 함수로 여러 종목 주가 수집 |
| 02 | [네이버 금융: 시가총액 상위 50위](code/02_Naver_Market_Capitalization_50.ipynb) | 표 형태 웹 페이지에서 종목명과 현재가 수집 |
| 03 | [네이버 금융: 주요 시장지표](code/03_Naver_Market_Index.ipynb) | 환율·유가·금시세 등 시장지표 수집, 기존 클래스를 상속해 메서드 추가 |
| 04 | [네이버 금융: 증권 주요뉴스](code/04_Naver_Stock_News.ipynb) | 쿼리 파라미터를 이용한 요청, 뉴스 정보를 데이터프레임으로 정리 |
| 05 | [공공데이터포털: 아파트 실거래가](code/05_DataGoKr_APT_Price.ipynb) | Open API 인증키 관리(`.env`), XML 응답 처리, 데이터프레임 생성 |
| 06 | [Selenium 활용법](code/06_Selenium_Basic.ipynb) | 웹 브라우저 자동 제어(클릭, 검색어 입력, 스크롤, 대기, iframe), 블로그 본문 수집 |

### Part 2. 데이터 전처리

| 번호 | 노트북 | 주요 내용 |
|:---:|:---|:---|
| 07 | [데이터 입출력](code/07_Data_Input_Output.ipynb) | 작업 경로 관리, xlsx·csv·tsv·json·parquet 파일 읽기와 저장 |
| 08 | [정형 데이터 전처리](code/08_Data_Preprocessing.ipynb) | 행·열 선택, 열 삭제와 이름 변경, 파생변수, 구간화, 자료형 변환, 날짜시간형 처리, 결측값 처리 |
| 09 | [텍스트 전처리](code/09_Text_Preprocessing.ipynb) | 정규 표현식, 한글 맞춤법 교정, Kiwi 형태소 분석, 불용어와 사용자 사전, 바이그램, 문서-단어 행렬, 코사인 거리로 유사 문서 찾기 |

## 폴더 구조

```
python-data-prep/
├── code/                     # 실습 노트북
│   ├── 01 ~ 09_*.ipynb
│   └── ko_spelling_et5.py    # 한글 맞춤법 교정 모듈 (09번 노트북에서 사용)
├── data/                     # 실습 데이터
│   ├── iris.*                                # 07번: 파일 형식별 입출력 실습
│   ├── APT_Price_Seoul_Merged_2021~2025.*    # 08번: 서울 아파트 매매 실거래가 (2021~2025년)
│   └── Galaxy_Book_Review_20250131*.xlsx     # 09번: 노트북 상품 리뷰 텍스트 (원본, 맞춤법 교정본)
└── note/                     # 강의안
    └── SDS Python Data Preprocessing.pdf
```

07~09번 노트북은 `code` 폴더에서 실행한다고 가정하고, `os.chdir(path='../data')`로 `data` 폴더에 접근합니다. 저장소를 내려받은 폴더 구조를 그대로 유지해주세요.

## 실습 환경 준비

강의는 **Python 3.12**와 Jupyter Notebook(VS Code 또는 JupyterLab) 환경에서 진행했습니다.

### 1. 저장소 내려받기

```bash
git clone https://github.com/HelloDataScience/python-data-prep.git
```

Git이 익숙하지 않다면 이 페이지 위쪽의 **Code → Download ZIP** 버튼으로 내려받아 압축을 풀어도 됩니다.

### 2. 라이브러리 설치

가상환경을 만든 다음, 아래 라이브러리를 설치합니다.

```bash
pip install jupyter requests beautifulsoup4 pandas openpyxl pyarrow python-dotenv xmltodict selenium pyautogui
```

09번 텍스트 전처리 노트북에서 사용하는 라이브러리는 버전 호환 문제가 있어 따로 설치합니다.

```bash
pip install "numpy<2.4" "transformers<4.40" torch protobuf sentencepiece kiwipiepy nltk scikit-learn tqdm
```

## 실습 전 확인할 점

- **웹 페이지 구조 변경**: 01~04번과 06번은 네이버 페이지에서 데이터를 수집합니다. 사이트 구조가 바뀌면 HTML 태그나 CSS 선택자를 수정해야 코드가 정상 동작합니다. 이것도 실전 크롤링에서 꼭 겪는 과정이니, 개발자 도구로 바뀐 구조를 직접 찾아보는 연습으로 활용해보세요.
- **공공데이터포털 인증키**: 05번을 실습하려면 [공공데이터포털](https://www.data.go.kr)에 회원가입하고 '국토교통부 아파트 매매 실거래가 자료' API 활용 신청을 해서 인증키를 받아야 합니다. 인증키는 노트북 안내에 따라 `.env` 파일에 저장하며, `.env` 파일은 깃허브 등에 올리지 않도록 주의합니다.
- **크롬 브라우저**: 06번은 크롬 브라우저가 설치되어 있어야 합니다. 최신 Selenium은 크롬 드라이버를 자동으로 내려받으므로 따로 설치하지 않아도 됩니다. 자동 설치가 안 되는 환경이라면 노트북의 [부록 1]을 참고하세요.
- **맞춤법 교정 모델**: 09번의 `ko_spelling_et5.py`는 처음 실행할 때 Hugging Face에서 T5 기반 맞춤법 교정 모델(`j5ng/et5-typos-corrector`)을 `다운로드` 폴더에 내려받습니다. 리뷰 전체를 교정하려면 시간이 오래 걸리므로, 노트북에서는 미리 교정해둔 `Galaxy_Book_Review_20250131_Corrected.xlsx` 파일을 불러와 다음 단계를 진행합니다.

## 라이선스

이 저장소의 소스 코드와 예제 노트북은 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

강의안(PDF)의 저작권은 HelloDataScience에 있으며, 별도 허락 없이 재배포하거나 상업적으로 이용할 수 없습니다.
