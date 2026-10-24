# VietCite Studio tasks. Works in Git Bash on Windows and on Linux/macOS.
# uv is called as a Python module so it works even when uv is not on PATH.
UV ?= python -m uv
BACKEND = cd backend &&
FRONTEND = cd frontend &&

.PHONY: help install up down logs test test-live lint format typecheck hello smoke api web check-ui

help:
	@echo "install     install backend (uv) and frontend (npm) dependencies"
	@echo "up / down   start / stop the docker stack (wordpress :8080, api :8000, web :5173)"
	@echo "test        offline tests (mock model, no key needed)"
	@echo "test-live   tests that call real APIs (costs a little; skips missing keys)"
	@echo "lint        ruff check + format check"
	@echo "typecheck   pyright + frontend tsc"
	@echo "hello       run the hello agent on the mock model (MODE=live for DeepSeek)"
	@echo "smoke       call each real provider once"
	@echo "api / web   run the API (:8000) / the web dev server (:5173) without docker"

install: check-ui
	$(BACKEND) $(UV) sync
	$(FRONTEND) npm install

check-ui:
	node scripts/check-ui-package.mjs

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

test:
	$(BACKEND) $(UV) run pytest -q
	$(FRONTEND) npm test

test-live:
	$(BACKEND) $(UV) run pytest -m live -q

lint:
	$(BACKEND) $(UV) run ruff check .
	$(BACKEND) $(UV) run ruff format --check .

format:
	$(BACKEND) $(UV) run ruff check --fix .
	$(BACKEND) $(UV) run ruff format .

typecheck:
	$(BACKEND) $(UV) run pyright
	$(FRONTEND) npm run typecheck

MODE ?= mock
hello:
	$(BACKEND) $(UV) run geo hello --mode $(MODE)

smoke:
	$(BACKEND) $(UV) run geo smoke

api:
	$(BACKEND) $(UV) run uvicorn app.main:app --reload --port 8000

web:
	$(FRONTEND) npm run dev
