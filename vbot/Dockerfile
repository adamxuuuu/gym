FROM ubuntu:latestdo

# 复制 /usr/lib 和 /usr/include 到 Docker 镜像中
COPY /usr/lib /usr/lib
COPY /usr/include /usr/include

# 安装Python和相关依赖
#RUN apt-get update && apt-get install -y python3 python3-pip

# 将当前目录下的requirements.txt文件复制到容器中
#COPY requirements.txt /app/requirements.txt

# 在容器中安装Python依赖
#RUN pip3 install -r /app/requirements.txt

# 将当前目录下的Python脚本复制到容器中
#COPY chatbot.py /app/chatbot.py
#COPY config.py  /app/config.py
#COPY . /app

# 设置容器启动时的默认命令
#CMD ["python3", "/app/chatbot.py"]
