# IMPLEMENTATION FOR LAB 1

# 1. DIRECTORY TREE
```
.
├── datatest
│   └── test.jpg
├── lab1
│   ├── outputs
│   ├── docs
│   │   ├── implementation.md
│   │   └── plan.md
│   ├── main.ipynb
│   └── main.py
```

## Directory explanation:
1. Main directory contains:
- Images for testing: `datatest`
- Lab folder: `lab1`
2. Lab folder contains:
- Image operation outputs: `outputs`
- Documentation/Workflow: `docs`
- Main code: `main.ipynb`/`main.py`

# 2. DETAILED IMPLEMENTATION (FUNCTIONS, LIBRARIES) 
1. Cài đặt các thư viện OpenCV và Pillow\
No programming in this assignment.
2. Đọc và hiển thị ảnh:
- Đọc một hình ảnh bất kỳ từ máy tính.
    - CV2: `img = cv2.imread(/path/to/img.jpg/)`
    - Pillow: `img = img.open(/path/to/img/jpg)`
- Hiển thị hình ảnh đó lên màn hình.
    - CV2: `cv2.imshow(name, img)`
    - Pillow: `img.show()`
- Lưu hình ảnh đã xử lý lại với định dạng khác.
    - CV2: `cv2.imwrite(new_suffix, img)`
    - Pillow: `img.save(new_suffix_full_path)`

3. Chuyển đổi không gian màu:
- Chuyển đổi ảnh từ RGB sang grayscale.
    - CV2: `gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
    - Pillow: `gray_img = ImageOps.grayscale(img)`
- Chuyển đổi ảnh sang các không gian màu khác như HSV, LAB.
    - CV2:
        - HSV: `hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)`
        - LAB: `lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)`
    - Pillow
        - HSV: `pil_hsv = np.array(pil_img.convert("HSV"))`
        - LAB: Use `ImageCms.buildTransform` and `ImageCms.applyTransform`

4. Cắt xén và thay đổi kích thước:
- Cắt một vùng hình ảnh bất kỳ.
    - CV2: `cropped_img = img[from_y:to_y, from_x:to_x]`
    - Pillow: `img.crop((left, upper, right, lower))`
- Thay đổi kích thước hình ảnh theo tỷ lệ hoặc kích thước cố định.
    - CV2:
        - Ratio: `resized_ratio = cv2.resize(img, dsize = (0, 0), fx=ratio_x, fy=ratio_y)`
        - Fixed: `resized_fixed = cv2.resize(image, dsize = (x, y))`
    - Pillow:
        - Ratio: `img.resize((int(ratio_x*w), int(ratio_y*h)))`
        - Fixed: `pil_resize_ratio = pil_img.resize(size=(x, y))`


5. Vẽ hình cơ bản:
- Vẽ các hình cơ bản như đường thẳng, hình tròn, hình chữ nhật lên hình ảnh.
    - CV2:
        - Line: `cv2.line(drawing_image, (start_x, start_y), (end_x, end_y), (b, g, r), thickness)`
        - Rectangle: `cv2.rectangle(drawing_image, (start_x, start_y), (end_x, end_y), (b, g, r), thickness)`
        - Circle: `cv2.circle(drawing_image, (pos_x, pos_y), rad, (b, g, r), thickness)`
    - Pillow:
        - Line: ` ImageDraw.line(xy, fill=None, width=0, joint=None)`
        - Rectangle: `ImageDraw.rectangle(xy, fill=None, outline=None, width=1)`
        - Circle: ` ImageDraw.circle(xy, radius, fill=None, outline=None, width=1)`
- Thêm văn bản vào hình ảnh.
    - CV2: `cv2.putText(drawing_image, text, (pos_x, pos_y), cv2.FONT_YOU_WANT, font_scale, (b, g, r), thickness)`
    - Pillow: `ImageDraw.text(xy, text, fill=None, font=None, font_size=None)`
        
# 3. IMPORTANT NOTES
1. All results will be displayed using matplotlib
```python
plt.imshow(img_rgb)
plt.title("Title")
plt.axis('off')
```

To avoid having to repeat this code too many times, a custom function will be created at the start:
```python
def plt_imshow(img: MatLike | Image.Image, title: String | None = None, cmap: String | None = None):
    if isinstance(img, Image.Image):
        plt.imshow(img, cmap=cmap)
    else:
        plt.imshow(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
    
    plt.title(title)
    plt.axis("off")
```

2. Due to cv2 using BGR color format, images shown with matplotlib will first be convered to RGB
    - Command: `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`

3. There is not need to use `cv2.destroyAllWindows()` because of note `1.`