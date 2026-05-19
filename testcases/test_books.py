from http.client import responses

import pytest

from api.book_api import BookAPI
from data.data_loader import load_test_data


class TestCreateBook:
    """新增图书测试"""
    def setup_class(self):
        self.api = BookAPI()


    test_data = load_test_data("test_data.json")
    success_cases = test_data["create_book_success"]

    @pytest.mark.parametrize("book", success_cases)
    def test_create_book_success(self,book):
        """正向用例：正常新增一本图书"""
        response = self.api.create_book(
            title = book["title"],
            author = book["author"],
            isbn = book["isbn"],
            price = book["price"]
        )
        assert response.status_code == 201, f"期望状态码201，实际{response.status_code}"
        data = response.json()
        assert data["title"] == book["title"]
        assert data["author"] == book["author"]
        assert data["isbn"] == book["isbn"]
        assert data["price"] == book["price"]
        assert "id" in data, "响应中应包含id字段"

        book_id = data["id"]
        response_get = self.api.get_book_by_id(book_id)
        assert response_get.status_code == 200
        assert response_get.json()["title"] == book["title"]

    def test_create_book_missing_title(self):
        response = self.api.post("/books", json={
            # title="《Python 语言程序设计》",
            "author" : "Glenford J. Myers",
            "isbn" : "9787111181919",
            "price" : 59.9
        })
        print( f"状态码：{response.status_code}")
        print(  f"状态码：{response.json()}")

        assert response.status_code == 422, f"期望状态码422，实际{response.status_code}"

        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == "missing"
        assert error_detail["loc"] == ["body", "title"]
        assert "Field required" in error_detail["msg"]




    def test_create_book_invalid_price(self):
        response = self.api.create_book(
            title="《Python 语言程序设计》",
            author="Glenford J. Myers",
            isbn="9787111181919",
            price=-59.9
        )
        print( f"状态码：{response.status_code}")
        print(  f"状态码：{response.json()}")
        assert response.status_code == 201, f"期望状态码201，实际{response.status_code}"
        data = response.json()
        assert data["price"] == -59.9, f"期望价格为：-59.9，实际价格{data['price']}"


    def test_create_book_error_price(self):
        response = self.api.post("/books", json={
            "price": -10.0
        })
        print(f"状态码：{response.status_code}")
        print(f"状态码：{response.json()}")
        assert response.status_code == 422, f"期望状态码422，实际{response.status_code}"
        error_detail = response.json()["detail"]
        assert len(error_detail) == 3, f"期望3个错误，实际错误{len(error_detail)}个"

    def test_get_book_not_found(self):
        response = self.api.get_book_by_id(999999)
        print(f"状态码：{response.status_code}")
        print(f"状态码：{response.json()}")
        assert response.status_code == 404, f"期望状态码404，实际{response.status_code}"