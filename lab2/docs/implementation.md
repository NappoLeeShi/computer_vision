# IMPLEMENTATION FOR LAB 2

# DIRECTORY TREE
```
.
├── datatest
│   └── test.jpg
├── lab2
│   ├── outputs
│   ├── docs
│   │   ├── implementation.md
│   │   └── plan.md
│   │   └── evidence.md
│   ├── main.ipynb
```
## 1. Môi trường & Thư viện sử dụng
- **Ngôn ngữ:** Python 3.x (Triển khai trên Jupyter Notebook / File `.py`).
- **Thư viện chính:**
  - `opencv-python` (`cv2`): Đọc/ghi ảnh, chuyển đổi màu BGR $\rightarrow$ RGB, thực hiện các hàm lọc built-in (`cv2.GaussianBlur`, `cv2.medianBlur`, `cv2.bilateralFilter`).
  - `numpy`: Thao tác mảng 2D/3D, biến đổi điểm ảnh, xử lý tràn số (`np.clip`), khởi tạo ma trận Kernel tùy chỉnh.
  - `matplotlib.pyplot`: Trực quan hóa và so sánh kết quả các bộ lọc trên cùng một khung hình.

---

## 2. Chi tiết Triển khai Thuật toán

### I. Toán Tử Điểm Ảnh (Point Operations)
Xử lý trực tiếp trên từng điểm ảnh $I(x, y)$ độc lập mà không phụ thuộc vào các điểm lân cận:

1. **Thay đổi độ sáng:**
   - **Nguyên lý:** Cộng hoặc trừ hằng số $c$ vào mọi điểm ảnh: $I_{out}(x, y) = I_{in}(x, y) \pm c$.
   - **Cài đặt:** Ép kiểu mảng về `float32` để cộng/trừ, sau đó dùng `np.clip(0, 255)` để tránh hiện tượng tràn số (overflow/underflow) rồi ép lại `uint8`.

2. **Thay đổi độ tương phản:**
   - **Nguyên lý:** Nhân mọi điểm ảnh với hệ số $\alpha > 0$: $I_{out}(x, y) = \alpha \cdot I_{in}(x, y)$.
   - **Cài đặt:** Khi $\alpha > 1$ làm tăng độ tương phản (vùng sáng sáng hơn, vùng tối tối hơn); khi $0 < \alpha < 1$ làm giảm độ tương phản. Xử lý giới hạn khoảng $[0, 255]$ bằng `np.clip`.

3. **Biến đổi âm bản (Image Inversion):**
   - **Nguyên lý:** Đảo ngược giá trị cường độ sáng: $I_{out}(x, y) = 255 - I_{in}(x, y)$.
   - **Cài đặt:** Áp dụng cho ảnh xám hoặc thực hiện đồng thời trên cả 3 kênh màu RGB để tạo ảnh âm bản.

4. **Cắt ngưỡng nhị phân (Thresholding):**
   - **Nguyên lý:** So sánh từng điểm ảnh với ngưỡng $T$:
     $$I_{out}(x, y) = \begin{cases} 255 & \text{nếu } I_{in}(x, y) \ge T \\ 0 & \text{nếu } I_{in}(x, y) < T \end{cases}$$
   - **Cài đặt:** Chuyển ảnh về ảnh xám trước khi cắt ngưỡng để thu được ảnh nhị phân (đen/trắng).

---

### II. Lọc Tuyến Tính (Linear Filtering)
Sử dụng ma trận Kernel $K$ kích thước $N \times N$ thực hiện phép nhân chập 2D (Convolution) trên vùng không gian lân cận của từng điểm ảnh:

1. **Lọc trung bình (Mean Filter):**
   - **Nguyên lý:** Thay thế điểm ảnh trung tâm bằng trung bình cộng các điểm ảnh trong vùng lân cận.
   - **Cài đặt:** Khởi tạo ma trận Kernel kích thước $k \times k$ (VD: $3 \times 3$ hoặc $5 \times 5$) với tất cả các phần tử bằng $\frac{1}{k^2}$.

2. **Lọc Gaussian (Gaussian Blur):**
   - **Nguyên lý:** Sử dụng phân bố chuẩn 2D để gán trọng số cho các điểm lân cận (điểm càng gần trung tâm trọng số càng lớn):
     $$G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2 + y^2}{2\sigma^2}}$$
   - **Cài đặt:** Triển khai qua `cv2.GaussianBlur()` với kích thước Kernel và độ lệch chuẩn $\sigma$ tùy chỉnh để làm mờ tự nhiên.

3. **Làm sắc nét ảnh (Sharpening):**
   - **Nguyên lý:** Sử dụng toán tử Laplacian (đạo hàm bậc 2) hoặc Unsharp Masking để khuếch đại sự chênh lệch độ sáng ở các biên cạnh.
   - **Cài đặt:** Nhân chập ảnh với ma trận Kernel sắc nét (VD: trung tâm $= 5$, 4 điểm lân cận $= -1$) hoặc lấy ảnh gốc cộng với phần chi tiết tần số cao.

---

### III. Bài Tập Nâng Cao (Advanced Tasks)

1. **Phát hiện cạnh (Sobel & Prewitt):**
   - **Sobel:** Dùng 2 ma trận Kernel $G_x$ (đạo hàm ngang) và $G_y$ (đạo hàm dọc) có trọng số làm mịn ở hàng/cột giữa. Tính biên độ độ sáng $G = \sqrt{G_x^2 + G_y^2}$.
   - **Prewitt:** Tương tự Sobel nhưng không áp dụng trọng số Gaussian ở hàng/cột giữa (tất cả hệ số biên bằng $1$ hoặc $-1$).

2. **Tự thiết kế Kernel tùy chỉnh:**
   - **Motion Blur:** Khởi tạo ma trận $N \times N$, gán hàng giữa bằng $1/N$ để tạo hiệu ứng mờ chuyển động ngang.
   - **Emboss (Dập nổi):** Thiết kế Kernel đối xứng lệch pha (VD: đường chéo trên âm, đường chéo dưới dương) để tạo hiệu ứng nổi 3D.
   - **Super Sharpen:** Sử dụng Kernel Laplacian $3 \times 3$ có điểm trung tâm bằng $9$ và 8 điểm lân cận bằng $-1$.

3. **So sánh các loại lọc:**
   - **Phương pháp:** Đưa cùng một bức ảnh gốc qua các bộ lọc: Mean, Gaussian, Sharpening, Sobel, Prewitt, Median và Bilateral.
   - **Trực quan hóa:** Dùng `matplotlib` hiển thị hình ảnh kết quả dưới dạng lưới (Grid Subplots) kèm nhãn tiêu đề rõ ràng để so sánh mức độ làm mịn, giữ biên và độ nét.

4. **Áp dụng lọc phi tuyến tính (Non-linear Filtering):**
   - **Lọc trung vị (Median Filter):** Lấy giá trị trung vị (Median) của vùng lân cận để thay thế cho điểm ảnh trung tâm. Cực kỳ hiệu quả trong việc loại bỏ **nhiễu muối tiêu (salt-and-pepper)** mà không làm mờ biên cạnh.
   - **Lọc song phương (Bilateral Filter):** Kết hợp giữa khoảng cách không gian (Spatial domain) và sự chênh lệch cường độ màu (Radiometric domain). Giúp **làm mịn vùng đồng chất nhưng giữ nguyên độ sắc nét của các đường biên cạnh**.