# chatbot

# How to launch
```shell
echo "TG_BOT_TOKEN=<actual_token>" >> .env
docker-compose up -d --build
```

Roadmap:

1. Build
   1. tg bot
   2. controller
   3. CI/CD
   4. Docker
   5. tests + docker healthcheck
   6. monitoring
   7. github package, tags
   8. node_exporter
2. Advancements
   1. sessions
   2. redis + postgres
   3. logs
   4. sphinx
3. Asynchronous support
   1. async
   2. kafka
4. Web chat
   1. web interface
   2. history
   3. llm + history
5. Security
   1. auth
   2. security
