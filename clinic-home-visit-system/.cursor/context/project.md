# Project Context

## Project Name
Clinic Home Visit System

## Project Type
Python FastAPI Microservices + Vue.js 3 Frontend

## Key Features
- Clinic search with GPS distance sorting
- Appointment booking (at clinic or home visit)
- JWT authentication
- Review system
- Notification service

## Tech Stack
- Backend: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL, Redis
- Frontend: Vue.js 3, Vite, TailwindCSS, Pinia
- Infrastructure: Docker, Traefik

## Project Structure
```
services/
├── auth-service/         # Port 8003
├── clinic-service/      # Port 8001
├── booking-service/     # Port 8002
├── review-service/      # Port 8004
├── notification-service/ # Port 8005
├── data-collector/      # Port 8006
└── api-gateway/         # Port 8000

shared/
├── common/              # Exceptions, constants
├── gps/                 # Haversine, geocoding, routing
└── config.py, database.py, redis_client.py
```

## Important Conventions
- All services use multi-schema PostgreSQL
- GPS coordinates use lat/lng format
- Authentication via JWT access/refresh tokens in HttpOnly cookies
- Inter-service communication via Redis Pub/Sub events
