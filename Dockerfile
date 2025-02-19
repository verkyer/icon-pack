FROM python:3.9-slim-buster

WORKDIR /app

# 复制 requirements.txt 件并安装 Python 依赖
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# 复制应用代码、模板和静态文件
COPY app.py .
COPY template.html .
COPY static ./static

# 创建空 images 目录
RUN mkdir -p images  # -p 是递归创建目录（确保可用性）

# 声明构建参数
ARG LOGO_IMG=favicon.ico
ARG SITE_NAME=xg-icons
ARG COPYRIGHT="Created by <a href="https://github.com/verkyer/icon-pack" target="_blank" rel="noopener noreferrer">@icon-pack</a>"

# 设置环境变量
ENV LOGO_IMG=$LOGO_IMG
ENV SITE_NAME=$SITE_NAME
ENV COPYRIGHT=$COPYRIGHT

EXPOSE 5000

CMD ["python", "app.py"]
