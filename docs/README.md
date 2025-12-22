[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker Compatibility](https://img.shields.io/badge/Docker-20.10%2B-0db7ed)](https://docs.docker.com)
[![Docker Compose Compatibility](https://img.shields.io/badge/Docker_Compose-2.0%2B-1ad1b9)](https://docs.docker.com/compose)
[![SageMath](https://img.shields.io/badge/SageMath-10.7-3F7E44?logo=sagemath)](https://www.sagemath.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# ![Project Banner](banner.jpg)
<div align="center">
<h2>🕸️ Geodesic Subpath Number Analysis 🕸️</h2>
</div>

_Project was developed as part of course 'Financial lab' at the 
University of Ljubljana, Faculty of Mathematics and Physics, during the 
academic year 2025/2026. The aim was to analyze structural properties in 
various classes of connected simple graphs through the lens of the
geodesic subpath number._


## 📚 Essentials
Let $`G = (V, E)`$ be connected, simple, undirected graph. 
For any two vertices (nodes) $`u, v \in V`$ the length of **shortest** path 
between them is called **graph distance**, denoted as $`d_G(u, v)`$.

- **`Path`** in $G$ is a sequence of distinct vertices $`(v_i)_{i=1}^{\ell}`$ 
such that each consecutive pair $`(v_{i-1}, v_i) \in E`$
- **`Trivial path`** is a path of length $`0`$ consisting of a single vertex
- **`Geodesic path`** between vertices $u$ and $v$ is any simple path of length 
exactly $d_G(u, v)$

Let $P \mspace{2mu} (G \mspace{2mu})$ denote the set of all geodesic paths (including trivial paths).  
The **`geodesic subpath number`** of $G$ is defined as:

$$
gpn \mspace{2mu}( G \mspace{3mu}) \mspace{2mu} = | P \mspace{5mu} ( G \mspace{3mu}) \mspace{6mu}|
$$

Simply, $`gpn(G \mspace{2mu} )`$ counts all shortest paths between
vertex pairs and includes all trivial paths.

## 📝 Findings
Report of our analysis in Slovene can be accessed here: [full report](./docs/report/geodetske_poti.pdf)

## 🛠️ Setup Guide

- 📋Pre-requisites:
    - [Docker 20.10+](https://docs.docker.com/get-docker/)
    - [Docker Compose 2.0+](https://docs.docker.com/compose/install/)

- 🔧 Environment Configuration:
    
    1. 🐳 Deploy Docker Compose Service
    ```bash
    docker compose up -d
    ```
    2. 🖥️ Shell Access to SageMath Container
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


> [!TIP]
> Jupyter notebook cells can be executed directly from an IDE such as **Visual Studio Code**:
>
> - Install the **Jupyter Notebook** extension
> - Select **`Dev Containers: Attach to Running Container`** from option menu
> - Choose **`/sagemath-dev`** container as the execution environment

- 🚀 Running Python Modules from Docker Container:
    ```bash
    sage -python <path-to-file>
    ```


## 💡 Advisors
Project was developed under the guidance of:
- Riste Škrekovski 
- Timotej Hrga

