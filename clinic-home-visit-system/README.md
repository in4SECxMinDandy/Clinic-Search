# Clinic Home Visit System

Hệ thống Quản lý và Đặt lịch Phòng khám - Hỗ trợ Khám bệnh tại Nhà. Được xây dựng với kiến trúc Microservices xử lý hiệu năng cao, kết hợp giao diện Vue.js 3 hiện đại.

## Mục lục
- [Mô tả dự án](#mô-tả-dự-án)
- [Tính năng](#tính-năng)
- [Kiến trúc](#kiến-trúc)
- [Cài đặt](#cài-đặt)
- [Chạy ứng dụng](#chạy-ứng-dụng)
- [API Endpoints](#api-endpoints)
- [Phân quyền người dùng](#phân-quyền-người-dùng)
- [Cấu trúc project](#cấu-trúc-project)

## Mô tả dự án
Hệ thống kết nối bệnh nhân với các phòng khám, cung cấp khả năng tìm kiếm phòng khám gần nhất thông qua tọa độ GPS, xử lý quy trình đặt lịch khám trực tiếp hoặc yêu cầu bác sĩ đến khám tại nhà một cách liền mạch.

## Tính năng

### 1. Tìm kiếm Phòng khám (Clinic Search)
- Tìm kiếm phòng khám theo vị trí GPS
- Lọc theo bán kính (km)
- Sắp xếp theo khoảng cách
- Xem chi tiết thông tin phòng khám

### 2. Hệ thống Đặt lịch (Booking)
- Đặt lịch khám tại phòng khám (Clinic Visit)
- Đặt lịch khám tại nhà (Home Visit)
- Quản lý trạng thái: Chờ xác nhận → Đã xác nhận → Đã hoàn thành / Đã hủy
- Chủ phòng khám duyệt/từ chối yêu cầu đặt lịch

### 3. Hệ thống Review
- Đánh giá bằng sao (1-5 sao)
- Nhận xét chi tiết sau khi hoàn thành khám
- Xem đánh giá trung bình của phòng khám

### 4. Thông báo (Notifications)
- Thông báo thời gian thực
- Cập nhật trạng thái đặt lịch
- Thông báo cho bệnh nhân và chủ phòng khám

### 5. Phân quyền Dashboard

#### Admin Dashboard
- Quản lý tài khoản người dùng
- Quản lý chủ phòng khám
- Quản lý phòng khám
- Quản lý bác sĩ
- Xem thống kê hệ thống

#### Owner Dashboard (Chủ Phòng khám)
- Quản lý cơ sở phòng khám
- Quản lý bác sĩ trong phòng khám
- Duyệt/từ chối yêu cầu đặt lịch
- Xem lịch hẹn của phòng khám

## Kiến trúc

### Microservices
```
clinic-home-visit-system/
├── services/
│   ├── api-gateway/           # Port 8000 - Điều hướng API
│   ├── auth-service/         # Port 8003 - Xác thực & Ủy quyền
│   ├── clinic-service/       # Port 8001 - Quản lý phòng khám
│   ├── booking-service/      # Port 8002 - Quản lý đặt lịch
│   ├── review-service/       # Port 8004 - Đánh giá & Review
│   ├── notification-service/ # Port 8005 - Thông báo
│   └── data-collector/       # Port 8006 - Thu thập dữ liệu GPS
├── frontend/                  # Vue.js 3 Frontend
├── shared/                    # Shared modules
├── traefik/                   # Reverse Proxy & Load Balancer
└── scripts/                  # Database seeding scripts
```

### Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Vue.js 3, Vite, TailwindCSS, Pinia |
| Backend | Python 3.11+, FastAPI, SQLAlchemy |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| Gateway | Traefik 3.0 |
| Monitoring | Prometheus, Grafana |
| Container | Docker Compose |

## Cài đặt

### Yêu cầu
- Docker Desktop (khuyến nghị 4GB+ RAM)
- Docker Compose
- Git

### 1. Clone Repository
```bash
git clone https://github.com/your-repo/clinic-home-visit-system.git
cd clinic-home-visit-system
```

### 2. Cấu hình Environment
Tạo file `.env` trong thư mục gốc (nếu cần):
```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=clinic_system

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost

# Debug
DEBUG=true
```

### 3. Khởi tạo Database
```bash
# Chạy script seed để tạo dữ liệu mẫu
docker compose exec postgres psql -U postgres -d clinic_system -f /scripts/seed_data.sql
```

## Chạy ứng dụng

### Cách 1: Docker Compose (Khuyến nghị)
```bash
# Build và chạy tất cả services
docker compose up -d --build

# Xem logs
docker compose logs -f

# Dừng services
docker compose down
```

### Cách 2: Chạy từng service (Development)

#### Backend Services
```bash
cd services/booking-service
docker build -t booking-service . && docker run -p 8002:8002 booking-service

# Hoặc sử dụng Makefile (nếu có)
make booking-up
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
docker ps

# Kiểm tra health của service
curl http://localhost:8000/health
curl http://localhost:8002/health
curl http://localhost:8001/health
```

### Truy cập Ứng dụng
- **Frontend**: http://localhost (qua Traefik)
- **API Gateway**: http://localhost:8000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Traefik Dashboard**: http://localhost:8080/dashboard/

## API Endpoints

### Authentication
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/v1/auth/register` | Đăng ký tài khoản |
| POST | `/api/v1/auth/login` | Đăng nhập |
| POST | `/api/v1/auth/refresh` | Làm mới token |
| GET | `/api/v1/users/me` | Thông tin user hiện tại |

### Clinics
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/clinics` | Tìm kiếm phòng khám (theo GPS) |
| GET | `/api/v1/clinics/{id}` | Chi tiết phòng khám |
| GET | `/api/v1/clinics/owner/my-clinics` | Danh sách phòng khám của chủ sở hữu |

### Bookings
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/v1/bookings` | Tạo đặt lịch mới |
| GET | `/api/v1/bookings` | Danh sách đặt lịch của user |
| GET | `/api/v1/bookings/clinic/owner/all` | Danh sách đặt lịch (chủ PK) |
| PUT | `/api/v1/bookings/{id}/status` | Cập nhật trạng thái |
| PUT | `/api/v1/bookings/clinic/{clinic_id}/owner/update-status/{booking_id}` | Chủ PK duyệt/từ chối |

### Reviews
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/v1/reviews` | Tạo đánh giá |
| GET | `/api/v1/reviews/clinic/{clinic_id}` | Đánh giá theo phòng khám |

### Doctors
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/v1/doctors` | Danh sách bác sĩ |
| GET | `/api/v1/doctors/clinic/{clinic_id}` | Bác sĩ theo phòng khám |

## Phân quyền người dùng

### Vai trò (Roles)
| Role | Mô tả |
|------|-------|
| `admin` | Quản trị viên hệ thống |
| `clinic_owner` | Chủ phòng khám |
| `doctor` | Bác sĩ |
| `patient` | Bệnh nhân |
| `collector` | Người thu thập dữ liệu |

### Quyền hạn
| Chức năng | Admin | Owner | Doctor | Patient | Collector |
|-----------|-------|-------|--------|---------|-----------|
| Quản lý users | ✅ | ❌ | ❌ | ❌ | ❌ |
| Quản lý phòng khám | ✅ | ✅ (sở hữu) | ❌ | ❌ | ❌ |
| Duyệt đặt lịch | ✅ | ✅ (sở hữu) | ❌ | ❌ | ❌ |
| Tạo đặt lịch | ✅ | ❌ | ❌ | ✅ | ❌ |
| Tạo review | ✅ | ❌ | ❌ | ✅ | ❌ |
| Thu thập GPS | ✅ | ❌ | ❌ | ❌ | ✅ |

## Scripts

### Database Seeding
```bash
# Seed admin user
docker compose exec postgres psql -U postgres -d clinic_system -f scripts/seed_admin.sql

# Seed clinic data
docker compose exec postgres psql -U postgres -d clinic_system -f scripts/seed_clinics.sql

# Seed full demo data
docker compose exec postgres psql -U postgres -d clinic_system -f scripts/seed_demo.sql
```

### Makefile Commands
```bash
make help           # Hiển thị tất cả commands
make all-up         # Chạy tất cả services
make all-down       # Dừng tất cả services
make booking-up     # Chạy booking service
make clinic-up      # Chạy clinic service
make logs           # Xem logs tất cả services
make clean          # Dọn dẹp containers và volumes
```

## Monitoring

### Prometheus Metrics
- Truy cập: http://localhost:9090
- Metrics endpoints: `/-/metrics` trên mỗi service

### Grafana Dashboards
- Truy cập: http://localhost:3000
- Default credentials: `admin` / `admin`

## Troubleshooting

### Lỗi thường gặp

#### 1. Container không start
```bash
# Xem logs chi tiết
docker compose logs [service-name]

# Restart service
docker compose restart [service-name]
```

#### 2. Database connection failed
```bash
# Kiểm tra postgres
docker compose ps postgres

# Restart postgres
docker compose restart postgres
```

#### 3. Frontend không load
```bash
# Rebuild frontend
docker compose up -d --build frontend
```

### Reset Database
```bash
# Xóa volumes và recreate
docker compose down -v
docker compose up -d
```

## License
MIT License - Clinic Search Project
