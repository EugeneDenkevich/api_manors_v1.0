FROM python:3.11.3-slim
ARG group

# For viewing the application's code execution in a real time
ENV PYTHONDONTWRITEBYTECODE 1
# For not creating the .pyc files
ENV PYTHONUNBUFFERED 1

# Copy project's dependencies
WORKDIR /app
COPY ./poetry.lock ./pyproject.toml /app/

# Instal project's dependencies
RUN python -m pip install --upgrade pip && \ 
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction $group

# Copy all project's files
COPY ./entrypoint.sh .
COPY ./src .

CMD [ "./entrypoint.sh" ]
