FROM python:3
RUN  pip install aiosmtpd
COPY server.py client.py /
COPY server.pem server.key /
WORKDIR /
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["/server.py"]
