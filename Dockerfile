FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/modelcontextprotocol/python-sdk.git

COPY . .

EXPOSE 8000

CMD ["python", "src/server.py"]