# Test case chức năng Đăng nhập

Hệ thống kiểm thử: https://vanphongdientu.utc.edu.vn

## 1. Dữ liệu kiểm thử

| Biến | Ý nghĩa |
|---|---|
| `{VALID_USER}` | Tên đăng nhập hợp lệ (`huongnt`) |
| `{VALID_PASS}` | Mật khẩu hợp lệ, không ghi trong repo, truyền qua biến môi trường |
| `Sai@Pass#9999` | Mật khẩu sai dùng chung cho các test âm |

Cột **Nhóm** cho biết điều kiện chạy:

- **A**: không cần mật khẩu đúng, chạy được ngay.
- **B**: cần tài khoản đúng (biến môi trường `VALID_PASS`), nếu thiếu thì tự bỏ qua.
- **C**: test rủi ro (SQL Injection, XSS, sai nhiều lần có thể khóa tài khoản), mặc định bỏ qua, bật bằng `RUN_RISKY=1`.

## 2. Bảng test case

| STT | ID | Description | Steps | Expected Output | Nhóm | Hàm test |
|---|---|---|---|---|---|---|
| 1 | TC1 | Để trống username, nhập password | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô pass<br>3. Nhập pass là: `Sai@Pass#9999`<br>4. Click vào nút Login | Bạn chưa nhập tên đăng nhập | A | `test_TC1_empty_user` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 2 | TC2 | Nhập username, để trống password | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `{VALID_USER}`<br>4. Click vào nút Login | Bạn chưa nhập mật khẩu | A | `test_TC2_empty_pass` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 3 | TC3 | Đúng tên, sai mật khẩu | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `{VALID_USER}`<br>4. Click vào ô pass<br>5. Nhập pass là: `Sai@Pass#9999`<br>6. Click vào nút Login | Tài khoản không đúng | A | `test_TC3_right_user_wrong_pass` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 4 | TC4 | Sai tên, mật khẩu bất kỳ | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `huongthunguyen`<br>4. Click vào ô pass<br>5. Nhập pass là: `Sai@Pass#9999`<br>6. Click vào nút Login | Tài khoản không đúng | A | `test_TC4_wrong_user` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 5 | TC5 | Đăng nhập thành công và chọn "Giữ tôi luôn đăng nhập" | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `{VALID_USER}`<br>4. Click vào ô pass<br>5. Nhập pass là: `{VALID_PASS}`<br>6. Tích chọn "Giữ tôi luôn đăng nhập"<br>7. Click vào nút Login<br>8. Tắt trình duyệt và mở lại | Đưa vào trang chủ. Sau khi mở lại vẫn ở trang chủ | B | `test_TC5_keep_login` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 6 | TC6 | Đăng nhập thành công và không chọn "Giữ tôi luôn đăng nhập" | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `{VALID_USER}`<br>4. Click vào ô pass<br>5. Nhập pass là: `{VALID_PASS}`<br>6. Click vào nút Login<br>7. Tắt trình duyệt và mở lại | Đưa vào trang chủ. Sau khi mở lại về trang đăng nhập | B | `test_TC6_no_keep_login` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 7 | TC7 | Để trống cả username và password | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào nút Login | Bạn chưa nhập tên đăng nhập | A | `test_TC7_empty_both` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 8 | TC8 | Sai cả tên và mật khẩu | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `abc123`<br>4. Click vào ô pass<br>5. Nhập pass là: `abc@123`<br>6. Click vào nút Login | Tài khoản không đúng | A | `test_TC8_wrong_both` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 9 | TC9 | Đúng tên, mật khẩu đúng nhưng đổi sang chữ hoa (kiểm tra phân biệt hoa/thường) | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `{VALID_USER}`<br>4. Click vào ô pass<br>5. Nhập pass là: `{VALID_PASS}` viết hoa toàn bộ<br>6. Click vào nút Login | Tài khoản không đúng | B | `test_TC9_pass_case_sensitive` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 10 | TC10 | Username viết hoa toàn bộ, mật khẩu đúng | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `{VALID_USER}` viết hoa toàn bộ<br>4. Click vào ô pass<br>5. Nhập pass là: `{VALID_PASS}`<br>6. Click vào nút Login | Đăng nhập thành công, hoặc báo "Tài khoản không đúng" nếu hệ thống phân biệt hoa/thường (ghi lại hành vi thực tế) | B | `test_TC10_username_uppercase` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 11 | TC11 | Username có khoảng trắng ở đầu và cuối, mật khẩu đúng | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `" "` + `{VALID_USER}` + `" "` (có dấu cách hai đầu)<br>4. Click vào ô pass<br>5. Nhập pass là: `{VALID_PASS}`<br>6. Click vào nút Login | Hệ thống tự cắt khoảng trắng và đăng nhập thành công, hoặc báo "Tài khoản không đúng" (ghi lại hành vi thực tế) | B | `test_TC11_username_spaces_around` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 12 | TC12 | Username chỉ nhập khoảng trắng | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập 3 dấu cách<br>4. Click vào ô pass<br>5. Nhập pass là: `Sai@Pass#9999`<br>6. Click vào nút Login | Bạn chưa nhập tên đăng nhập | A | `test_TC12_username_only_spaces` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 13 | TC13 | Username quá dài | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập chuỗi 256 ký tự `a`<br>4. Click vào ô pass<br>5. Nhập pass là: `Sai@Pass#9999`<br>6. Click vào nút Login | Không đăng nhập được; hệ thống giới hạn độ dài hoặc báo "Tài khoản không đúng", không bị lỗi/treo | A | `test_TC13_username_too_long` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 14 | TC14 | Kiểm tra mật khẩu được che | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô pass<br>3. Nhập pass là: `Sai@Pass#9999` | Ô password có type=`password`, hiển thị dạng dấu chấm | A | `test_TC14_password_masked` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 15 | TC15 | Đăng nhập sai bằng phím Enter | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `{VALID_USER}`<br>4. Click vào ô pass<br>5. Nhập pass là: `Sai@Pass#9999`<br>6. Nhấn phím Enter | Tài khoản không đúng | A | `test_TC15_wrong_login_with_enter` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 16 | TC16 | Đăng nhập đúng bằng phím Enter | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `{VALID_USER}`<br>4. Click vào ô pass<br>5. Nhập pass là: `{VALID_PASS}`<br>6. Nhấn phím Enter | Đưa vào trang chủ | B | `test_TC16_login_with_enter` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 17 | TC17 | Chọn "Giữ tôi luôn đăng nhập" nhưng nhập sai mật khẩu | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là `{VALID_USER}`<br>4. Click vào ô pass<br>5. Nhập pass là: `Sai@Pass#9999`<br>6. Tích chọn "Giữ tôi luôn đăng nhập"<br>7. Click vào nút Login<br>8. Tắt trình duyệt và mở lại | Báo "Tài khoản không đúng"; sau khi mở lại vẫn ở trang đăng nhập | A | `test_TC17_keep_login_but_wrong_pass` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 18 | TC18 | Đăng xuất rồi nhấn nút Back của trình duyệt | 1. Đăng nhập thành công với `{VALID_USER}` / `{VALID_PASS}`<br>2. Click Đăng xuất<br>3. Nhấn nút Back của trình duyệt | Không xem được trang chủ, quay về trang đăng nhập | B | `test_TC18_back_after_logout` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 19 | TC19 | Truy cập trang chủ trực tiếp khi chưa đăng nhập | 1. Mở trình duyệt ẩn danh<br>2. Nhập thẳng URL trang chủ (trang sau đăng nhập) | Chuyển hướng về trang đăng nhập | A | `test_TC19_home_without_login` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 20 | TC20 | Đăng nhập thành công trên nhiều trình duyệt | 1. Mở trang https://vanphongdientu.utc.edu.vn bằng Chrome, Firefox, Edge lần lượt<br>2. Nhập user là `{VALID_USER}`, pass là: `{VALID_PASS}`<br>3. Click vào nút Login | Đăng nhập thành công trên cả 3 trình duyệt, giao diện hiển thị đúng | B | `test_TC20_cross_browser` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 21 | TC21 | Nhập SQL Injection vào username và password | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là: `' OR '1'='1`<br>4. Click vào ô pass<br>5. Nhập pass là: `' OR '1'='1`<br>6. Click vào nút Login | Tài khoản không đúng, không đăng nhập được, không lộ lỗi CSDL | C | `test_TC21_sql_injection` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 22 | TC22 | Nhập mã script vào username (XSS) | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Click vào ô username<br>3. Nhập user là: `<script>alert(1)</script>`<br>4. Click vào ô pass<br>5. Nhập pass là: `Sai@Pass#9999`<br>6. Click vào nút Login | Tài khoản không đúng, script không được thực thi (không có alert) | C | `test_TC22_xss` (`src/test/python/e2e/tests/test_login_e2e.py`) |
| 23 | TC23 | Đăng nhập sai nhiều lần liên tiếp | 1. Mở trang https://vanphongdientu.utc.edu.vn<br>2. Nhập user là `{VALID_USER}`, pass sai<br>3. Click Login<br>4. Lặp lại bước 2-3 đủ 5 lần | Hiển thị "Tài khoản không đúng" mỗi lần; nếu có cơ chế bảo vệ thì khóa tạm thời hoặc yêu cầu captcha | C | `test_TC23_many_wrong_attempts` (`src/test/python/e2e/tests/test_login_e2e.py`) |

## 3. Cách chạy automation test

```bash
pip install -r requirements.txt

# Install Allure Commandline separately (requires Node.js and Java)
npm install --global allure-commandline

# Linux/macOS
export VALID_USER=huongnt
export VALID_PASS='<mật khẩu đúng>'
# Windows PowerShell
# $env:VALID_USER="huongnt"; $env:VALID_PASS="<mật khẩu đúng>"

pytest -v --alluredir=allure-results --clean-alluredir
```

Để tập trung chạy testcase âm tính (đầu vào sai/thiếu hoặc truy cập chưa xác thực):

```bash
pytest -m negative -v --alluredir=allure-results --clean-alluredir
```

Để chỉ chạy lại lỗi đã tái hiện ở TC12:

```bash
pytest -k TC12_username_only_spaces -v --alluredir=allure-results --clean-alluredir
```

Mở báo cáo Allure HTML (yêu cầu cài Allure Commandline và Java):

```bash
allure serve allure-results
```

Hoặc tạo báo cáo tĩnh trong thư mục `allure-report`:

```bash
allure generate allure-results --clean -o allure-report
```

Các test cần mật khẩu hợp lệ sẽ tự động skip nếu thiếu `VALID_PASS`. Chạy thêm nhóm rủi ro C (có thể khóa tài khoản): đặt `RUN_RISKY=1`.

## 4. Ghi chú

- Cấu trúc test theo `src/test/python/e2e/`: `base/` khởi tạo WebDriver, `pages/` chứa Page Objects, `tests/` chứa testcase.
- Locator trong `src/test/python/e2e/pages/login_page.py` cần khớp với giao diện thật của trang.
- Các case TC10, TC11, TC13, TC23 có hai kết quả chấp nhận được theo đặc tả, kết quả thực tế ghi vào báo cáo.
- Trang hiện hiển thị `Tài khoản hoặc mật khẩu không đúng.` cho thông tin đăng nhập sai; test chấp nhận thông báo này tương đương với `Tài khoản không đúng` trong bảng.
- TC12 được giữ đúng kỳ vọng trong testcase: nếu chỉ nhập dấu cách mà không báo `Bạn chưa nhập tên đăng nhập`, test sẽ thất bại để ghi nhận sai lệch thực tế.
- Các testcase âm tính được đánh dấu `negative`; nhóm nguy cơ khóa tài khoản/XSS/SQL Injection vẫn skip mặc định.
