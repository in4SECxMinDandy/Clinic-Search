.PHONY: help up down logs ps restart clean test lint migrate seed init-network

# Colors
GREEN  := \033[0;32m
YELLOW := \033[0;33m
BLUE   := \033[0;34m
NC     := \033[0m

# Default target
help:
	@echo "$(BLUE)╔═══════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║         Clinic Home Visit System - Development CLI       ║$(NC)"
	@echo "$(BLUE)╚═══════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Docker Commands:$(NC)"
	@echo "  make up              $(YELLOW)Start all services with Docker Compose$(NC)"
	@echo "  make down            $(YELLOW)Stop all services$(NC)"
	@echo "  make restart         $(YELLOW)Restart all services$(NC)"
	@echo "  make logs            $(YELLOW)View logs (Ctrl+C to exit)$(NC)"
	@echo "  make ps              $(YELLOW)Show running containers status$(NC)"
	@echo "  make clean           $(YELLOW)Remove all containers, volumes, and images$(NC)"
	@echo ""
	@echo "$(GREEN)Service Commands:$(NC)"
	@echo "  make auth-up         $(YELLOW)Start only auth-service$(NC)"
	@echo "  make clinic-up       $(YELLOW)Start only clinic-service$(NC)"
	@echo "  make booking-up      $(YELLOW)Start only booking-service$(NC)"
	@echo "  make gateway-up      $(YELLOW)Start only api-gateway$(NC)"
	@echo ""
	@echo "$(GREEN)Database Commands:$(NC)"
	@echo "  make migrate         $(YELLOW)Run all database migrations$(NC)"
	@echo "  make migrate-auth    $(YELLOW)Run auth-service migrations$(NC)"
	@echo "  make migrate-clinic  $(YELLOW)Run clinic-service migrations$(NC)"
	@echo "  make migrate-booking $(YELLOW)Run booking-service migrations$(NC)"
	@echo "  make migrate-review  $(YELLOW)Run review-service migrations$(NC)"
	@echo "  make seed            $(YELLOW)Seed database with sample data$(NC)"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make test            $(YELLOW)Run all tests$(NC)"
	@echo "  make lint            $(YELLOW)Run linters$(NC)"
	@echo "  make format          $(YELLOW)Format code with black/isort$(NC)"
	@echo "  make deps            $(YELLOW)Install/update dependencies$(NC)"
	@echo ""
	@echo "$(GREEN)Frontend:$(NC)"
	@echo "  make frontend-up     $(YELLOW)Start Vue.js frontend (dev server)$(NC)"
	@echo "  make frontend-build   $(YELLOW)Build frontend for production$(NC)"
	@echo ""
	@echo "$(GREEN)Observability:$(NC)"
	@echo "  make prometheus      $(YELLOW)Open Prometheus dashboard$(NC)"
	@echo "  make grafana         $(YELLOW)Open Grafana dashboard$(NC)"
	@echo "  make swagger         $(YELLOW)Open API documentation$(NC)"
	@echo ""

# Docker Compose commands
up:
	docker-compose up -d --build
	@echo "$(GREEN)All services started!$(NC)"
	@echo "  Gateway:    http://localhost:8000"
	@echo "  Swagger:    http://localhost:8000/docs"
	@echo "  Grafana:    http://localhost:3001"
	@echo "  Prometheus:  http://localhost:9090"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

ps:
	docker-compose ps

clean:
	docker-compose down -v --remove-orphans
	@echo "$(GREEN)Cleaned up!$(NC)"

# Individual service up (for development)
auth-up:
	cd services/auth-service && uvicorn main:app --reload --port 8003

clinic-up:
	cd services/clinic-service && uvicorn main:app --reload --port 8001

booking-up:
	cd services/booking-service && uvicorn main:app --reload --port 8002

gateway-up:
	cd services/api-gateway && uvicorn main:app --reload --port 8000

# Database migrations
migrate:
	@echo "$(YELLOW)Running migrations...$(NC)"
	cd services/auth-service && alembic upgrade head
	cd services/clinic-service && alembic upgrade head
	cd services/booking-service && alembic upgrade head
	cd services/review-service && alembic upgrade head
	cd services/notification-service && alembic upgrade head
	@echo "$(GREEN)All migrations completed!$(NC)"

migrate-auth:
	cd services/auth-service && alembic upgrade head

migrate-clinic:
	cd services/clinic-service && alembic upgrade head

migrate-booking:
	cd services/booking-service && alembic upgrade head

migrate-review:
	cd services/review-service && alembic upgrade head

seed:
	cd services/auth-service && python -c "from scripts.seed import seed_data; import asyncio; asyncio.run(seed_data())"

# Testing
test:
	pytest -v --cov=services --cov-report=html

test-auth:
	cd services/auth-service && pytest -v

test-clinic:
	cd services/clinic-service && pytest -v

test-booking:
	cd services/booking-service && pytest -v

# Linting and formatting
lint:
	ruff check services/
	isort services/ --check-only --diff
	black --check services/

format:
	ruff check services/ --fix
	isort services/
	black services/

deps:
	pip install -r requirements.txt

# Frontend
frontend-up:
	cd frontend && npm install && npm run dev

frontend-build:
	cd frontend && npm run build

# Observability
prometheus:
	open http://localhost:9090

grafana:
	open http://localhost:3001

swagger:
	open http://localhost:8000/docs

# Docker exec shortcuts
exec-auth:
	docker-compose exec auth-service /bin/sh

exec-clinic:
	docker-compose exec clinic-service /bin/sh

exec-postgres:
	docker-compose exec postgres psql -U postgres -d postgres

exec-redis:
	docker-compose exec redis redis-cli

# Build only
build:
	docker-compose build

# Health check
health:
	@echo "$(YELLOW)Checking services health...$(NC)"
	@curl -s http://localhost:8000/health || echo "Gateway: DOWN"
	@curl -s http://localhost:8003/health || echo "Auth: DOWN"
	@curl -s http://localhost:8001/health || echo "Clinic: DOWN"
	@curl -s http://localhost:8002/health || echo "Booking: DOWN"
	@curl -s http://localhost:8004/health || echo "Review: DOWN"
	@curl -s http://localhost:8005/health || echo "Notification: DOWN"
	@curl -s http://localhost:8006/health || echo "Data Collector: DOWN"
