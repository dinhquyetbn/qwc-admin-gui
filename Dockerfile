FROM sourcepole/qwc-uwsgi-base:alpine-v2023.10.26

ADD requirements.txt /srv/qwc_service/requirements.txt
# ADD qwc_services_core-1.3.28-py3-none-any.whl /srv/qwc_service/qwc_services_core-1.3.28-py3-none-any.whl
# git: Required for pip with git repos
# postgresql-dev g++ python3-dev: Required for psycopg2
RUN \
    apk add --no-cache --update --virtual runtime-deps postgresql-libs && \
    apk add --no-cache --update --virtual build-deps git postgresql-dev g++ python3-dev && \
    # Thêm các lệnh để cài đặt QGIS
    pip3 install --no-cache-dir -r /srv/qwc_service/requirements.txt && \
    apk del build-deps

ADD src /srv/qwc_service/

ENV SERVICE_MOUNTPOINT=/qwc_admin


# FROM ubuntu:22.04

# ENV TZ=Asia/Ho_Chi_Minh
# # Cài đặt các gói cần thiết
# RUN apt-get update && apt-get install -y \
#     software-properties-common \
#     wget \
#     gnupg2 tzdata \
#     && ln -fs /usr/share/zoneinfo/$TZ /etc/localtime \
#     && dpkg-reconfigure -f noninteractive tzdata \
#     && apt-get clean

# # Thêm PPA và cài đặt QGIS cùng với Python bindings
# RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable && \
#     apt-get update && \
#     apt-get install -y \
#     qgis \
#     python3-qgis \
#     libpq-dev \
#     uwsgi \
#     uwsgi-plugin-python3 \
#     && apt-get clean

# # Thêm các tệp cần thiết vào container
# ADD requirements.txt /srv/qwc_service/requirements.txt

# # Cài đặt các phụ thuộc Python
# RUN apt-get install -y python3-pip && \
#     pip3 install --no-cache-dir -r /srv/qwc_service/requirements.txt

# # Thêm mã nguồn vào container
# ADD src /srv/qwc_service/

# # Đặt biến môi trường
# ENV SERVICE_MOUNTPOINT=/qwc_admin

# # Lệnh khởi chạy container
# ENTRYPOINT ["uwsgi"]
# CMD ["--ini", "/srv/qwc_service/uwsgi.ini"]