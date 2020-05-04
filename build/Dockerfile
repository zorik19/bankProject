FROM python:3.8.2-alpine3.10

ARG rsakey
ARG isdev
ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

ADD ./source/requirements.txt /app/source/requirements.txt
WORKDIR /app
RUN apk update && \
  apk --no-cache add --virtual .build-deps gcc build-base musl-dev make git openssh-client && \
  apk --no-cache add libstdc++ postgresql-dev postgresql-libs postgresql-contrib libpq && \
  mkdir -p ~/.ssh && \
  echo "${rsakey}" > ~/.ssh/id_rsa && \
  chmod og-r ~/.ssh/id_rsa && \
  echo -e "StrictHostKeyChecking no" > ~/.ssh/config && \
  pip install --cache-dir /root/.cache/pip -r ./source/requirements.txt && \
  apk del .build-deps && \
  rm -r ~/.ssh

ADD . /app

RUN chmod +x /app/build/run.sh
RUN chmod +x /app/build/run_test.sh

CMD ["python", "-m", "source.app"]