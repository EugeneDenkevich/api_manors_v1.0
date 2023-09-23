FROM python:3.11.3-slim
ARG group

# For viewing the application's code execution in a real time
ENV PYTHONDONTWRITEBYTECODE 1
# For not creating the .pyc files
ENV PYTHONUNBUFFERED 1

# Copy project's dependencies
WORKDIR /app

# Install project's dependencies (pip)
COPY ./requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools wheel
RUN pip3 install -r requirements.txt

# # Instal project's dependencies (poetry)
# COPY ./poetry.lock ./pyproject.toml /app/
# RUN python -m pip install --upgrade pip && \ 
#     pip install poetry && \
#     poetry config virtualenvs.create false && \
#     poetry install --no-root --no-interaction $group

# Copy all project's files
COPY ./entrypoint.sh .
COPY ./src .

CMD [ "./entrypoint.sh" ]
