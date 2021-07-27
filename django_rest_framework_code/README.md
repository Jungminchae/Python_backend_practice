# Django RestAPI DEV
- Django rest_framework로 API 개발하기

## 기능 요구사항
- 질문을 데이터베이스에 저장, 수정, 삭제하는 API
- 질문의 댓글을 데이터베이스에 저장하는 API
- 질문에 달린 댓글 목록을 출력하는 API
- 키워드로 질문의 제목 또는 본문내용을 검색하는 API
- 질문 작성일 기준 각 월별 전체 질문 중에서 가장 좋아요가 많은 질문을 출력하는 API

## Language & Framework
- Language - Python 3.7
- Framework
  - Django 3.1.7
  - Django rest_framework

<br>
<br>

#### **_기능별 설명은 토글을 클릭하시면 됩니다._**

<br>

## 질문을 데이터베이스에 저장, 수정, 삭제하는 API 개발

<details>
<summary> 질문 생성 </summary>

### Create Question

- URL <br>
  api/v1/questions/
- Method <br>
  POST
- Sample Request

```code
{"title":"샘플 질문 입니다","content":"샘플 질문 입니다"}
```

- Success Response <br>
  CODE - 200 <br>
  Message - OK <br>
  Content

```code
{
    "id": 5,
    "username": {
        "username": "jmc"
    },
    "created_at": "2021-07-11T16:39:01.952780+09:00",
    "updated_at": "2021-07-11T16:39:01.952780+09:00",
    "title": "샘플 질문 입니다",
    "content": "샘플 질문 입니다"
}
```

- Error Response <br>
CODE - 401 <br>
Message - UNAUTHORIZED <br><br>
Or <br><br>
CODE - 400 <br>
Message - BAD_REQUEST
</details>
<br>
<details>
<summary>질문 수정, 삭제</summary>

### Edit, Delete Question

- URL <br>
  api/v1/questions/id/ -> question id
- Method <br>
  PUT, DELETE
- URL Params <br>
  id = Integer
- Sample Request <br>
  - PUT
    ```code
    {"title":"샘플 질문 수정"}
    ```
- Success Response <br>
  CODE - 200 <br>
  Message - OK <br>
  Content

  ```code
  {
    "id": 5,
    "username": {
        "username": "jmc"
    },
    "created_at": "2021-07-11T16:39:01.952780+09:00",
    "updated_at": "2021-07-11T17:02:37.353986+09:00",
    "title": "샘플 질문 수정",
    "content": "샘플 질문 입니다"
  }
  ```

- Error Response <br>
CODE - 403 <br>
Message - FORBIDDEN <br><br>
Or <br><br>
CODE - 400 <br>
Message - BAD_REQUEST
Or <br><br>
CODE - 404 <br>
Message - NOT_FOUND
<hr>

- DELETE
- Success Response <br>
  CODE - 200 <br>
  Message - OK <br>

- Error Response <br>
  CODE - 403 <br>
  Message - FORBIDDEN <br><br>
  Or <br><br>
  CODE - 404 <br>
  Message - NOT_FOUND

</details>
<br>
<hr>
<br>

## 질문의 댓글을 데이터베이스에 저장하는 API 개발

<details>
<summary> 댓글 저장 </summary>

### Save Comment

- URL <br>
  api/v1/comments/ <br>
- Method <br>
  POST
- Sample Request <br>

```code
{"question":1,"content":"샘플 댓글 입니다"}
```

- Success Response <br>
  CODE - 201 <br>
  Message - CREATED <br>
  Content

```code
{
    "id": 5,
    "created_at": "2021-07-11T17:22:08.926028+09:00",
    "content": "샘플 댓글 입니다",
    "question": 1,
    "username": 1
}
```

- Error Response <br>
  CODE - 401 <br>
  Message - UNAUTHORIZED <br><br>
  Or <br><br>
  CODE - 400 <br>
  Message - BAD_REQUEST

</details>

<br>
<hr>
<br>

## 질문에 달린 댓글 목록을 출력하는 API 개발

<details>
<summary> 댓글 목록 출력 </summary>

### List Comment

- URL <br>
  api/v1/comments/id/ -> question id
- Method <br>
  GET
- URL Params <br>
  id = Integer

- Success Response <br>
  CODE - 200 <br>
  Message - OK <br>
  Content

  ```code
    [
        {
            "id": 1,
            "created_at": "2021-07-10T13:17:50.174989+09:00",
            "content": "무야호~",
            "question": 4,
            "username": 1
        },
        {
            "id": 2,
            "created_at": "2021-07-10T15:02:56.549081+09:00",
            "content": "무야호호호호호호~~",
            "question": 4,
            "username": 1
        },
        {
            "id": 3,
            "created_at": "2021-07-10T15:03:11.347648+09:00",
            "content": "무야호호호호호우우우야",
            "question": 4,
            "username": 1
        }
    ]
  ```

- Error Response <br>
  CODE - 404 <br>
  Message - NOT_FOUND <br><br>

</details>

<br>
<hr>
<br>

## 키워드로 질문의 제목 또는 본문내용을 검색하는 API 개발

<details>
<summary> 질문 검색 </summary>

### Search Question

- URL <br>
  api/v1/comments/keyword/ -> 검색 키워드
- Method <br>
  GET
- URL Params <br>
  keyword = String

- Success Response <br>
  CODE - 200 <br>
  Message - OK <br>
  Content

  ```code
    [
        {
            "id": 5,
            "username": {
                "username": "jmc"
            },
            "created_at": "2021-07-11T16:39:01.952780+09:00",
            "updated_at": "2021-07-11T17:02:37.353986+09:00",
            "title": "샘플 질문 수정",
            "content": "샘플 질문 입니다"
        }
    ]
  ```

- Error Response <br>
  CODE - 404 <br>
  Message - NOT_FOUND <br><br>

</details>

<br>
<hr>
<br>

## 질문 작성일 기준 각 월별 전체 질문 중에서 가장 좋아요가 많은 질문을 출력하는 API 개발

<details>
<summary> 좋아요가 가장 많은 질문 검색 </summary>

### Search Monthly No.1 Likes Question

- URL <br>
  api/v1/questions/monthly_top/id -> question id
- Method <br>
  GET
- URL Params <br>
  id = Integer

- Success Response <br>
  CODE - 200 <br>
  Message - OK <br>
  Content

  ```code
    [
        {
            "id": 4,
            "username": {
                "username": "jmc"
            },
            "created_at": "2021-07-09T21:34:21.782063+09:00",
            "updated_at": "2021-07-09T21:43:00.838423+09:00",
            "title": "혹시?",
            "content": "설마?"
        }
    ]
  ```

- Error Response <br>
  CODE - 404 <br>
  Message - NOT_FOUND <br><br>

</details>
