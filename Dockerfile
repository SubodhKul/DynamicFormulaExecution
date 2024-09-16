FROM python:3.10
EXPOSE 5000
WORKDIR /app
RUN pip install flask
COPY . /app
RUN pip install -r requirements.txt
CMD ["python","app.py"]
