FROM python:3.9-slim
WORKDIR /app
COPY ./toolkit/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./toolkit ./
EXPOSE 5000
CMD ["python", "toolkit-service.py"]