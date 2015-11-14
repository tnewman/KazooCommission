FROM python
MAINTAINER Thomas Newman
RUN apt-get update -y \
	&& apt-get install supervisor -y \
	&& apt-get clean
RUN pip install gunicorn
RUN git clone https://github.com/tnewman/KazooCommission --depth 1
CMD ["gunicorn runserver --bind 0.0.0.0:8000"]
