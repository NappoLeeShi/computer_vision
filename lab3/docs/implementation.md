# Implementation for lab3

# DIRECTORY TREE
```
.
├── datatest
│   └── test.jpg
├── lab3
│   ├── outputs
│   ├── docs
│   │   ├── implementation.md
│   │   └── plan.md
│   │   └── evidence.md
│   ├── main.ipynb
```

## 1. Môi trường & Thư viện sử dụng
- **Ngôn ngữ:** Python 3.x (Triển khai trên Jupyter Notebook / File `.ipynb`).
- **Thư viện chính:**
  - `opencv-python` (`cv2`): Chuyển đổi màu BGR $\rightarrow$ Grayscale, thực hiện Canny edge detection qua `cv2.Canny()`.
  - `scikit-image` (`skimage.feature.canny`): Thực hiện phát hiện cạnh Canny theo chuẩn float $[0.0, 1.0]$ với bộ lọc Gaussian tích hợp sẵn.
  - `numpy`: Xử lý mảng 2D/3D, chuẩn hóa dữ liệu giữa các thư viện, tạo nhiễu nhân tạo (Gaussian Noise) cho bài kiểm thử.
  - `matplotlib.pyplot`: Vẽ và biểu diễn kết quả so sánh trực quan dưới dạng Subplots.

---

## 2. Chi tiết Triển khai & Phương pháp Kỹ thuật

### I. Lý thuyết & Thuật toán Canny (Canny Edge Detector)

1. **5 Bước cốt lõi trong thuật toán Canny:**
   - **Bước 1 - Giảm nhiễu (Noise Reduction):** Nhúng bộ lọc Gaussian $k \times k$ để làm mịn ảnh, loại bỏ nhiễu tần số cao trước khi tính đạo hàm.
   - **Bước 2 - Tính toán Gradient:** Áp dụng toán tử Sobel theo phương ngang $G_x$ và phương dọc $G_y$. Tính độ lớn Gradient $G = \sqrt{G_x^2 + G_y^2}$ và hướng góc cạnh $\Theta = \arctan(G_y / G_x)$ (quy về 4 hướng chính: $0^\circ, 45^\circ, 90^\circ, 135^\circ$).
   - **Bước 3 - Triệt tiêu cực đại cục bộ (Non-Maximum Suppression - NMS):** Duyệt qua từng điểm ảnh, so sánh độ lớn Gradient với 2 điểm lân cận theo hướng $\Theta$. Nếu không phải cực đại cục bộ, gán giá trị về $0$ để thu được đường biên mảnh 1 pixel.
   - **Bước 4 - Phân ngưỡng kép (Double Thresholding):** Sử dụng 2 ngưỡng: $T_{high}$ và $T_{low}$.
     - Điểm ảnh $> T_{high}$: Cạnh mạnh (Strong Edge).
     - $T_{low} \le \text{Điểm ảnh} \le T_{high}$: Cạnh yếu (Weak Edge).
     - Điểm ảnh $< T_{low}$: Nhiễu $\rightarrow$ Loại bỏ.
   - **Bước 5 - Theo dõi cạnh theo phân vùng (Edge Tracking by Hysteresis):** Giữ lại các cạnh yếu nếu chúng có kết nối trực tiếp với ít nhất một cạnh mạnh trong vùng lân cận $8$ điểm.

2. **Ảnh hưởng của các Tham số:**
   - **Độ lệch chuẩn ($\sigma$ / Sigma):** Điều chỉnh mức độ làm mịn Gaussian. $\sigma$ lớn giúp loại bỏ nhiễu tốt hơn nhưng làm nhòe bớt các chi tiết mảnh; $\sigma$ nhỏ giữ lại đường nét chi tiết nhưng dễ bị ảnh hưởng bởi nhiễu.
   - **Ngưỡng thấp ($T_{low}$) & Ngưỡng cao ($T_{high}$):** Tỷ lệ chọn tối ưu là $1:2$ hoặc $1:3$. Ngưỡng cao xác định khung biên chính, ngưỡng thấp quyết định độ liên tục của các đường biên yếu.

---

### II. Triển khai Bài tập Thực hành

1. **Câu 1: Thực hiện thuật toán Canny bằng các thư viện**
   - **OpenCV (`cv2.Canny`):** Triển khai trực tiếp trên ảnh xám dạng số nguyên `uint8` $[0, 255]$. Nhận trực tiếp hai giá trị ngưỡng số nguyên (`low_threshold`, `high_threshold`).
   - **Scikit-image (`skimage.feature.canny`):** Yêu cầu chuẩn hóa mảng ảnh đầu vào về dạng số thực `float` $[0.0, 1.0]$. Cần chia giá trị ảnh gốc và các ngưỡng $T_{low}, T_{high}$ cho $255.0$ để đảm bảo đúng quy chuẩn dữ liệu.

2. **Câu 2: Thay đổi các tham số và quan sát kết quả**
   - **Thay đổi Sigma ($\sigma$):** Thử nghiệm với các giá trị $\sigma = 0.5, 1.5, 3.0$. Quan sát thấy $\sigma$ càng lớn thì chi tiết mảnh càng bị mờ đi, chỉ còn giữ lại khung biên chính.
   - **Thay đổi Ngưỡng ($T_{low}, T_{high}$):** Khảo sát tỷ lệ $1:2$ và $1:3$. Khi tăng $T_{high}$, các cạnh mờ/phụ biến mất; khi giảm $T_{low}$, xuất hiện thêm nhiều đường biên yếu và vệt nhiễu lặt vặt.
   - **So sánh với mặc định:** Đặt các kết quả thử nghiệm lên cùng một lưới đồ thị Subplots để đưa ra nhận xét định tính so với bộ tham số mặc định ($\sigma = 1.0, T_{low} = 50, T_{high} = 150$).

3. **Câu 3: Áp dụng Canny cho các loại ảnh khác nhau**
   - **Ảnh nhiều nhiễu:** Thêm nhiễu Gaussian bằng `np.random.normal`. Canny xử lý chống nhiễu tốt hơn Sobel/Prewitt nhờ bước lọc mờ Gaussian tích hợp sẵn.
   - **Ảnh độ tương phản thấp:** Tiền xử lý bằng cân bằng bảng màu (Histogram Equalization) trước khi đưa vào Canny để nâng cao độ phân tách giữa viền đối tượng và nền.
   - **Ảnh nhiều chi tiết nhỏ:** Tinh chỉnh giảm $\sigma$ xuống $0.8$ và hạ $T_{low}$ để bắt trọn các đường nét mảnh và nhỏ.
   - **Đánh giá & Kết luận:** Rút ra nhận xét về tính linh hoạt của Canny và tầm quan trọng của việc chọn đúng tham số cho từng loại dữ liệu ảnh.

4. **Câu 4: Kết hợp Canny với các kỹ thuật khác**
   - **Kết hợp thuật toán phân đoạn (Segmentation):** Sử dụng các nét biên khép kín thu được từ Canny làm mặt nạ (Mask) hoặc hạt giống (Seed) để thực hiện phân đoạn tách đối tượng khỏi nền (như thuật toán Watershed hoặc Flood Fill).
   - **Kết hợp nhận dạng hình dạng (Shape Detection):** Trích xuất đường biên bằng Canny $\rightarrow$ Sử dụng hàm tìm đường viền (`cv2.findContours`) và biến đổi Hough (`HoughLines`, `HoughCircles`) để phát hiện, phân loại các hình dạng hình học (hình tròn, đường thẳng, hình chữ nhật) của đối tượng.

---

### III. Trả lời Câu hỏi Mở rộng

1. **Đánh giá chất lượng cạnh phát hiện bởi Canny:**
   - Dựa trên 3 tiêu chí của Canny: **Tỷ lệ báo động giả thấp (Low error rate)**, **Vị trí cạnh chính xác (Localization)** và **Phản hồi duy nhất (Single response)**.
   - So sánh định lượng với mặt nạ biên chuẩn (Ground Truth) qua chỉ số IoU (Intersection over Union) hoặc F1-Score.

2. **Cải thiện hiệu suất thuật toán Canny:**
   - Áp dụng **Adaptive Thresholding** (ngưỡng tự động) dựa trên trung vị (median) của ảnh thay vì cố định hằng số.
   - Thay bộ lọc Gaussian bằng **Bilateral Filter** để làm mịn bề mặt mà giữ nguyên độ sắc nét của biên.
   - Tối ưu hóa tính toán trên GPU để đạt tốc độ xử lý khung hình thời gian thực (Real-time).

3. **Áp dụng Canny cho Ảnh màu:**
   - Chuyển ảnh sang không gian màu HSV hoặc CIELAB.
   - Áp dụng Canny riêng trên từng kênh màu, sau đó lấy giá trị cực đại (Magnitude) hoặc thực hiện phép OR logic để tổng hợp các đường biên lại.

4. **Áp dụng Canny cho Video:**
   - Đọc luồng video theo từng khung hình (Frame-by-frame).
   - Áp dụng Canny trên từng Frame trong vòng lặp kết hợp với kỹ thuật lọc theo thời gian (Temporal Filtering) giữa các Frame liên tiếp để giảm hiện tượng nhấp nháy biên.