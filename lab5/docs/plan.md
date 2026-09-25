# Bài thực hành 5
# Nhận dạng khuôn mặt thời gian thực sử dụng FaceNet và MTCNN trên Webcam, Python

## I> Mục tiêu bài tập:
- Biết cách sử dụng MTCNN để phát hiện khuôn mặt trong ảnh và trong khung hình webcam theo thời gian thực.
- Biết cách sử dụng mô hình FaceNet đã huấn luyện sẵn để trích xuất vector đặc trưng (embedding) của khuôn mặt.
- Biết cách so sánh embedding của khuôn mặt webcam với các embedding tham chiếu và áp dụng ngưỡng tương đồng để quyết định "Matched" hay "Unknown".
- Làm quen với việc xử lý video theo thời gian thực bằng thư viện OpenCV.

## II> Bài toán cụ thể:
1. Chuẩn bị dữ liệu. Thu thập ảnh tham chiếu của các người đã biết, lưu theo từng thư mục
   (`data/faces/person_01/`, `data/faces/person_02/`). Đây chỉ là dữ liệu tham chiếu, không phải đầu vào nhận dạng thời gian thực.
2. Mở webcam bằng OpenCV và liên tục lấy khung hình.
3. Phát hiện khuôn mặt trong mỗi khung hình bằng MTCNN.
4. Trích xuất embedding của các khuôn mặt được phát hiện bằng mô hình FaceNet đã huấn luyện sẵn
   (không huấn luyện lại mô hình).
5. So sánh embedding của khuôn mặt trực tiếp với các embedding tham chiếu bằng một đại lượng đo độ tương đồng.
6. Áp dụng ngưỡng tương đồng: similarity > 0.7 → "Matched", similarity < 0.7 → "Unknown". Ngưỡng phải cấu hình được.
7. Hiển thị danh tính và điểm tương đồng trực tiếp trên khung hình webcam.
8. Lặp lại liên tục trong một vòng lặp thời gian thực cho đến khi người dùng thoát ra.

## III> Bài tập nâng cao:
1. Khảo sát ảnh hưởng của ngưỡng tương đồng đến tỉ lệ "Matched"/"Unknown".
2. So sánh hiệu năng thời gian thực (số khung hình mỗi giây) của FaceNet với các backbone khác cho cùng một bài toán.

# PHÂN CÔNG THÀNH VIÊN
| Thành viên | | Hạng mục công việc đảm nhận | Trạng thái |
| :--- | :--- | :--- | :--- |
| **Khuất Trọng Thuận** | |**Tạo project structure và prompts cơ bản**| `Hoàn thành` |
| **Hoàng Phạm Minh Tiến** | |**Implement bằng OpenCode**| `Hoàn Thành` |

## IV> Trạng thái implement:
| Hạng mục | File | Trạng thái |
| :--- | :--- | :--- |
| Phát hiện khuôn mặt bằng MTCNN | `src/face_detector.py` | `Hoàn thành` |
| Trích xuất embedding bằng FaceNet pre-trained | `src/face_embedding.py` | `Hoàn thành` |
| So sánh embedding và áp dụng ngưỡng 0.7 | `src/face_matching.py` | `Hoàn thành` |
| Mở webcam và vòng lặp thời gian thực | `src/webcam.py` | `Hoàn thành` |
| Tích hợp toàn bộ pipeline trên webcam thật | `main.py` | `Hoàn thành` |
| Hướng dẫn cài đặt và chạy ứng dụng | `README.md` | `Hoàn thành` |

**Kết quả kiểm thử trên webcam thật (ACER HD User Facing UVC, 640x480):**
- Ảnh tham chiếu được load đúng 1 lần lúc khởi tạo, không load lại trong vòng lặp.
- 24 khung hình thực tế, phát hiện được 26 khuôn mặt (20 khung 1 mặt, 3 khung 2 mặt, 1 khung không có mặt).
- Mọi khuôn mặt đều được nhận dạng và hiển thị kết quả trực tiếp trên khung hình.
- Ngưỡng 0.7 hoạt động đúng: khuôn mặt đã đăng ký được gán tên (màu xanh), khuôn mặt chưa đăng ký luôn là `Unknown` (màu đỏ), không bị ép vào một danh tính nào.
- Hiệu năng thời gian thực (CPU, không GPU): camera thu được 13.8 FPS, vòng lặp nhận dạng đầy đủ đạt 9.8 FPS ở 640x480.

