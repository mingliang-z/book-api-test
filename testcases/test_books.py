import pytest
import allure
from api.book_api import BookAPI
from data.data_loader import load_test_data


@allure.feature("图书管理")
class TestCreateBook:
    """新增图书测试"""

    def setup_class(self):
        self.api = BookAPI()

    test_data = load_test_data("test_data.json")
    success_cases = test_data["create_book_success"]

    @allure.story("正向用例")
    @allure.title("新增图书 - {book[title]}")
    @pytest.mark.parametrize("book", success_cases)
    def test_create_book_success(self, book):
        """数据驱动的正向用例"""
        with allure.step("发送新增图书请求"):
            response = self.api.create_book(
                title=book["title"],
                author=book["author"],
                isbn=book["isbn"],
                price=book["price"]
            )

        with allure.step("验证状态码为 201"):
            assert response.status_code == 201, \
                f"期望状态码 201，实际 {response.status_code}"

        with allure.step("验证返回数据正确"):
            data = response.json()
            assert data["title"] == book["title"]
            assert data["author"] == book["author"]
            assert data["isbn"] == book["isbn"]
            assert data["price"] == book["price"]
            assert "id" in data

        with allure.step("验证数据确实被创建"):
            book_id = data["id"]
            response_get = self.api.get_book_by_id(book_id)
            assert response_get.status_code == 200

    @allure.story("异常用例")
    @allure.title("缺少必填字段 title")
    def test_create_book_missing_title(self):
        with allure.step("发送缺少 title 的请求"):
            response = self.api.post("/books", json={
                "author": "Glenford J. Myers",
                "isbn": "9787111181919",
                "price": 59.9
            })

        with allure.step("验证返回 422"):
            assert response.status_code == 422

        with allure.step("验证错误详情"):
            errors = response.json()["detail"]
            error_fields = [e["loc"] for e in errors]
            assert ["body", "title"] in error_fields

    @allure.story("异常用例")
    @allure.title("查询不存在的图书")
    def test_get_book_not_found(self):
        with allure.step("查询不存在的 ID"):
            response = self.api.get_book_by_id(999999)

        with allure.step("验证返回 404"):
            assert response.status_code == 404

        with allure.step("验证错误信息"):
            assert "不存在" in response.json()["detail"]