import requests
import json
import logging
import allure
from config.config import config

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
        logger.info(f"请求: {method} {url}")
        if 'json' in kwargs:
            logger.info(f"请求体: {json.dumps(kwargs['json'], ensure_ascii=False)}")

    def _log_response(self, response):
        logger.info(f"响应: {response.status_code}")
        try:
            logger.info(f"响应体: {json.dumps(response.json(), ensure_ascii=False)}")
        except:
            logger.info(f"响应体: {response.text}")

    def _attach_to_allure(self, method, url, request_body, response):
        """将请求和响应附加到 Allure 报告"""
        # 附加请求信息
        request_info = f"请求方式: {method}\n请求路径: {url}"
        if request_body:
            request_info += f"\n请求体: {json.dumps(request_body, ensure_ascii=False, indent=2)}"
        allure.attach(request_info, "请求信息", allure.attachment_type.TEXT)

        # 附加响应信息
        response_info = f"状态码: {response.status_code}"
        try:
            response_info += f"\n响应体: {json.dumps(response.json(), ensure_ascii=False, indent=2)}"
        except:
            response_info += f"\n响应体: {response.text}"
        allure.attach(response_info, "响应信息", allure.attachment_type.TEXT)

    def get(self, path, **kwargs):
        url = f"{self.base_url}{path}"
        self._log_request("GET", url, **kwargs)
        response = self.session.get(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        self._attach_to_allure("GET", url, kwargs.get("params"), response)
        return response

    def post(self, path, **kwargs):
        url = f"{self.base_url}{path}"
        self._log_request("POST", url, **kwargs)
        response = self.session.post(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        self._attach_to_allure("POST", url, kwargs.get("json"), response)
        return response

    def put(self, path, **kwargs):
        url = f"{self.base_url}{path}"
        self._log_request("PUT", url, **kwargs)
        response = self.session.put(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        self._attach_to_allure("PUT", url, kwargs.get("json"), response)
        return response

    def delete(self, path, **kwargs):
        url = f"{self.base_url}{path}"
        self._log_request("DELETE", url, **kwargs)
        response = self.session.delete(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        self._attach_to_allure("DELETE", url, None, response)
        return response


class BookAPI(BaseAPI):
    """图书管理接口封装"""

    def create_book(self, title, author, isbn, price):
        return self.post("/books", json={
            "title": title,
            "author": author,
            "isbn": isbn,
            "price": price
        })

    def get_all_books(self, author=None):
        params = {}
        if author:
            params["author"] = author
        return self.get("/books", params=params)

    def get_book_by_id(self, book_id):
        return self.get(f"/books/{book_id}")

    def update_book(self, book_id, title, author, isbn, price):
        return self.put(f"/books/{book_id}", json={
            "title": title,
            "author": author,
            "isbn": isbn,
            "price": price
        })

    def delete_book(self, book_id):
        return self.delete(f"/books/{book_id}")