# FROM sagemath/sagemath:latest (2025/11/11)
FROM sagemath/sagemath@sha256:c7f2f4c4c5360900d22b90f33500d8ccd96edb3a1127dcd56b4f107c14315691

WORKDIR /home/sage/sage/repo

COPY . .

RUN /home/sage/sage/local/var/lib/sage/venv-python3.12.5/bin/pip install --no-cache-dir -r requirements.txt

RUN echo 'export PATH="/home/sage/sage/local/var/lib/sage/venv-python3.12.5/bin:$PATH"' >> ~/.bashrc && \
    echo 'alias python="python3.12"' >> ~/.bashrc && \
    echo 'alias python3="python3.12"' >> ~/.bashrc && \
    echo 'alias pip="pip3.12"' >> ~/.bashrc

CMD ["/bin/bash", "-l"]
