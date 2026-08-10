## Plan for lab 2
### 1. Cài đặt các thư viện OpenCV, Matplotlib và Numpy
- **Subtask:** Initialize venv
- **Commands:**
    - Initialize venv (CachyOS/Arch Linux/Linux Systems):
        - `python -m venv .venv`
        - `source .venv/bin/activate.fish` (For fish terminal)
        - `source .venv/bin/activate` (For bashbash terminal)
    - Install libraries:`pip install opencv-python`
                        `pip install matplotlin`
                        `pip install numpy`
### 2.Yêu cầu bài lab
**I. Toán Tử Điểm Ảnh**

1. Thay đổi độ sáng: Cộng hoặc trừ một hằng số cố định vào tất cả giá trị điểm ảnh (pixel) của ảnh gốc để tăng/giảm độ sáng, sau đó ép giá trị nằm trong khoảng $[0, 255]$

2. Thay đổi độ tương phản: Nhân tất cả giá trị điểm ảnh với một hằng số (hệ số tương phản), sau đó giới hạn giá trị trong khoảng $[0, 255]$.

3. Biến đổi âm bản: Đảo ngược màu của từng điểm ảnh bằng cách lấy $255$ trừ đi giá trị điểm ảnh hiện tại (với ảnh xám hoặc cả 3 kênh màu).

4. Cắt ngưỡng (Phân ngưỡng nhị phân): Chọn một giá trị ngưỡng $T$ (threshold); chuyển điểm ảnh thành $255$ (trắng) nếu giá trị $> T$, ngược lại chuyển thành $0$ (đen) để tạo ảnh nhị phân.

**II.Lọc Tuyến Tính**

1. Lọc trung bình (Mean Filter): Tạo ma trận Kernel trung bình (tất cả phần tử bằng $1 / N$) và thực hiện phép nhân chập trên ảnh để làm mờ ảnh nhẹ.

2. Lọc Gaussian: Tạo hoặc gọi bộ lọc Gaussian Kernel để làm mờ ảnh một cách tự nhiên, giảm nhiễu mà vẫn giữ viền mềm hơn lọc trung bình.

3. Làm sắc nét ảnh (Sharpening): Thiết kế/áp dụng ma trận Kernel sắc nét (như Laplacian hoặc kỹ thuật Unsharp Masking) để làm nổi bật các viền cạnh của đối tượng trong ảnh.

**III.Bài Tập Nâng Cao**

1. Phát hiện cạnh: Tạo ma trận Kernel Sobel ($G_x, G_y$) và Prewitt ($G_x, G_y$) theo 2 chiều ngang/dọc, áp dụng nhân chập để trích xuất và hiển thị các đường biên cạnh của ảnh.

2. Tự thiết kế Kernel tùy chỉnh: Tự định nghĩa các ma trận Kernel $3 \times 3$ hoặc $5 \times 5$ khác nhau để tạo ra các hiệu ứng như: mờ chuyển động (Motion Blur), dập nổi (Emboss), hoặc siêu sắc nét (Super Sharpen).

3. So sánh các loại lọc: Đặt ảnh gốc và các ảnh kết quả sau khi qua các bộ lọc (Trung bình, Gaussian, Sắc nét, Sobel,...) nằm cạnh nhau trên cùng một khung hình để nhận xét ưu/nhược điểm từng loại.

4. Áp dụng lọc phi tuyến tính: Triển khai bộ lọc Trung vị (Median Filter) để khử nhiễu muối tiêu và bộ lọc Song phương (Bilateral Filter) để vừa làm mịn ảnh vừa giữ nguyên biên cạnh sắc nét.

## 3. Phân công thành viên 

| Thành viên | | Hạng mục công việc đảm nhận | Trạng thái |
| :--- | :--- | :--- | :--- |
| **Nguyễn Thường Kiệt** | | **Phần I.1,2 Thay đổi độ sáng & Thay đổi độ tương phản:** Cài đặt chức năng Thay đổi độ sáng, Thay đổi độ tương phản, Biến đổi âm bản, Cắt ngưỡng (Thresholding). | `Hoàn thành` |
| **Nguyễn Tăng Thành** |  | - **Phần I.3,4 Biến đổi âm bản & Cắt ngưỡng:** .<br>- **III.1 & III.2:**  và .Biến đổi âm bản, Cắt ngưỡng (Thresholding) | `Hoàn thành` |
| **Hồ Quốc Toản** |  | - **II.1,2 Lọc trung bình (Mean Filter) & Lọc Gaussian :**Cài đặt các bộ lọc Lọc trung bình (Mean Filter), Lọc Gaussian (Gaussian Blur) .<br>- * . | `Hoàn thành` |
| **Nguyễn Minh Thảo** | | - **II.3.Làm sắc nét ảnh (Sharpening) :**| `Hoàn thành` |
| **Trần Thị Minh Thùy** | | - **III.1 Phát hiện cạnh :**Phát hiện cạnh (Sobel, Prewitt)  | `Hoàn thành` |
| **Khuất Trọng Thuận** | | - Quản lý repo, khởi tạo cấu trúc dự án và viết tài liệu (`PLAN.md`, `implementation.md`).<br>- Chuẩn bị ảnh test (`datatest/`), <br> - **III.2,3.Tự thiết kế Kernel tùy chỉnh &  So sánh các loại lọc :**Tự thiết kế Kernel tùy chỉnh,Lập bảng & trực quan hóa so sánh hiệu quả của các bộ lọc trên cùng một bức ảnh| `Hoàn thành` |
| **Hoàng Phạm Minh Tiến** |  | - Quản lý repo, khởi tạo cấu trúc dự án và viết tài liệu (`PLAN.md`, `implemantation.md`).<br>- Chuẩn bị ảnh test (`datatest/`), <br> - **III.4.Áp dụng lọc phi tuyến tính :**Nghiên cứu và cài đặt Lọc trung vị (Median Filter) và Lọc song phương (Bilateral Filter)| `Hoàn thành` |