# Bài thực hành 4
# So sánh sự tương đồng của các hình ảnh sử dụng Wavelet, Python

## I> Mục tiêu bài tập:
- Biết cách sử dụng wavelet biến đổi để trích xuất thông tin cụ thể và so sánh sự tương thích giữa các hình ảnh.
- Làm quen với PyWavelets thư viện và các công cụ xử lý ảnh trong Python.
- Đánh giá kết quả của hàm băm wavelet phương pháp trong việc xác định các hình ảnh tương thích.
## II> Bài toán cụ thể:
1. Chuẩn bị dữ liệu. Chuẩn bị một tập hợp các hình ảnh, bao gồm các hình ảnh cặp đôi tương tự nhau (ví dụ: cùng một đối tượng với các
góc độ khác nhau, các mức độ nhiễu khác nhau) và các hình ảnh cặp không tương tự.

2. Trích xuất wavelet đặc biệt. Sử dụng wavelet biến đổi để chuyển đổi từng hình ảnh thành một wavelet ma trận.

3. Tạo mã băm cho mỗi hình ảnh dựa trên các wavelet số đã lượng tử hóa.

4. So sánh hàm băm. Tính khoảng cách Hamming giữa các mã băm để đánh giá mức độ tương thích giữa các hình ảnh.

5. Đánh giá.
- Độ chính xác: Tỷ lệ tính toán của các cặp hình ảnh được phân loại đúng (tương tự/không tương tự).
- Độ nhạy: Tỷ lệ các cặp hình ảnh tương thích được phân loại đúng.
- Độ đặc biệt: Tỷ lệ tính toán của các cặp hình ảnh không tương thích với loại phân tích đúng.
- Đường cong ROC: Vẽ đường cong ROC để đánh giá hiệu suất của thuật toán.

## III> Bài tập nâng cao:
1. Thực hiện khảo sát về các phương pháp băm wavelet khác nhau và so sánh hiệu suất của chúng.
2. Xây dựng ứng dụng tìm kiếm hình ảnh dựa trên hàm băm wavelet.

# PHÂN CÔNG THÀNH VIÊN
| Thành viên | | Hạng mục công việc đảm nhận | Trạng thái |
| :--- | :--- | :--- | :--- |
| **Khuất Trọng Thuận** |  |**Tạo project structure và prompts cơ bản**| `Hoàn thành` |
| **Hoàng Phạm Minh Tiến** |  |**Implement bằng OpenCode**| `Hoàn thành` |