FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD sh -c "python db/load_data.py && streamlit run app/app.py --server.port=8501 --server.address=0.0.0.0"
