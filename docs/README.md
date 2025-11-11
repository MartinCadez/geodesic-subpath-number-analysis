[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker Compatibility](https://img.shields.io/badge/Docker-20.10%2B-0db7ed)](https://docs.docker.com)
[![Docker Compose Compatibility](https://img.shields.io/badge/Docker_Compose-2.0%2B-1ad1b9)](https://docs.docker.com/compose)
[![SageMath](https://img.shields.io/badge/SageMath-10.7-3F7E44?logo=sagemath)](https://www.sagemath.org/)
[![Ruff](https://img.shields.io/badge/Ruff-Linter-EEAA00?logo=python&logoColor=fff)](https://github.com/astral-sh/ruff)

<!-- # ![Project Banner](banner.jpg) -->

<div align="center">
<h2>need to update</h2>
</div>

_Project was developed as part of course 'Financial lab' at the 
University of Ljubljana, Faculty of Mathematics and Physics, during the 
academic year 2025/2026. It aims to (need to update)_


## 📚 Essentials
need to update ab graph theory graphs etc.

## 🛠️ Setup Guide

- 📋Pre-requisites:
    - [Docker 20.10+](https://docs.docker.com/get-docker/)
    - [Docker Compose 2.0+](https://docs.docker.com/compose/install/)

- 🔧 Environment Configuration:
    
    1. 🐳 Deploy Docker Compose Services
    ```bash
    docker compose up -d
    ```
    2. 🖥️ Interactive Access to SageMath Container
    ```bash
    docker compose exec sagemath bash
    ```

>[!NOTE]
> The current configuration ([`docker-compose.yml`](../docker-compose.yml)) 
defines a service which deploys a container with a volume that acts as a sync
between the container directory and the host directory. Any changes made on
the host are immediately reflected inside the container, and vice versa.

> [!TIP]
> Before proceeding with any operations, ensure the Docker service is running
> and verify its status.
> 
> ```bash
> docker ps --filter "name=sagemath-dev"
> ``````

- 🚀 Run Simulation
    ```bash
    sage -python src/main.py
    ```

## 💡 Advisors
Project was developed under the guidance of:
- Riste Škrekovski 
- Timotej Hrga
