FROM python
MAINTAINER Thomas Newman
RUN git clone https://github.com/tnewman/KazooCommission --depth 1
WORKDIR KazooCommission
RUN pip install -r requirements.txt && pip install gunicorn	
EXPOSE 8000
CMD gunicorn --bind 0.0.0.0:8000 --bind [::1]:8000 runserver
