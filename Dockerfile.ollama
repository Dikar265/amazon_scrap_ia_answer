FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y curl nginx && rm -rf /var/lib/apt/lists/*

COPY ollama-entrypoint.sh /ollama-entrypoint.sh
COPY ollama-nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /ollama-entrypoint.sh

ENTRYPOINT ["/ollama-entrypoint.sh"]