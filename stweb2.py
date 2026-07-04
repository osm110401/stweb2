# age_app.py

import streamlit as st
import csv
import io
import matplotlib.pyplot as plt

# 한글 폰트 설정 - Windows 기준
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

st.title('인구 데이터 분석')

file = st.file_uploader('age.csv 파일 업로드', type='csv')

if file is not None:

    # =========================
    # 1. 파일 열기
    # =========================

    text = io.TextIOWrapper(file, encoding='cp949')
    data = csv.reader(text)

    header = next(data)
    data = list(data)

    # 천 단위 콤마 제거
    for row in data:
        for i in range(len(row)):
            row[i] = row[i].replace(',', '')

    st.write('첫 번째 데이터')
    st.write(data[0])

    st.write('전체 데이터 수')
    st.write(len(data))

    # =========================
    # 2. 지역 선택
    # =========================

    area_list = []

    for row in data:
        area_list.append(row[0])

    name = st.selectbox('지역이름(읍면동)을 선택하세요', area_list)

    # =========================
    # 3. 우리 동네 인구 구조
    # =========================

    st.header('우리 동네 인구 구조')

    result = []

    for row in data:
        if name in row[0]:
            for i in row[3:104]:
                result.append(int(i))
            break

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(result)
    ax.set_title(name + ' 인구 구조')
    ax.set_xlabel('나이')
    ax.set_ylabel('인구수')
    st.pyplot(fig)

    # =========================
    # 4. 남성, 여성 인구 비교
    # =========================

    st.header('남성, 여성 인구 비교')

    m = []
    f = []

    for row in data:
        if name in row[0]:
            for i in range(101):
                m.append(-int(row[i + 106]))
                f.append(int(row[i + 209]))
            break

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(range(101), m, label='남성')
    ax.barh(range(101), f, label='여성')
    ax.set_title(name + ' 남녀 인구 비교')
    ax.set_xlabel('인구수')
    ax.set_ylabel('나이')
    ax.legend()
    st.pyplot(fig)

    # =========================
    # 5. 성별 비율 파이 차트
    # =========================

    st.header('성별 인구 비율')

    male = 0
    female = 0

    for row in data:
        if name in row[0]:
            for i in range(101):
                male += int(row[i + 106])
                female += int(row[i + 209])
            break

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie([male, female],
           labels=['male', 'female'],
           autopct='%.1f%%')
    ax.set_title(name + ' 성별 인구 비율')
    st.pyplot(fig)

    # =========================
    # 6. 인구 구조가 가장 비슷한 지역 찾기
    # =========================

    st.header('인구 구조가 가장 비슷한 지역 찾기')

    result = []
    result2 = []
    result_name = ''

    for row in data:
        if name in row[0]:
            for i in row[3:104]:
                result.append(int(i))
            break

    min_value = 100000000000

    for row in data:
        total = 0

        for i in range(3, 104):
            total += (int(row[i]) - int(result[i - 3])) ** 2

        if min_value > total and name not in row[0]:
            min_value = total
            result2 = []

            for i in row[3:104]:
                result2.append(int(i))

            result_name = row[0]

    st.write('가장 비슷한 지역:', result_name)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(result, label=name)
    ax.plot(result2, label=result_name)
    ax.set_title('인구 구조 비교')
    ax.set_xlabel('나이')
    ax.set_ylabel('인구수')
    ax.legend()
    st.pyplot(fig)
    # =========================
    # 7. 가장 인구가 많은 나이 찾기
    # =========================

    st.header('가장 인구가 많은 나이')

    max_pop = 0
    max_age = 0

    for row in data:
        if name in row[0]:
            for i in range(101):
                value = int(row[i + 3])
                if value > max_pop:
                    max_pop = value
                    max_age = i
                break

    st.write(f'가장 많은 나이: {max_age}세')
    st.write(f'인구 수: {max_pop}')
else:
    st.info('age.csv 파일을 업로드하세요.')