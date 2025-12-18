python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -U pip
pip install fastapi uvicorn


# nếu dự án có requirements:
pip install -r requirements.txt
# chạy server

uvicorn app.Program:app --reload --host 0.0.0.0 --port 8000
