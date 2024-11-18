from apify_client import ApifyClient
import pandas as pd
import json
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# apifty client 생성
client = ApifyClient("YOUR_APIFY")

# 크롤링 설정
run_input = {
    "startUrls": [{"url": "https://en.wikipedia.org/wiki/Python_(programming_language)"}],
    "useSitemaps": True,
    "crawlerType": "playwright:adaptive",
    "includeUrlGlobs": [],
    "excludeUrlGlobs": [],
    "keepUrlFragments": False,
    "ignoreCanonicalUrl": False,
    "maxCrawlDepth": 20,
    "maxCrawlPages": 9999999,
    "initialConcurrency": 0,
    "maxConcurrency": 200,
    "initialCookies": [],
    "proxyConfiguration": {"useApifyProxy": True},
    "maxSessionRotations": 10,
    "maxRequestRetries": 5,
    "requestTimeoutSecs": 60,
    "minFileDownloadSpeedKBps": 128,
    "dynamicContentWaitSecs": 10,
    "waitForSelector": "",
    "maxScrollHeightPixels": 5000,
    "keepElementsCssSelector": "",
    "removeElementsCssSelector": """nav, footer, script, style, noscript, svg, img[src^='data:'],
    [role=\"alert\"],
    [role=\"banner\"],
    [role=\"dialog\"],
    [role=\"alertdialog\"],
    [role=\"region\"][aria-label*=\"skip\" i],
    [aria-modal=\"true\"]""",
    "removeCookieWarnings": True,
    "expandIframes": True,
    "clickElementsCssSelector": "[aria-expanded=\"false\"]",
    "htmlTransformer": "readableText",
    "readableTextCharThreshold": 100,
    "aggressivePrune": False,
    "debugMode": False,
    "debugLog": False,
    "saveHtml": False,
    "saveHtmlAsFile": False,
    "saveMarkdown": True,
    "saveFiles": False,
    "saveScreenshots": False,
    "maxResults": 9999999,
    "clientSideMinChangePercentage": 15,
    "renderingTypeDetectionPercentage": 10,
}

# api 호출
run = client.actor("aYG0l9s7dbB7j3gbS").call(run_input=run_input)

# 결과 json 파일로 저장
data = [item for item in client.dataset(run["defaultDatasetId"]).iterate_items()]
with open("wikipedia_data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# 불러오기
df = pd.DataFrame(data)

# 데이터 구조 확인을 위해 컬럼 정보 출력
print(df.columns)     # 컬럼 이름 확인
print(df.head())      # 첫 몇 개의 행 확인
print(df.iloc[0])     # 첫 번째 행의 세부 내용 확인

# 데이터 전처리
all_text = " ".join(df['text'])

# 단어 카운트
word_counts = Counter(all_text.split())
print(word_counts.most_common(10))

# 워드 클라우드 생성
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off') 
plt.show()

# 키워드 추출'cuda'
filtered_sentences = [sentence for sentence in all_text.split('.') if 'cuda' in sentence.lower()]
print(filtered_sentences[:10])


