## Plan for lab 3

### 1. Cài đặt các thư viện OpenCV, Matplotlib ,Numpy, Skimage
- **Subtask:** Initialize venv
- **Commands:**
    - Initialize venv (CachyOS/Arch Linux/Linux Systems):
        - `python -m venv .venv`
        - `source .venv/bin/activate.fish` (For fish terminal)
        - `source .venv/bin/activate` (For bashbash terminal)
    - Install libraries:`pip install opencv-python`
                        `pip install matplotlin`
                        `pip install numpy`
                        `pip install ski-image`
### 2.Yêu cầu bài lab


**II. Bài Tập Thực Hành**

**1. Thực hiện Canny bằng các thư viện**

- OpenCV (cv2.Canny): Chuyển ảnh đầu vào về ảnh xám (Grayscale), sau đó áp dụng trực tiếp hàm Canny với $T_{low}$ và $T_{high}$.

- Scikit-image (skimage.feature.canny): Chuẩn hóa giá trị điểm ảnh về khoảng $[0.0, 1.0]$, sau đó gọi hàm Canny với các tham số sigma, low_threshold, high_threshold.

**2. Thay đổi tham số & Quan sát kết quả**

Thực hiện chạy thử nghiệm với các bộ tham số khác nhau:

- Bộ 1 (Mặc định): $\sigma = 1.0$, $T_{low} = 50$, $T_{high} = 150$
.
- Bộ 2 (Tăng Sigma): Tăng $\sigma = 3.0$ để thấy nét cạnh bị đứt đoạn và đẫm mờ ra sao.

- Bộ 3 (Tăng Ngưỡng): Tăng $T_{high} = 200$ để quan sát việc các chi tiết phụ biến mất.Hiển thị tất cả kết quả lên cùng một lưới đồ thị (Subplots) để đưa ra nhận xét trực quan.

**3. Áp dụng Canny cho các loại ảnh khác nhau**

- Ảnh nhiều nhiễu: Thêm nhiễu Gaussian hoặc Nhiễu muối tiêu vào ảnh gốc $\rightarrow$ Quan sát thấy Canny vẫn giữ được khung biên tốt hơn hẳn các toán tử khác nhờ bước lọc Gaussian đầu tiên.

- Ảnh độ tương phản thấp: Cần áp dụng kỹ thuật cân bằng bàng màu (Histogram Equalization) trước khi đưa vào Canny để tránh mất cạnh.

- Ảnh nhiều chi tiết nhỏ: Cần giảm $\sigma$ và hạ ngưỡng $T_{low}$ để thu được đầy đủ các đường nét mảnh.

**4.Kết hợp Canny với các kỹ thuật khác**

- Kết hợp nhận dạng hình dạng (Contour & Shape Detection): Dùng Canny để trích xuất biên $\rightarrow$ Áp dụng hàm tìm đường viền (findContours) và biến đổi Hough (HoughLines/HoughCircles) để phát hiện các hình dạng hình học (hình tròn, đường thẳng, hình chữ nhật).

## 3. Phân công thành viên 

| Thành viên | | Hạng mục công việc đảm nhận | Trạng thái |
| :--- | :--- | :--- | :--- |
| **Trần Thị Minh Thùy** | | - **1 Thực hiện Canny bằng các thư viện :**  | `Hoàn thành` |
| **Khuất Trọng Thuận** | |- **2,4.Thay đổi tham số & Quan sát kết quả & Áp dụng Canny cho các loại ảnh khác nhau :**| `Hoàn thành` |
| **Hoàng Phạm Minh Tiến** |  | <br> - **3.Áp dụng Canny cho các loại ảnh khác nhau :**| `Hoàn thành` |