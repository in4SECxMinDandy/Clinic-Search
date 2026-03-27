# Clinic Home Visit System

Hệ thống Quản lý và Đặt lịch Phòng khám - Hỗ trợ Khám bệnh tại Nhà. Được xây dựng với kiến trúc Microservices xử lý hiệu năng cao, kết hợp giao diện Vue.js 3 hiện đại.

## Mục lục

- [Mô tả dự án](#mô-tả-dự-án)
- [Tính năng](#tính-năng)
- [Kiến trúc](#kiến-trúc)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cài đặt](#cài-đặt)
- [Chạy ứng dụng](#chạy-ứng-dụng)
- [Cấu hình môi trường](#cấu-hình-môi-trường)
- [API Endpoints](#api-endpoints)
- [Phân quyền người dùng](#phân-quyền-người-dùng)
- [Database Schema](#database-schema)
- [Scripts](#scripts)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Đóng góp](#đóng-góp)
- [License](#license)

---

## Mô tả dự án

Hệ thống kết nối bệnh nhân với các phòng khám, cung cấp khả năng tìm kiếm phòng khám gần nhất thông qua tọa độ GPS, xử lý quy trình đặt lịch khám trực tiếp hoặc yêu cầu bác sĩ đến khám tại nhà một cách liền mạch.

### Mục tiêu
- Cung cấp nền tảng đặt lịch khám trực tuyến tiện lợi
- Hỗ trợ khám bệnh tại nhà cho người có nhu cầu
- Quản lý phòng khám và bác sĩ hiệu quả
- Đánh giá chất lượng dịch vụ y tế

---

## Tính năng

### 1. Tìm kiếm Phòng khám (Clinic Search)
- Tìm kiếm phòng khám theo vị trí GPS
- Lọc theo bán kính (km)
- Sắp xếp theo khoảng cách
- Xem chi tiết thông tin phòng khám
- Lọc theo chuyên khoa
- Xem đánh giá và điểm trung bình

### 2. Hệ thống Đặt lịch (Booking)
- Đặt lịch khám tại phòng khám (Clinic Visit)
- Đặt lịch khám tại nhà (Home Visit)
- Quản lý trạng thái: Chờ xác nhận → Đã xác nhận → Đã hoàn thành / Đã hủy
- Chủ phòng khám duyệt/từ chối yêu cầu đặt lịch
- Hủy đặt lịch với lý do

### 3. Hệ thống Review
- Đánh giá bằng sao (1-5 sao)
- Nhận xét chi tiết sau khi hoàn thành khám
- Xem đánh giá trung bình của phòng khám
- Reply từ chủ phòng khám

### 4. Thông báo (Notifications)
- Thông báo thời gian thực
- Cập nhật trạng thái đặt lịch
- Thông báo cho bệnh nhân và chủ phòng khám
- Kênh notification riêng biệt

### 5. Dashboard Admin
- Quản lý tài khoản người dùng (khóa/mở khóa, đổi vai trò)
- Quản lý chủ phòng khám
- Quản lý phòng khám
- Quản lý bác sĩ
- Xem thống kê hệ thống

### 6. Dashboard Owner (Chủ Phòng khám)
- Quản lý cơ sở phòng khám
- Quản lý bác sĩ trong phòng khám
- Duyệt/từ chối yêu cầu đặt lịch
- Xem lịch hẹn của phòng khám
- Trả lời review từ bệnh nhân

### 7. Thu thập dữ liệu GPS
- Thu thập vị trí phòng khám
- Cập nhật thông tin GPS tự động

---

## Kiến trúc

```
clinic-home-visit-system/
├── services/
│   ├── api-gateway/              # Port 8000 - Điều hướng API, Rate Limiting
│   ├── auth-service/             # Port 8003 - Xác thực & Ủy quyền
│   ├── clinic-service/           # Port 8001 - Quản lý phòng khám
│   ├── booking-service/          # Port 8002 - Quản lý đặt lịch
│   ├── review-service/           # Port 8004 - Đánh giá & Review
│   ├── notification-service/     # Port 8005 - Thông báo
│   └── data-collector-service/  # Port 8006 - Thu thập dữ liệu GPS
├── frontend/                     # Vue.js 3 Frontend
│   ├── src/
│   │   ├── views/               # Trang chính
│   │   ├── components/          # Component reuse
│   │   ├── stores/              # Pinia stores
│   │   ├── services/            # API client
│   │   └── router/              # Vue Router
│   └── Dockerfile
├── shared/                      # Shared modules (config, database, redis)
├── traefik/                     # Reverse Proxy & Load Balancer
├── prometheus/                  # Prometheus config
├── grafana/                     # Grafana dashboards
├── scripts/                     # Database seeding scripts
└── docker-compose.yml           # Docker Compose orchestration
```

### Luồng dữ liệu

```
[Frontend/Vue.js]
       ↓ HTTP
[API Gateway/Traefik] (Port 8000)
       ↓ Internal
[Auth Service] ←→ [PostgreSQL]
[Clinic Service] ←→ [PostgreSQL]
[Booking Service] ←→ [PostgreSQL]
[Review Service] ←→ [PostgreSQL]
[Notification Service] ←→ [Redis Pub/Sub]
```

---

## Công nghệ sử dụng

| Layer | Technology | Version |
|-------|------------|---------|
| **Frontend** | Vue.js 3 | 3.4+ |
| | Vite | 5.0+ |
| | TailwindCSS | 3.4+ |
| | Pinia | 2.1+ |
| | Vue Router | 4.2+ |
| | Axios | 1.6+ |
| **Backend** | Python | 3.12+ |
| | FastAPI | 0.109+ |
| | SQLAlchemy | 2.0+ |
| | Pydantic | 2.5+ |
| | Uvicorn | 0.27+ |
| **Database** | PostgreSQL | 15 |
| **Cache** | Redis | 7 |
| **Gateway** | Traefik | 3.0 |
| **Monitoring** | Prometheus | - |
| | Grafana | - |
| **Container** | Docker | 24+ |
| | Docker Compose | 2.20+ |

---

## Cài đặt

### Yêu cầu hệ thống

| Yêu cầu | Phiên bản tối thiểu |
|----------|---------------------|
| Docker Desktop | 4.0+ |
| Docker Compose | 2.0+ |
| Git | 2.0+ |
| RAM | 4GB+ |
| Disk | 10GB+ |

### 1. Clone Repository

```bash
git clone https://github.com/your-repo/clinic-home-visit-system.git
cd clinic-home-visit-system
```

### 2. Cấu hình Environment

Tạo file `.env` trong thư mục gốc:

```env
# ====================
# Database Configuration
# ====================
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=clinic_system

# ====================
# JWT Configuration
# ====================
JWT_SECRET=your-secret-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# ====================
# Service URLs (for Docker internal)
# ====================
AUTH_SERVICE_URL=http://auth-service:8003
CLINIC_SERVICE_URL=http://clinic-service:8001
BOOKING_SERVICE_URL=http://booking-service:8002
REVIEW_SERVICE_URL=http://review-service:8004
NOTIFICATION_SERVICE_URL=http://notification-service:8005
DATA_COLLECTOR_SERVICE_URL=http://data-collector-service:8006

# ====================
# Redis
# ====================
REDIS_URL=redis://redis:6379

# ====================
# CORS
# ====================
CORS_ORIGINS=http://localhost:3000,http://localhost,http://127.0.0.1:3000

# ====================
# Debug Mode
# ====================
DEBUG=true
LOG_LEVEL=INFO

# ====================
# SMTP (for emails)
# ====================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# ====================
# Cookie Security
# ====================
COOKIE_SECURE=false
```

### 3. Khởi tạo Database

Database schema sẽ được tự động khởi tạo khi container PostgreSQL start lần đầu.

Để seed dữ liệu mẫu:

```bash
# Seed admin user
docker compose exec postgres psql -U postgres -d postgres -f /scripts/seed_admin_user.sql

# Seed demo data (users, clinics, doctors)
docker compose exec postgres psql -U postgres -d postgres -f /scripts/seed_demo_data.sql
```

---

## Chạy ứng dụng

### Cách 1: Docker Compose (Khuyến nghị - Production)

```bash
# Build và chạy tất cả services
docker compose up -d --build

# Xem logs tất cả services
docker compose logs -f

# Xem logs của service cụ thể
docker compose logs -f auth-service

# Dừng tất cả services
docker compose down

# Dừng và xóa volumes (reset hoàn toàn)
docker compose down -v
```

### Cách 2: Chạy cục bộ (Development)

#### Backend Services

```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/services"

# Auth Service
cd services/auth-service
pip install -r requirements.txt
uvicorn auth_service.main:app --reload --port 8003

# Clinic Service (terminal khác)
cd services/clinic-service
pip install -r requirements.txt
uvicorn clinic_service.main:app --reload --port 8001

# Booking Service (terminal khác)
cd services/booking-service
pip install -r requirements.txt
uvicorn booking_service.main:app --reload --port 8002
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Kiểm tra Services

```bash
# Kiểm tra tất cả containers
docker compose ps

# Kiểm tra health của từng service
curl http://localhost:8000/health          # API Gateway
curl http://localhost:8001/health          # Clinic Service
curl http://localhost:8002/health          # Booking Service
curl http://localhost:8003/health          # Auth Service
curl http://localhost:8004/health          # Review Service
curl http://localhost:8005/health          # Notification Service
curl http://localhost:8006/health          # Data Collector Service
```

### Truy cập Ứng dụng

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost | - |
| API Gateway | http://localhost:8000 | - |
| Auth Service | http://localhost:8003 | - |
| Traefik Dashboard | http://localhost:8080/dashboard/ | - |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | - |
| PostgreSQL | localhost:5432 | postgres / postgres |
| Redis | localhost:6379 | - |

---

## Cấu hình môi trường

### Các biến môi trường quan trọng

| Biến | Mô tả | Giá trị mặc định |
|------|-------|------------------|
| `JWT_SECRET` | Secret key cho JWT tokens | supersecretkey123 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Thời gian hết hạn access token (phút) | 15 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Thời gian hết hạn refresh token (ngày) | 7 |
| `COOKIE_SECURE` | Cookie secure flag | false |
| `CORS_ORIGINS` | Danh sách origins được phép | * |
| `LOG_LEVEL` | Mức độ log | INFO |
| `DEBUG` | Chế độ debug | true |

---

## API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Mô tả | Body |
|--------|----------|-------|------|
| POST | `/register` | Đăng ký tài khoản | `{email, password, full_name, phone, role?}` |
| POST | `/login` | Đăng nhập | `{email, password}` |
| POST | `/logout` | Đăng xuất | - |
| POST | `/refresh` | Làm mới token | `{refresh_token}` |
| POST | `/forgot-password` | Quên mật khẩu | `{email}` |
| POST | `/reset-password` | Đặt lại mật khẩu | `{token, new_password}` |

### Users (`/api/v1/users`)

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| GET | `/me` | Thông tin user hiện tại | Required |
| PUT | `/me` | Cập nhật thông tin | Required |
| GET | `/admin/all` | Danh sách tất cả users | Admin |
| PUT | `/admin/{user_id}/role` | Đổi vai trò user | Admin |
| PUT | `/admin/{user_id}/status` | Khóa/Mở khóa user | Admin |

### Clinics (`/api/v1/clinics`)

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| GET | `/` | Tìm kiếm phòng khám | - |
| POST | `/` | Tạo phòng khám mới | Owner |
| GET | `/{id}` | Chi tiết phòng khám | - |
| PUT | `/{id}` | Cập nhật phòng khám | Owner |
| DELETE | `/{id}` | Xóa phòng khám | Admin |
| GET | `/owner/my-clinics` | Danh sách phòng khám của tôi | Owner |
| GET | `/nearby` | Tìm phòng khám gần đây | - |

### Bookings (`/api/v1/bookings`)

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| GET | `/` | Danh sách đặt lịch của user | Required |
| POST | `/` | Tạo đặt lịch mới | Patient |
| GET | `/{id}` | Chi tiết đặt lịch | Required |
| PUT | `/{id}/status` | Cập nhật trạng thái | Required |
| DELETE | `/{id}` | Hủy đặt lịch | Patient/Admin |
| GET | `/clinic/owner/all` | Danh sách đặt lịch (Owner) | Owner |
| PUT | `/clinic/{clinic_id}/owner/update-status/{booking_id}` | Duyệt/từ chối | Owner |

### Reviews (`/api/v1/reviews`)

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| GET | `/clinic/{clinic_id}` | Đánh giá theo phòng khám | - |
| POST | `/` | Tạo đánh giá | Patient |
| PUT | `/{id}` | Cập nhật đánh giá | Patient |
| POST | `/{id}/reply` | Trả lời đánh giá | Owner |

### Doctors (`/api/v1/doctors`)

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| GET | `/` | Danh sách bác sĩ | - |
| GET | `/clinic/{clinic_id}` | Bác sĩ theo phòng khám | - |
| POST | `/` | Thêm bác sĩ mới | Owner |
| PUT | `/{id}` | Cập nhật thông tin bác sĩ | Owner |

### Locations (`/api/v1/locations`)

| Method | Endpoint | Mô tả | Auth |
|--------|----------|-------|------|
| GET | `/me` | Danh sách địa chỉ của tôi | Required |
| POST | `/` | Thêm địa chỉ mới | Required |
| PUT | `/{id}` | Cập nhật địa chỉ | Required |
| DELETE | `/{id}` | Xóa địa chỉ | Required |

---

## Phân quyền người dùng

### Vai trò (Roles)

| Role | Mô tả | Khả năng |
|------|-------|----------|
| `admin` | Quản trị viên hệ thống | Toàn quyền quản lý |
| `clinic_owner` | Chủ phòng khám | Quản lý phòng khám của mình |
| `doctor` | Bác sĩ | Xem thông tin, nhận lịch khám |
| `patient` | Bệnh nhân | Đặt lịch, đánh giá |
| `collector` | Người thu thập dữ liệu | Thu thập GPS data |

### Ma trận quyền

| Chức năng | Admin | Owner | Doctor | Patient | Collector |
|-----------|-------|-------|--------|---------|-----------|
| Quản lý users | ✅ | ❌ | ❌ | ❌ | ❌ |
| Quản lý phòng khám | ✅ | ✅ (sở hữu) | ❌ | ❌ | ❌ |
| Quản lý bác sĩ | ✅ | ✅ (sở hữu) | ❌ | ❌ | ❌ |
| Duyệt đặt lịch | ✅ | ✅ (sở hữu) | ❌ | ❌ | ❌ |
| Tạo đặt lịch | ✅ | ❌ | ❌ | ✅ | ❌ |
| Tạo review | ✅ | ❌ | ❌ | ✅ | ❌ |
| Trả lời review | ✅ | ✅ (sở hữu) | ❌ | ❌ | ❌ |
| Thu thập GPS | ✅ | ❌ | ❌ | ❌ | ✅ |

---

## Database Schema

### Auth Schema (auth_service)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'patient',
    is_active BOOLEAN DEFAULT true,
    email_verified_at TIMESTAMP,
    last_login_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User locations
CREATE TABLE user_locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    label VARCHAR(100),
    address TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    is_default BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Refresh tokens
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Clinic Schema (clinic_service)

```sql
-- Clinics table
CREATE TABLE clinics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID REFERENCES auth_schema.users(id),
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    phone VARCHAR(20),
    description TEXT,
    image_url TEXT,
    opening_hours JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Doctors
CREATE TABLE doctors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clinic_id UUID REFERENCES clinics(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth_schema.users(id),
    specialization VARCHAR(100),
    license_number VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Booking Schema (booking_service)

```sql
-- Bookings table
CREATE TABLE bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES auth_schema.users(id),
    clinic_id UUID REFERENCES clinic_schema.clinics(id),
    doctor_id UUID REFERENCES clinic_schema.doctors(id),
    booking_type VARCHAR(50) NOT NULL, -- 'clinic_visit' or 'home_visit'
    scheduled_at TIMESTAMP NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    home_address TEXT,
    home_lat DOUBLE PRECISION,
    home_lng DOUBLE PRECISION,
    symptoms TEXT,
    notes TEXT,
    cancellation_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Review Schema (review_service)

```sql
-- Reviews table
CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES booking_schema.bookings(id),
    clinic_id UUID REFERENCES clinic_schema.clinics(id),
    patient_id UUID REFERENCES auth_schema.users(id),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    owner_reply TEXT,
    owner_reply_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Scripts

### Database Seeding

```bash
# Seed admin user
# Default: admin@clinic.com / Admin123!
docker compose exec postgres psql -U postgres -d postgres -f scripts/seed_admin_user.sql

# Seed demo data (users, clinics, doctors, bookings)
docker compose exec postgres psql -U postgres -d postgres -f scripts/seed_demo_data.sql

# Reset database
docker compose down -v
docker compose up -d postgres
# Wait for postgres to be ready
sleep 10
docker compose up -d
```

### Makefile Commands

```bash
make help           # Hiển thị tất cả commands
make all-up         # Chạy tất cả services
make all-down       # Dừng tất cả services
make logs           # Xem logs tất cả services
make clean          # Dọn dẹp containers và volumes
make rebuild        # Rebuild tất cả services
```

---

## Monitoring

### Prometheus Metrics

Truy cập: http://localhost:9090

Metrics endpoints có sẵn trên mỗi service:
- `/metrics` - Auth Service (port 8003)
- `/metrics` - Clinic Service (port 8001)
- `/metrics` - Booking Service (port 8002)

### Grafana Dashboards

Truy cập: http://localhost:3000

Default credentials: `admin` / `admin`

Dashboards có sẵn:
- Service Health Overview
- Request Rate
- Error Rate
- Response Time

### Cấu hình Prometheus

Xem file: `prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'auth-service'
    static_configs:
      - targets: ['auth-service:8003']
  - job_name: 'clinic-service'
    static_configs:
      - targets: ['clinic-service:8001']
  - job_name: 'booking-service'
    static_configs:
      - targets: ['booking-service:8002']
```

---

## Troubleshooting

### Lỗi thường gặp

#### 1. Container không start

```bash
# Xem logs chi tiết
docker compose logs [service-name]

# Ví dụ
docker compose logs auth-service

# Restart service
docker compose restart [service-name]
docker compose restart auth-service
```

#### 2. Database connection failed

```bash
# Kiểm tra postgres
docker compose ps postgres

# Xem logs postgres
docker compose logs postgres

# Restart postgres
docker compose restart postgres
```

#### 3. Frontend không load

```bash
# Rebuild frontend
docker compose up -d --build frontend
```

#### 4. Lỗi 422 khi gọi API

- Kiểm tra request body format
- Verify authentication token
- Xem logs của service tương ứng

#### 5. Lỗi CORS

```bash
# Kiểm tra CORS_ORIGINS trong .env
# Đảm bảo origin của bạn có trong danh sách
CORS_ORIGINS=http://localhost:3000,http://localhost
```

### Reset Database

```bash
# Xóa volumes và recreate
docker compose down -v

# Restart
docker compose up -d
```

### Kiểm tra Health

```bash
# Tất cả containers
docker compose ps

# Health check tất cả services
for port in 8000 8001 8002 8003 8004; do
  echo "Checking port $port..."
  curl -s http://localhost:$port/health || echo "FAILED"
done
```

---

## Đóng góp

### Quy trình đóng góp

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add some feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Tạo Pull Request

### Coding Standards

- Code Python tuân thủ PEP 8
- Sử dụng type hints
- Viết docstrings cho functions
- ESLint cho JavaScript/Vue
- Prettier cho code formatting

### Testing

```bash
# Backend tests
cd services/[service-name]
pytest

# Frontend tests
cd frontend
npm run test
```

---

## License

MIT License - Clinic Search Project

Copyright (c) 2024 Clinic Home Visit System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Liên hệ

- Email: contact@clinic-search.com
- GitHub Issues: https://github.com/your-repo/clinic-home-visit-system/issues

## Changelog

### v1.0.0 (2024)
- Initial release
- Basic clinic search functionality
- Booking system
- User authentication
- Admin dashboard
- Review system
