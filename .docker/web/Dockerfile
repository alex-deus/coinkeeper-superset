FROM python:3.11.5-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV WORK_DIR="/application/src"
ENV USER=coinkeeper
ENV GROUP=coinkeeper

EXPOSE 8000

WORKDIR ${WORK_DIR}

RUN addgroup --system ${GROUP} &&\
    adduser --system --home ${WORK_DIR}/../user --ingroup ${GROUP} ${USER} --shell /bin/bash &&\
    chown -R ${USER}:${GROUP} ${WORK_DIR}/..

RUN pip install --no-cache-dir poetry &&\
    poetry config virtualenvs.create false
ADD poetry.lock .
ADD pyproject.toml .
RUN poetry install --no-interaction --no-ansi --without dev

ADD . ${WORK_DIR}
RUN chown -R ${USER}:${GROUP} ${WORK_DIR}
USER ${USER}

ENTRYPOINT ["/application/src/docker-entrypoint.sh"]
