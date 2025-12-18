## Chuẩn bị môi trường

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -U pip
pip install -r requirement.txt
```

## Cấu hình `.env`

Tạo file `.env` từ mẫu và cập nhật thông tin kết nối, secret cho phù hợp:

```bash
cp .env.example .env
```

Các biến quan trọng:

- `APP_NAME`: tên ứng dụng.
- `DEBUG`: bật/tắt log debug.
- `DATABASE_URL`: chuỗi kết nối MySQL dạng `mysql+aiomysql://user:password@host:port/database`.
- `JWT_SECRET`: secret ký JWT.
- `JWT_EXPIRE_MINUTES`: thời gian hết hạn của JWT (phút).

## Chạy ứng dụng

```bash
uvicorn app.Program:app --reload --host 0.0.0.0 --port 8000
```

Hoặc sử dụng Docker Compose để chạy kèm MySQL:

```bash
docker-compose up --build
```
