# litestar-sse-cleanup-issue

https://github.com/litestar-org/litestar/issues/

1. Clone this repo: `git clone https://github.com/vrslev/litestar-sse-cleanup-issue && cd litestar-sse-cleanup-issue`
1. Start Redis server: `docker compose up`
1. Run the app: `uv run litestar --app hello:app run`
1. Make a request to the app: `curl http://localhost:8000/sse`—and cancel it with Ctrl+C.
