---
name: tiep
description: Reads the pinned agent transcript for the clinic home-visit project and resumes that work session. Use when the user invokes /Tiếp, says "tiếp tục phiên làm việc", or asks to continue the previous session tied to transcript 4366d683-c337-43ab-abde-608376c3527e.
---

# /Tiếp — Tiếp tục phiên làm việc

## Mục đích

Khôi phục ngữ cảnh từ transcript phiên trước và tiếp tục công việc dở (Docker, microservices, frontend `clinic-home-visit-system`) thay vì bắt đầu lại từ đầu.

## Transcript cố định

**Luôn đọc file transcript này trước** (dùng công cụ Read):

`c:/Users/haqua/.cursor/projects/c-Users-haqua-OneDrive-Desktop-BigProject-Python/agent-transcripts/4366d683-c337-43ab-abde-608376c3527e/4366d683-c337-43ab-abde-608376c3527e.jsonl`

Nếu file không tồn tại hoặc trống, báo rõ và hỏi người dùng đường dẫn transcript mới.

## Quy trình

1. **Đọc transcript** — Trích các quyết định đã làm, lệnh đã chạy, và phần còn dở hoặc lỗi cuối cùng.
2. **Tóm tắt ngắn** — 3–6 gạch đầu dòng: đã xong gì, đang kẹt ở đâu (nếu có), bước hợp lý tiếp theo.
3. **Tiếp tục** — Thực hiện bước tiếp theo trong workspace `clinic-home-visit-system` (không mở rộng sang dự án khác trừ khi user yêu cầu).
4. **Khớp phong cách** — Giữ tiếng Việt nếu user đang dùng tiếng Việt; chạy lệnh và sửa code trực tiếp, không chỉ hướng dẫn chung.

## Bối cảnh đã biết từ phiên transcript (tóm tắt)

Dùng như gợi ý nhanh; **ưu tiên nội dung thực tế trong file `.jsonl`** nếu khác.

- Dự án: **clinic-home-visit-system** (microservices, Docker, frontend Vue).
- Đã xử lý: lỗi frontend (file/style/view thiếu), biến môi trường/schema/port backend, Dockerfile (kể cả data-collector), copy `shared`, `docker-compose` build context, import/path trong container, tên thư mục service có dấu gạch và Python package.
- Hướng tiếp theo thường gặp: kiểm tra **cảnh báo bảo mật image Docker** (Docker DX / quét CVE), rebuild sau khi đổi base image hoặc pin phiên bản, và xác nhận toàn bộ service chạy ổn định.

## Ghi chú

- Không nhúng toàn bộ transcript vào reply; chỉ trích đoạn cần thiết khi giải thích.
- Nếu user muốn đổi transcript sang phiên khác, cập nhật đường dẫn trong mục "Transcript cố định" ở trên trong `SKILL.md`.
