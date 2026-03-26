# Clinic Home Visit System

Hệ thống Quản lý và Đặt lịch Phòng khám - Hỗ trợ Khám bệnh tại Nhà. Được xây dựng với kiến trúc Microservices xử lý hiệu năng cao, kết hợp giao diện Vue.js 3 hiện đại.

## Mô tả dự án
Hệ thống kết nối bệnh nhân với các phòng khám, cung cấp khả năng tìm kiếm phòng khám gần nhất thông qua tọa độ GPS, xử lý quy trình đặt lịch khám trực tiếp hoặc yêu cầu bác sĩ đến khám tại nhà một cách liền mạch.

## Các chức năng chính (Cập nhật mới)

### 1. Phân quyền và Dashboards (MỚI ✨)
Hệ thống đã đập đi xây lại giao diện và luồng router để hỗ trợ hệ thống phân quyền (RBAC) chi tiết, đi kèm với các dashboard chuyên biệt:
- **Quản trị viên (Admin Dashboard)**: Quyền kiểm soát toàn diện hệ thống.
  - Quản lý tài khoản người dùng (`AdminUsersView`).
  - Quản lý chủ phòng khám (`AdminClinicOwnersView`).
  - Quản lý phòng khám (`AdminClinicsView`) và danh sách y bác sĩ (`AdminDoctorsView`) tổng.
- **Chủ phòng khám (Owner Dashboard)**: Cổng thông tin dành riêng cho đối tác y tế.
  - Quản lý các cơ sở phòng khám do mình sở hữu (`OwnerClinicsView`).
  - Phân bổ và quản lý đội ngũ y bác sĩ tại các cơ sở (`OwnerDoctorsView`).

### 2. Dịch vụ thu thập dữ liệu - Data Collector Service (MỚI ✨)
- Triển khai thêm một vi dịch vụ (Microservice) hoàn toàn mới tại port `8006`.
- Tích hợp công cụ `hotosm_client` chuyên biệt giúp thu thập, đồng bộ dữ liệu bản đồ mở, định vị GPS một cách nhanh chóng định kỳ.

### 3. Công cụ Seeding & Chuẩn hóa Dữ liệu (MỚI ✨)
Các công cụ kịch bản (scripts) mới để tăng tốc quá trình triển khai dự án:
- `seed_admin_user.py`: Khởi tạo tài khoản cấp phát Admin một cách nhanh chóng.
- `seed_fake_data.sql`: Nạp một lượng lớn Mock Data về phòng khám, bác sĩ, và các user có sẵn.
- `fix_doctor_names_vietnamese.py`: Chuẩn hóa ngôn ngữ và tên riêng của người Việt Nam trong CSDL.

### 4. Tính năng Cốt lõi sẵn có
- **Clinic Search**: Thuật toán tìm kiếm sử dụng khoảng cách GPS mạnh mẽ.
- **Hệ thống đặt lịch (Booking)**: Đặt lịch khám tại Clinic hoặc Home Visit (tại nhà).
- **Hệ thống Review**: Đánh giá bằng sao và nhận xét chi tiết sau khi hoàn thành khám.
- **Bảo mật**: Xác thực chuẩn JWT lưu trong HttpOnly Cookies.
- **Thông báo**: Microservice phát và lắng nghe thông báo thời gian thực.

## Tech Stack
- **Backend (Microservices)**: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL, Redis
- **Frontend**: Vue.js 3, Vite, TailwindCSS, Vue Router, Pinia
- **Infrastructure**: Docker Compose, Traefik (API Gateway), Prometheus & Grafana

## Kiến trúc Dịch vụ
Dự án được chia làm những service độc lập sau:
```text
services/
├── api-gateway/         # Port 8000
├── clinic-service/      # Port 8001
├── booking-service/     # Port 8002
├── auth-service/        # Port 8003
├── review-service/      # Port 8004
├── notification-service/# Port 8005
└── data-collector/      # Port 8006
```

## Quy chuẩn Dự án
- **CSDL**: Các dịch vụ sử dụng chung PostgreSQL với schema tách biệt theo khái niệm "multi-schema".
- **Giao tiếp liên dịch vụ**: Xử lý bất đồng bộ, event-driven thông qua Redis Pub/Sub.
- Tọa độ GPS quy định chuẩn hóa thành lat/lng (Latitude/Longitude).
