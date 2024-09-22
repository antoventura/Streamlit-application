# Dockerfile

FROM python:3.11-slim

RUN pip install poetry

WORKDIR /Streamlit-application

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/antoventura/Streamlit-application .

RUN poetry install --without dev

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "map_viz.py", "--server.port=8501", "--server.address=0.0.0.0"]