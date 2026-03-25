# ARCHITECTURE.md

# Clinic Home Visit System - Architecture

## System Overview

Microservices-based system for finding clinics and booking home visits.

## Architecture Diagram

```
Frontend (Vue.js 3) → API Gateway (8000) → Services
                                              │
          ┌──────────────┬────────┬────────┬────────┐
          │              │        │        │        │
       Auth(8003)  Clinic(8001)  Booking  Review  Notification
          │              │       (8002)  (8004)   (8005)
          └──────────────┴─────────┴────────┴────────┘
                              │
                    PostgreSQL + Redis
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| api-gateway | 8000 | Request routing, auth, rate limiting |
| auth-service | 8003 | Authentication, JWT tokens |
| clinic-service | 8001 | Clinic management, GPS features |
| booking-service | 8002 | Appointment booking |
| review-service | 8004 | Reviews and ratings |
| notification-service | 8005 | Email/SMS notifications |
| data-collector | 8006 | Crawl clinic data |

## GPS Features

- **Haversine Distance**: Straight-line distance calculation
- **OSRM Routing**: Shortest path with turn-by-turn directions
- **Nominatim Geocoding**: Address to GPS coordinates
- **Geofilter**: Filter clinics within radius

## Quick Start

```bash
docker-compose up -d
make logs -f
```

## API Documentation

Access Swagger UI at: `http://localhost:8000/docs`
