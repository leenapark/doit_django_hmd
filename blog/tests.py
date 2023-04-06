from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
class TestView(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # self.assertEqual(2, 2)
        # 1.1 포스트 목록 페이지를 가져온다
        response = self.client.get("/blog/")
        # 1.2 정상적으로 페이지가 로드된다
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지 타이틀은 'Blog'이다
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertEqual(soup.title.text, "Blog")
        # 1.4 내비게이션 바가 존재한다
        navbar = soup.nav
        # 1.5 Blog, About Me 라는 문구가 내비게이션 바 안에 있다
        self.assertIn("Blog", navbar.text)
        self.assertIn("About Me", navbar.text)

        # 게시물이 없을 경우
        # 2.1 '아직 게시물이 없습니다'
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find("div", id="main-area")
        self.assertIn("아직 게시물이 없습니다", main_area.text)

        # 게시물이 있을 경우
        # 3.1 포스트 목록 페이지 새로 고침 했을 때 포스트 타이틀이 존재
        # 3.2 '아직 게시물이 없습니다' 문구 삭제

