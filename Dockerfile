FROM python:3.11

WORKDIR /taskapi

COPY . .

RUN pip install uv
RUN uv venv

ENV PATH="/taskapi/.venv/bin:$PATH"

RUN uv pip install -r pyproject.toml
RUN uv pip install uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]





