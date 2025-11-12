FROM --platform=linux/amd64 python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential wget && \
    rm -rf /var/lib/apt/lists/*

# Install SPIN model checker
RUN wget http://spinroot.com/spin/Src/spin647.tar.gz && \
    tar -xzf spin647.tar.gz && \
    cd Src6.4.7 && \
    make && \
    cp spin /usr/local/bin/ && \
    cd .. && \
    rm -rf Src6.4.7 spin647.tar.gz

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
COPY . /app

ENV OUTPUT_DIR=/app/spin_output
RUN mkdir -p ${OUTPUT_DIR}

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

