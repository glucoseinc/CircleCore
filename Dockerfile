# css/js asset builder
FROM node:alpine as builder

WORKDIR /build
COPY package.json yarn.lock ./
COPY react-title-component/ react-title-component/
RUN yarn

COPY .babelrc .eslintrc.yml postcss.config.js webpack.config.js ./
COPY circle_core/web/src/ circle_core/web/src/
RUN yarn run build


# 
FROM python:3.6-alpine3.8

# setup nanomsg
WORKDIR /app

ENV LD_LIBRARY_PATH ${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}/usr/local/lib64

# setup modules
COPY Pipfile Pipfile.lock setup.py ./
RUN apk --update add gettext libffi libxml2 libstdc++ && \
  apk --virtual .build-deps add build-base cmake curl libffi-dev libxml2-dev libxslt-dev && \
  # build nanomsg
  mkdir /build && cd /build && \
  curl -OL https://github.com/nanomsg/nanomsg/archive/1.1.5.tar.gz && \
	tar zxvf 1.1.5.tar.gz && \
  cd nanomsg-1.1.5 && \
  mkdir build && cd build && \
  cmake .. && \
  cmake --build . && \
  ctest . && \
  cmake --build . --target install && \
  rm -r /build && \
  # build python
  cd /app && \
  pip install -U pip pipenv && \
  pipenv install -v --system --deploy && \
  # cleanup
  apk del --purge .build-deps

# copy sources
COPY docker/entrypoint.sh ./
COPY docker/circle_core.ini.template ./
COPY --from=builder /build/circle_core/web/static/ ./circle_core/web/static/
COPY . /app

EXPOSE 8080
VOLUME /app/data

ENV DB_URL mysql+pymysql://root@localhost/crcr_dev
ENV HTTP_PORT 8080

ENTRYPOINT ["./entrypoint.sh"]
CMD ["run"]
