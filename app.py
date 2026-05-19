from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="图书管理系统")

# 用字典模拟数据库
books_db = {}
current_id = 1

class Book(BaseModel):
    title: str
    author: str
    isbn: str
    price: float

class BookResponse(Book):
    id: int

@app.get("/books", response_model=List[BookResponse])
def get_books(author: Optional[str] = None):
    """获取所有图书，可按作者筛选"""
    result = list(books_db.values())
    if author:
        result = [b for b in result if b["author"] == author]
    return result

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    """获取单本图书"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="图书不存在")
    return books_db[book_id]

@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: Book):
    """新增图书"""
    global current_id
    book_data = book.model_dump()
    book_data["id"] = current_id
    books_db[current_id] = book_data
    current_id += 1
    return book_data

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: Book):
    """更新图书"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="图书不存在")
    book_data = book.model_dump()
    book_data["id"] = book_id
    books_db[book_id] = book_data
    return book_data

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    """删除图书"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="图书不存在")
    del books_db[book_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)