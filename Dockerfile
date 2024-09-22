# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies required for geospatial packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    libgdal-dev \
    libproj-dev \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set the working directory inside the container
WORKDIR /Streamlit-application

# Copy pyproject.toml and poetry.lock (for caching)
COPY pyproject.toml poetry.lock* ./

# Install dependencies without dev packages
RUN poetry install --without dev

# Copy the rest of the application code
COPY . .

# Expose port 8501 to make the app accessible
EXPOSE 8501

# Healthcheck for the Streamlit service
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Start the Streamlit app
ENTRYPOINT ["poetry", "run", "streamlit", "run", "map_viz.py", "--server.port=8501", "--server.address=0.0.0.0"]
