# PLAN FOR LAB 1

## 1. OBJECTIVE
Củng cố kỹ năng cơ bản trong việc dùng các thư viện opencv/pillow.

## 2. REQUIREMENTS
- **Language:** Python 3.X
- **Libraries:**
    - OpenCV (`opencv-python`)
    - Pillow (`PIL`)
    - Matplotlib
    - Numpy

## 3. TASK BREAKDOWN
1. Cài đặt các thư viện OpenCV và Pillow
- **Subtask:** Initialize venv
- **Commands:**
    - Initialize venv (CachyOS/Arch Linux/Linux Systems):
        - `python -m venv .venv`
        - `source .venv/bin/activate.fish` (For fish terminal)
        - `source .venv/bin/activate` (For bashbash terminal)
    - Install libraries:`pip install opencv-python pillow`

2. Đọc và hiển thị ảnh:
- Đọc một hình ảnh bất kỳ từ máy tính.
- Hiển thị hình ảnh đó lên màn hình.
- Lưu hình ảnh đã xử lý lại với định dạng khác.

3. Chuyển đổi không gian màu:
- Chuyển đổi ảnh từ RGB sang grayscale.
- Chuyển đổi ảnh sang các không gian màu khác như HSV, LAB.

4. Cắt xén và thay đổi kích thước: <br>
- Cắt một vùng hình ảnh bất kỳ. <br>
- Thay đổi kích thước hình ảnh theo tỷ lệ hoặc kích thước cố định.

5. Vẽ hình cơ bản:
- Vẽ các hình cơ bản như đường thẳng, hình tròn, hình chữ nhật lên hình ảnh.
- Thêm văn bản vào hình ảnh.

## 4. Checklist tiến độ
- [X] Task 1: Môi trường & Dataset ảnh
- [ ] Task 2: Read / Display / Save Image
- [ ] Task 3: Color space conversions
- [ ] Task 4: Crop & Resize
- [ ] Task 5: Draw shapes & Text annotation