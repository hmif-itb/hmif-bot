FROM python:3.10.5-alpine3.16

ARG user=hmif

RUN apk add --no-cache tzdata
ENV TZ=Asia/Jakarta

# as root
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN addgroup --gid 1001 -S ${user} && \
    adduser -G ${user} --disabled-password --uid 1001 ${user} && \
    mkdir -p /var/log/${user} && \
    chown ${user}:${user} /var/log/${user}
USER ${user}

CMD [ "gunicorn", "app:app", "--bind=0.0.0.0" ]
