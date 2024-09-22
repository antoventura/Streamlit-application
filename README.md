# Rome house prices dashboard

This repository contains Rome houses prices distribution among zones ("rioni"). It is a Streamlit web application that is packaged and run using Docker for easy deployment.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the App](#running-the-app)
  - [Stopping the App](#stopping-the-app)
- [Docker Details](#docker-details)
- [License](#license)

## Requirements

- [Docker](https://docs.docker.com/get-docker/) installed on your machine.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/antoventura/Streamlit-application
    cd your-repo-name
    ```

2. Build the Docker image:
    ```bash
    docker build -t map_viz .
    ```

## Usage

### Running the App

1. Run the Streamlit application using Docker:
    ```bash
    docker run -p 8501:8501 map_viz
    ```

2. Open your web browser and go to:
    ```
    http://localhost:8501
    ```

### Stopping the App

To stop the application, press `Ctrl + C` in the terminal where the app is running or stop the Docker container using the following command:

```bash
docker stop $(docker ps -q --filter ancestor=map_viz)
 ```

## License

This project is licensed under the MIT License 

