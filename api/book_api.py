import requests
import json
import logging
from config.config import config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BaseAPI:
    """API 基类，封装通用请求方法"""

    def __init__(self):
        self.base_url = config.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
        self.timeout = config.TIMEOUT

    def _log_request(self, method, url, **kwargs):
        """记录请求信息"""
        logger.info(f"请求: {method} {url}")
        if 'json' in kwargs:
            logger.info(f"请求体: {json.dumps(kwargs['json'], ensure_ascii=False)}")

    def _log_response(self, response):
        """记录响应信息"""
        logger.info(f"响应: {response.status_code}")
        try:
            logger.info(f"响应体: {json.dumps(response.json(), ensure_ascii=False)}")
        except:
            logger.info(f"响应体: {response.text}")

    def get(self, path, **kwargs):
        """GET 请求"""
        url = f"{self.base_url}{path}"
        self._log_request("GET", url, **kwargs)
        response = self.session.get(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    def post(self, path, **kwargs):
        """POST 请求"""
        url = f"{self.base_url}{path}"
        self._log_request("POST", url, **kwargs)
        response = self.session.post(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    def put(self, path, **kwargs):
        """PUT 请求"""
        url = f"{self.base_url}{path}"
        self._log_request("PUT", url, **kwargs)
        response = self.session.put(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response

    def delete(self, path, **kwargs):
        """DELETE 请求"""
        url = f"{self.base_url}{path}"
        self._log_request("DELETE", url, **kwargs)
        response = self.session.delete(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response


class BookAPI(BaseAPI):
    """图书管理接口封装"""

    def create_book(self, title, author, isbn, price):
        """新增图书"""
        return self.post("/books", json={
            "title": title,
            "author": author,
            "isbn": isbn,
            "price": price
        })

    def get_all_books(self, author=None):
        """获取所有图书，可按作者筛选"""
        params = {}
        if author:
            params["author"] = author
        return self.get("/books", params=params)

    def get_book_by_id(self, book_id):
        """根据ID获取图书"""
        return self.get(f"/books/{book_id}")

    def update_book(self, book_id, title, author, isbn, price):
        """更新图书"""
        return self.put(f"/books/{book_id}", json={
            "title": title,
            "author": author,
            "isbn": isbn,
            "price": price
        })

    def delete_book(self, book_id):
        """删除图书"""
        return self.delete(f"/books/{book_id}")