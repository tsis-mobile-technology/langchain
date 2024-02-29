"""
## 스크래핑 코드 작성

- 필요한 라이브러리 임포트
- 위키백과의 '강아지 품종 목록' 페이지 선택
- 잘 구조화된 HTML, 다양한 데이터 필드, 이미지 포함
- User-Agent를 사용하여 브라우저로 가장
- requests를 통해 HTML 페이지 다운로드 및 유효성 검사
- web site 접속 차단 방지 코드 추가(요청 속도 졸, 사용자 에이전트 및 프록시 회전 등)
- web site의 속도 제한이 있는 경우 요청 자동 조절 코드 추가
- BeautifulSoup으로 HTML 파싱
- CSS 선택자로 데이터 추출
- 이미지 다운로드 및 저장

copilot으로 작성한 코드 
"""
import requests
from bs4 import BeautifulSoup
import os

def download_images_from_url(url, folder_path):
    """
    Downloads images from a given URL and saves them in the specified folder path.

    Args:
        url (str): The URL of the web page containing the images.
        folder_path (str): The path of the folder where the images will be saved.

    Returns:
        None
    """
    # User-Agent 설정
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 웹 페이지 다운로드
    response = requests.get(url, headers=headers)

    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 유효성 검사
    if response.status_code == 200:
        # HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        # 데이터 추출
        # 이미지 태그 선택
        images = soup.find_all('img')

        # 이미지 다운로드 및 저장
        for image in images:
            image_url = url + image['src']
            image_response = requests.get(image_url)
            image_file_name = image_url.split('/')[-1].split('?')[0]  # Remove query parameters from image file name
            with open(folder_path + '/' + image_file_name, 'wb') as f:
                f.write(image_response.content)
    else:
        print('페이지를 다운로드할 수 없습니다.')

# 이미지 다운로드
download_images_from_url('https://www.google.com/', 'images')