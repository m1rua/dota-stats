# DotaStats

Веб-сервис для просмотра статистики игрока в Dota 2 по Steam Account ID. Сделан для практики DevOps стека — K8s, мониторинг, кэширование.

---

## Стек

| Слой | Технологии |
|---|---|
| Backend | Python 3.11, FastAPI, asyncpg |
| База данных | PostgreSQL 15 (кэш запросов) |
| Инфра | Kubernetes (minikube), Docker |
| Мониторинг | Prometheus, Grafana |
| Данные | OpenDota API (бесплатный) |

## Функционал

- Поиск игрока по Steam Account ID
- Winrate, KDA, победы/поражения
- Переключение периода — 30 или 100 матчей
- Топ 3 героя по количеству игр с иконками
- История последних матчей
- Кэширование результатов в PostgreSQL на 1 час

## Архитектура

```
Browser → FastAPI (K8s pod) → OpenDota API
               │
          PostgreSQL (cache)

Prometheus → собирает метрики с API
Grafana    → визуализация метрик
```

4 пода в кластере: `api`, `pgsql`, `prometheus`, `grafana`

## Как запустить

```bash
git clone https://github.com/m1rua/dota-stats.git
cd dota-stats
```

Запустить кластер и собрать образ:

```bash
minikube start
eval $(minikube docker-env)
cd app && docker build -t dota-api:latest . && cd ..
```

Задеплоить в K8s:

```bash
kubectl apply -f k8s/
```

Создать таблицу кэша:

```bash
kubectl exec -it deployment/pgsql -- psql -U user -d dota -c \
"CREATE TABLE cache (account_id BIGINT PRIMARY KEY, data JSONB, cached_at TIMESTAMP DEFAULT NOW());"
```

Пробросить порты:

```bash
kubectl port-forward service/api 8000:8000        # основной сервис
kubectl port-forward service/grafana 3000:3000    # мониторинг
```

Открыть в браузере: `http://localhost:8000`

## Мониторинг

Grafana доступна на `http://localhost:3000` (admin/admin).

Data source: `http://prometheus:9090`

Метрики: количество запросов, время ответа, статус эндпоинтов.
