FROM python:3.10
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN python -m pip install --upgrade pip
RUN pip install poetry

RUN mkdir /input_manager
WORKDIR /input_manager
COPY app.py /input_manager
COPY pyproject.toml /input_manager

RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python", "app.py"]