FROM python:3.6.13-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirments.txt -i https://pypi.douban.com/simple

# 暴露端口
EXPOSE 5000

CMD [ "python", "app.py"]