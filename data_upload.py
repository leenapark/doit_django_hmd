import os
import django
import csv
import sys


# 일반 파이썬앱(스크립트)에서 django ORM을 사용하려면 다음의 설정 필요
# django 환경설정 파일 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doit_django_prj.settings")
# django settings 메모리 로딩 적용
django.setup()

# Foods class 와 연결된 테이블에 data를 ORM으로 uploading 하기 위해 import 함
from food_sales.models import Foods

# csv 파일 위치를 변수에 저장해줌
CSV_PATH='./datas/food_sales.csv'

with open(CSV_PATH, 'r',  encoding='utf-8') as file:
    data_rows = csv.reader(file, skipinitialspace=True)
    # header 제외 : 제외할 행 만큼 next를 해줘야함
    next(data_rows, None)

    # 공백라인 제거
    # 표현 방식 1
    data_rows = list(data_rows)
    # print("전 ", data_rows)
    data_rows = list(filter(None, data_rows)) # 공백 라인 제거할 때 filter 사용을 위해서는 list 형변환을 먼저 해줘야함
    print("후 ", data_rows)
    # 표현 방식 2
    # data_rows = filter(None, list(data_rows))


    for row in data_rows:
        # print(row[0])
        if row[0] != None or row[0] != "":
            # data를 바로 insert 하는 방식
            # 중복 데이터 허용
            # Foods.objects.create(
            #     cook_name=row[0],
            #     count=row[1],
            #     unit_price=row[2]
            #     )


            # DB 중복 data 확인
            Foods.objects.update_or_create(
              # DB 중복 값이 있을 때

              # filter : 중복을 체크할 값
              # Ex. cook_name = row[0]
              # 중복 체크할 models 변수와 현재 데이터 값과 비교함 : 값이 있는지 없는지 체크하는 역할
              cook_name = row[0],

              # DB 중복 값이 없을 때
              # new value
              # 명령어 : defaults = {dir형}
              defaults = {
                "cook_name":row[0],
                "count":row[1],
                "unit_price":row[2]
              }
            )
        else:
          # 메뉴가 없을 경우는 pass
          continue