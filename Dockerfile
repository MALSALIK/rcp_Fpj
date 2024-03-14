FROM python

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .


RUN chmod +x run.sh


CMD ["./run.sh"]
