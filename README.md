# ClinicSearch — Hệ thống tìm kiếm phòng khám & khám tại nhà

> Hệ thống microservices đầy đủ tính năng: tìm kiếm phòng khám theo GPS, đặt lịch khám tại nhà / tại phòng khám, đánh giá, thông báo. Backend Python (FastAPI) + Frontend Vue.js 3 + Traefik + PostgreSQL + Redis + Docker.

---

## Mục lục

- [Tổng quan](#tổng-quan)
- [Kiến trúc](#kiến-trúc)
- [Danh sách services](#danh-sách-services)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Bắt đầu nhanh](#bắt-đầu-nhanh)
- [Chạy local không Docker](#chạy-local-không-docker)
- [Frontend](#frontend)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Scripts tiện ích](#scripts-tiện-ích)
- [Monitoring](#monitoring)
- [Environment Variables](#environment-variables)
- [Phát triển](#phát-triển)
- [Giấy phép](#giấy-phép)

---

## Tổng quan

**ClinicSearch** là hệ thống tìm kiếm và đặt lịch khám tại nhà, hỗ trợ:

- Tìm phòng khám gần vị trí người dùng (GPS / geocoding)
- Tính khoảng cách chính xác (Haversine, OSRM routing)
- Đặt lịch khám tại phòng khám hoặc tại nhà
- Bác sĩ với lịch trình và review chi tiết
- Hệ thống đánh giá và báo cáo nội dung
- Gửi thông báo qua Email / SMS
- Thu thập dữ liệu phòng khám tự động
- Monitoring với Prometheus + Grafana

---

## Kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                      Trình duyệt                         │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP (port 80)
                         ▼
┌─────────────────────────────────────────────────────────┐
│          Traefik (Reverse Proxy & Load Balancer)        │
│              traefik:80 → gateway:8000                   │
└────────────────────────┬────────────────────────────────┘
                         │ /api/{service}/*
                         ▼
┌─────────────────────────────────────────────────────────┐
│               API Gateway  (FastAPI)                     │
│         Port 8000 · Auth proxy · Rate limit            │
└───┬───────┬───────┬───────┬───────┬───────┬────────────┘
    │       │       │       │       │       │
    ▼       ▼       ▼       ▼       ▼       ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌────────┐
│ Auth │ │Clinic│ │Booking│ │Review│ │Notif.│ │ Data  │
│:8003 │ │:8001 │ │:8002 │ │:8004 │ │:8005 │ │:8006  │
└──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └───┬────┘
   │        │         │        │        │         │
   └───┬────┴────┬────┴────────┴────────┴─────────┘
       ▼         ▼
  ┌─────────┐ ┌──────┐
  │PostgreSQL│ │Redis │
  │ (15)   │ │ 7    │
  │multi-  │ │Cache │
  │schema  │ │Pub/Sub│
  └─────────┘ └──────┘
       │
  ┌────────────┐
  │Prometheus  │
  │ + Grafana  │
  └────────────┘
```

### Luồng request mặc định

| URL | Đích |
|-----|------|
| `/` | Frontend (Vue SPA qua Nginx) |
| `/api/auth/*` | → Auth Service (8003) |
| `/api/clinic/*` | → Clinic Service (8001) |
| `/api/booking/*` | → Booking Service (8002) |
| `/api/review/*` | → Review Service (8004) |
| `/api/notification/*` | → Notification Service (8005) |
| `/api/collector/*` | → Data Collector Service (8006) |
| `/metrics` | Prometheus metrics (API Gateway) |

---

## Danh sách services

| Service | Port | Mô tả | Database | Redis |
|---------|------|--------|---------|-------|
| **api-gateway** | 8000 | Điều hướng request, CORS, rate limit, auth proxy | — | ✓ |
| **auth-service** | 8003 | Xác thực JWT, phân quyền, quản lý users, refresh tokens, locations | `auth_schema` | ✓ |
| **clinic-service** | 8001 | CRUD phòng khám, bác sĩ, GPS tìm kiếm, geocoding, routing | `clinic_schema` | ✓ |
| **booking-service** | 8002 | Quản lý đặt lịch, time slots, thanh toán | `booking_schema` | ✓ |
| **review-service** | 8004 | Đánh giá, báo cáo nội dung, phản hồi | `review_schema` | — |
| **notification-service** | 8005 | Gửi email (SMTP) / SMS, notification queue | — | ✓ |
| **data-collector-service** | 8006 | Thu thập dữ liệu phòng khám tự động | `clinic_schema` | ✓ |
| **frontend** | 80 | Vue.js 3 SPA phục vụ qua Nginx | — | — |

### Middleware / Infrastructure

| Component | Image | Port | Mô tả |
|-----------|-------|------|--------|
| Traefik | traefik:3.0.4 | 80, 443, 8080 | Reverse proxy, auto-discovery |
| PostgreSQL | postgres:15 | 5432 | Multi-schema database |
| Redis | redis:7-alpine | 6379 | Cache, pub/sub, rate limiting |
| Prometheus | prom/prometheus | 9090 | Metrics collection |
| Grafana | grafana/grafana | 3001 | Dashboards (admin/admin) |

---

## Cấu trúc thư mục

```
clinic-home-visit-system/
├── docker-compose.yml          # Toàn bộ hệ thống
├── README.md                  # Tài liệu này
│
├── frontend/                  # Vue.js 3 SPA
│   ├── src/
│   │   ├── main.js            # Entry point
│   │   ├── App.vue            # Root component
│   │   ├── style.css          # Tailwind + custom CSS
│   │   ├── router/
│   │   │   └── index.js      # Vue Router (6 routes)
│   │   ├── views/             # Page components
│   │   │   ├── HomeView.vue
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── ClinicsView.vue
│   │   │   ├── ClinicDetailView.vue
│   │   │   ├── BookingsView.vue
│   │   │   └── ProfileView.vue
│   │   ├── components/
│   │   │   └── ClinicCard.vue
│   │   ├── services/
│   │   │   └── api.js         # Axios HTTP client
│   │   └── stores/            # Pinia stores
│   │       ├── auth.js
│   │       └── clinic.js
│   ├── Dockerfile             # Multi-stage: Vite build → Nginx
│   ├── nginx.conf             # Cấu hình Nginx SPA fallback
│   ├── vite.config.js         # Vite dev server (port 3000)
│   ├── tailwind.config.js     # Tailwind v3 config
│   ├── postcss.config.js      # PostCSS (Tailwind + Autoprefixer)
│   └── package.json
│
├── services/                  # Microservices (FastAPI)
│   ├── api-gateway/
│   │   ├── main.py            # FastAPI app · proxy /api/{service}/*
│   │   └── Dockerfile
│   ├── auth-service/          # Port 8003
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── auth.py        # /api/v1/auth (login, register, refresh)
│   │   │   ├── users.py       # /api/v1/users (CRUD, profile)
│   │   │   └── locations.py   # /api/v1/locations (user addresses)
│   │   ├── utils/dependencies.py
│   │   └── Dockerfile
│   ├── clinic-service/        # Port 8001
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── clinics.py     # /api/v1/clinics
│   │   │   ├── doctors.py     # /api/v1/doctors
│   │   │   └── gps.py         # /api/v1/gps (distance, route)
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── utils/dependencies.py
│   │   └── Dockerfile
│   ├── booking-service/       # Port 8002
│   │   ├── main.py
│   │   ├── routers/
│   │   │   └── bookings.py    # /api/v1/bookings
│   │   ├── models/models.py
│   │   ├── utils/dependencies.py
│   │   └── Dockerfile
│   ├── review-service/        # Port 8004
│   │   ├── main.py
│   │   ├── routers/
│   │   │   └── reviews.py     # /api/v1/reviews
│   │   └── Dockerfile
│   ├── notification-service/  # Port 8005
│   │   ├── main.py
│   │   ├── routers/
│   │   │   └── notifications.py
│   │   └── Dockerfile
│   └── data-collector-service/ # Port 8006
│       ├── main.py
│       ├── routers/
│       │   └── collectors.py
│       └── Dockerfile
│
├── shared/                    # Thư viện dùng chung
│   ├── config.py              # Pydantic Settings (.env)
│   ├── database.py            # SQLAlchemy async, multi-schema
│   ├── redis_client.py        # Redis async client
│   ├── message_broker.py      # Redis pub/sub wrapper
│   ├── gps/                   # GPS utilities
│   │   ├── geocoding.py       # Nominatim geocoding
│   │   ├── haversine.py       # Distance calculation
│   │   ├── routing.py         # OSRM routing
│   │   ├── geofilter.py       # Bounding box filtering
│   │   └── schemas.py         # GPS Pydantic models
│   └── common/
│       ├── constants.py
│       ├── exceptions.py      # Custom exceptions
│       └── responses.py       # Standardized API responses
│
├── traefik/
│   ├── traefik.yml            # Traefik static config
│   └── dynamic/
│       └── http.yml           # Dynamic service discovery
│
├── scripts/
│   └── init-schemas.sql       # Khởi tạo database schemas + indexes
│
├── prometheus/
│   └── prometheus.yml         # Prometheus scrape config
│
└── grafana/
    └── provisioning/           # Auto-provision Grafana dashboards
```

---

## Bắt đầu nhanh

### Yêu cầu

- Docker & Docker Compose v2+
- 4 GB RAM tối thiểu (8 GB khuyến nghị)
- Cổng 80, 443, 5432, 6379, 8000–8006, 9090, 3001 trống

### 1. Clone & khởi động

```bash
# Di chuyển vào thư mục dự án
cd clinic-home-visit-system

# Khởi động toàn bộ hệ thống (build + chạy)
docker-compose up -d

# Xem trạng thái containers
docker-compose ps

# Xem logs tất cả services
docker-compose logs -f

# Xem logs service cụ thể
docker-compose logs -f auth-service
```

### 2. Truy cập

| Service | URL |
|---------|-----|
| Frontend (trình duyệt) | http://localhost |
| Swagger UI (API Gateway) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 (admin/admin) |
| Traefik Dashboard | http://localhost:8080 |

### 3. Dừng hệ thống

```bash
docker-compose down          # Dừng, giữ dữ liệu
docker-compose down -v       # Dừng + xóa volumes (mất dữ liệu)
```

### Health checks

Tất cả services có 3 endpoint health:

```
GET /health          # Liveness cơ bản
GET /health/ready    # Readiness (DB + Redis)
GET /health/live     # Liveness đơn giản
GET /metrics         # Prometheus metrics (qua API Gateway: /metrics)
```

---

## Chạy local không Docker

Cần chạy riêng frontend và backend (hữu ích khi debug).

### Backend (từng service)

```bash
# Tạo virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Cài dependencies (chạy trong thư mục gốc hoặc từng service)
pip install -r requirements.txt  # nếu có file này ở gốc
# Hoặc cài trực tiếp:
pip install fastapi uvicorn sqlalchemy asyncpg pydantic-settings structlog httpx redis prometheus-fastapi-instrumentator

# Database: chạy PostgreSQL và Redis riêng
# Hoặc dùng Docker chỉ cho DB:
docker run -d -p 5432:5432 -p 6379:6379 --name clinic-db \
  -e POSTGRES_PASSWORD=postgres \
  postgres:15

# Chạy migrations (tạo schemas)
psql -U postgres -h localhost -f scripts/init-schemas.sql

# Chạy từng service:
cd services/auth-service
uvicorn main:app --reload --port 8003

# (Mở terminal mới)
cd services/clinic-service
uvicorn main:app --reload --port 8001

# Tiếp tục với các service khác...
```

### Frontend (Vue)

```bash
cd frontend
npm install
npm run dev      # Dev server: http://localhost:3000 (hoặc 3001/3002 nếu bận)
npm run build    # Production build
```

> **Lưu ý:** Khi chạy local, cổng backend thường là `8000`, frontend Vite proxy qua `/api` → `http://localhost:8000`.

---

## Frontend

### Công nghệ

- **Framework:** Vue.js 3 (Composition API + `<script setup>`)
- **Build tool:** Vite 5
- **CSS:** Tailwind CSS v3 + PostCSS
- **State:** Pinia
- **Router:** Vue Router 4
- **HTTP:** Axios
- **Map:** Leaflet + Vue-Leaflet
- **Icons:** Heroicons (SVG, không dùng emoji)

### Routes

| Path | Component | Auth |
|------|-----------|------|
| `/` | HomeView | Public |
| `/login` | LoginView | Public |
| `/register` | RegisterView | Public |
| `/clinics` | ClinicsView | Public |
| `/clinics/:id` | ClinicDetailView | Public |
| `/bookings` | BookingsView | Required |
| `/profile` | ProfileView | Required |

### Stores (Pinia)

- **auth** — Token, user state, login/logout/register actions
- **clinic** — Clinic list, search, filters, pagination

### API Service

`src/services/api.js` là axios instance với interceptors:
- Auto gắn `Authorization: Bearer <token>` từ cookie
- Proxy qua Vite dev server → Backend

---

## API Documentation

### Auth Service (`:8003`)

```
POST /api/v1/auth/register     Đăng ký tài khoản
POST /api/v1/auth/login        Đăng nhập (JWT access + refresh token)
POST /api/v1/auth/refresh      Refresh access token
POST /api/v1/auth/logout       Đăng xuất (revoke refresh token)
POST /api/v1/auth/forgot-password
POST /api/v1/auth/reset-password

GET  /api/v1/users/me          Lấy thông tin user hiện tại
PUT  /api/v1/users/me          Cập nhật profile
GET  /api/v1/users/locations   Danh sách địa chỉ
POST /api/v1/users/locations   Thêm địa chỉ mới
```

### Clinic Service (`:8001`)

```
GET  /api/v1/clinics                    Danh sách phòng khám (filter, search, pagination)
POST /api/v1/clinics                    Tạo phòng khám (owner)
GET  /api/v1/clinics/{id}               Chi tiết phòng khám
PUT  /api/v1/clinics/{id}               Cập nhật phòng khám
DELETE /api/v1/clinics/{id}             Xóa phòng khám
GET  /api/v1/clinics/nearby             Tìm phòng khám gần (lat, lng, radius)
GET  /api/v1/clinics/search             Tìm kiếm nâng cao

GET  /api/v1/doctors                    Danh sách bác sĩ
POST /api/v1/doctors                    Tạo bác sĩ
GET  /api/v1/doctors/{id}               Chi tiết bác sĩ
PUT  /api/v1/doctors/{id}               Cập nhật bác sĩ

GET  /api/v1/gps/distance               Tính khoảng cách 2 điểm (Haversine)
GET  /api/v1/gps/route                  Tính route (OSRM)
GET  /api/v1/gps/geocode                Geocoding (Nominatim)
```

### Booking Service (`:8002`)

```
GET  /api/v1/bookings                   Danh sách bookings (user/clinic)
POST /api/v1/bookings                   Tạo booking mới
GET  /api/v1/bookings/{id}              Chi tiết booking
PUT  /api/v1/bookings/{id}              Cập nhật booking
DELETE /api/v1/bookings/{id}            Hủy booking
GET  /api/v1/bookings/{id}/slots        Lấy time slots trống
```

### Review Service (`:8004`)

```
GET  /api/v1/reviews                     Danh sách reviews
POST /api/v1/reviews                    Tạo review (sau khi hoàn thành booking)
GET  /api/v1/reviews/{id}               Chi tiết review
PUT  /api/v1/reviews/{id}               Cập nhật review
DELETE /api/v1/reviews/{id}              Xóa review
POST /api/v1/reviews/{id}/report         Báo cáo review
POST /api/v1/reviews/{id}/reply         Phản hồi review (clinic owner)
```

### Notification Service (`:8005`)

```
GET  /api/v1/notifications              Danh sách notifications (user)
POST /api/v1/notifications/send         Gửi notification (email/SMS)
POST /api/v1/notifications/send-batch   Gửi nhiều notification
```

### Data Collector Service (`:8006`)

```
POST /api/v1/collectors/collect          Chạy thu thập dữ liệu
GET  /api/v1/collectors/status           Trạng thái collector
POST /api/v1/collectors/sync             Sync dữ liệu từ nguồn
```

---

## Database Schema

Hệ thống dùng **PostgreSQL multi-schema** — mỗi service có schema riêng:

| Schema | Tables |
|--------|--------|
| `auth_schema` | `users`, `user_locations`, `refresh_tokens` |
| `clinic_schema` | `clinics`, `doctors`, `doctor_schedules` |
| `booking_schema` | `bookings`, `booking_slots` |
| `review_schema` | `reviews`, `review_reports` |
| `notification_schema` | `notifications`, `email_templates` |

### Mối quan hệ chính

```
users ───< user_locations          (1:N)
users ───< bookings                (1:N)
users ───< reviews                 (1:N)
clinics ───< doctors               (1:N)
clinics ───< bookings              (1:N)
clinics ───< reviews              (1:N)
doctors ───< doctor_schedules      (1:N)
doctors ───< bookings             (1:N)
doctors ───< reviews              (1:N)
bookings ───< booking_slots        (1:N)
bookings ───< reviews             (1:N)
reviews ───< review_reports        (1:N)
```

Schema được tạo tự động qua `scripts/init-schemas.sql` khi container `postgres` khởi động lần đầu.

---

## Scripts tiện ích

```bash
# Chạy migration trong container
docker-compose exec postgres psql -U postgres -d postgres -f /scripts/init-schemas.sql

# Seed dữ liệu mẫu
docker-compose exec clinic-service python -c "from shared.database import Database; ..."

# Restart một service cụ thể
docker-compose restart auth-service

# Rebuild không dùng cache
docker-compose build --no-cache auth-service

# Xem resource usage
docker stats

# Truy cập PostgreSQL
docker-compose exec postgres psql -U postgres -d postgres

# Truy cập Redis
docker-compose exec redis redis-cli
```

---

## Monitoring

### Prometheus Metrics

Mỗi service expose `/metrics` với Prometheus FastAPI Instrumentator:
- `http_requests_total` (method, path, status)
- `http_request_duration_seconds`
- `http_requests_in_progress`
- Thêm custom metrics tùy service

### Grafana Dashboards

- Truy cập: http://localhost:3001
- Login: `admin` / `admin`
- Dashboards được auto-provision từ `grafana/provisioning/`

### Các metrics quan trọng cần theo dõi

| Metric | Service | Alert threshold |
|--------|---------|----------------|
| `http_request_duration_seconds_p99` | api-gateway | > 2s |
| `http_requests_total{status="5xx"}` | api-gateway | > 10/min |
| DB connection pool usage | auth/clinic/booking | > 80% |
| Redis memory | notification | > 200MB |

---

## Environment Variables

Cấu hình qua file `.env` (đặt ở thư mục gốc dự án):

```env
# ─── Security ────────────────────────────────────────────────────────────────
JWT_SECRET=your-super-secret-key-change-in-production

# ─── Database ────────────────────────────────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/postgres

# ─── Redis ───────────────────────────────────────────────────────────────────
REDIS_URL=redis://redis:6379

# ─── External Services ───────────────────────────────────────────────────────
NOMINATIM_URL=https://nominatim.openstreetmap.org
OSRM_URL=https://router.project-osrm.org

# ─── Email (Notification Service) ────────────────────────────────────────────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# ─── SMS ─────────────────────────────────────────────────────────────────────
SMS_API_KEY=your-sms-api-key

# ─── Optional Overrides ───────────────────────────────────────────────────────
DEBUG=true
LOG_LEVEL=DEBUG
CORS_ORIGINS=["http://localhost:3000","http://localhost"]
```

> **Security:** Thay `JWT_SECRET` bằng giá trị ngẫu nhiên dài (ít nhất 32 ký tự) trước khi deploy production. Không commit `.env` vào git.

---

## Phát triển

### Thêm một service mới

1. Tạo thư mục `services/<tên-service>/`
2. Copy cấu trúc từ service có sẵn (ví dụ: `review-service`)
3. Thêm vào `docker-compose.yml` với config tương tự
4. Thêm route vào `traefik/dynamic/http.yml`
5. Update API Gateway proxy trong `services/api-gateway/main.py`
6. Thêm schema vào `scripts/init-schemas.sql`

### Demo

https://github.com/user-attachments/assets/90288400-c9fa-4101-8dde-60879c9cb102
![download](https://github.com/user-attachments/assets/253c8a45-8d68-4264-9724-489f013feaa0)
![5a7db737-d1ce-480e-862f-d8c625145540](https://github.com/user-attachments/assets/92c6b969-7237-4de6-9909-37ee9c013ce4)
![11d9cd77-cd5d-4e90-8f75-52e486b5793f](https://github.com/user-attachments/assets/7d9988f5-1107-420c-ae9f-35e4cc337c85)
![4656a3a5-7e35-4834-b6b9-b05cbb965047](https://github.com/user-attachments/assets/44f54e4c-8927-4bc0-9493-935a1daa79fe)
![05804875-c251-46f1-be00-6ebf37fb0f78](https://github.com/user-attachments/assets/a81692ee-7775-4036-9ad0-7242441564e2)
<img width="72" height="72" alt="gray" src="https://github.com/user-attachments/assets/3d301a40-2984-430f-8d3d-8128c24bcc77" />


### Debug

```bash
# Logs chi tiết của một service
docker-compose logs -f --tail=200 auth-service

# Vào container để debug
docker-compose exec auth-service /bin/sh

# Kiểm tra health của tất cả services
curl http://localhost:8000/health     # Gateway
curl http://localhost:8003/health     # Auth
curl http://localhost:8001/health     # Clinic
curl http://localhost:8002/health     # Booking
curl http://localhost:8004/health     # Review
```

---

## Giấy phép

MIT License — xem file `LICENSE` (nếu có).
