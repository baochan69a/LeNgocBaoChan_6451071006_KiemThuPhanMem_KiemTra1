# UTC E-Office Login Automation Tests

Bo kiem thu giao dien dang nhap website [Van phong dien tu UTC](https://vanphongdientu.utc.edu.vn) bang Python, Selenium va pytest. Test case duoc mo ta chi tiet trong [TESTCASES.md](TESTCASES.md).

## Yeu cau

- Python 3.10 tro len
- Google Chrome (mac dinh) hoac trinh duyet duoc ho tro trong test
- Node.js va Java neu muon tao/xem bao cao Allure HTML
- Ket noi Internet de truy cap website va de Selenium Manager tai browser driver khi can

Mat khau hop le khong duoc luu trong repository. Cac test can mat khau se tu dong skip neu chua dat bien moi truong `VALID_PASS`.

## Cai dat tren Windows

Clone repository va mo PowerShell tai thu muc project:

```powershell
git clone https://github.com/baochan69a/LeNgocBaoChan_6451071006_KiemThuPhanMem_KiemTra1.git
cd LeNgocBaoChan_6451071006_KiemThuPhanMem_KiemTra1

py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Neu PowerShell khong cho phep activate virtual environment, co the dung Python trong venv bang duong dan day du:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Selenium Manager tu dong xu ly browser driver cho trinh duyet da cai dat, khong can tai ChromeDriver thu cong.

## Chay testcase

Chay cac testcase am tinh (bo trong/sai du lieu dang nhap va truy cap khi chua dang nhap):

```powershell
pytest -m negative -v --alluredir=allure-results --clean-alluredir
```

Chay tat ca 23 testcase:

```powershell
pytest -v --alluredir=allure-results --clean-alluredir
```

Chay rieng testcase hien tai tai hien loi TC12:

```powershell
pytest -k TC12_username_only_spaces -v --alluredir=allure-results --clean-alluredir
```

Chay lai cac testcase that bai trong lan chay truoc:

```powershell
pytest --lf -v --alluredir=allure-results --clean-alluredir
```

Mac dinh Chrome chay headless. De hien cua so trinh duyet:

```powershell
$env:HEADLESS="0"
pytest -m negative -v --alluredir=allure-results --clean-alluredir
```

### Test can tai khoan hop le

Dat mat khau trong bien moi truong cua PowerShell; khong commit mat khau vao source code:

```powershell
$env:VALID_USER="huongnt"
$env:VALID_PASS="<mat-khau-hop-le>"
pytest -v --alluredir=allure-results --clean-alluredir
```

### Test rui ro

TC21 (SQL Injection), TC22 (XSS) va TC23 (dang nhap sai lap lai, co kha nang kich hoat khoa tai khoan/CAPTCHA) duoc bo qua mac dinh. Chi bat khi duoc phep kiem thu va chap nhan rui ro:

```powershell
$env:RUN_RISKY="1"
pytest -m negative -v --alluredir=allure-results --clean-alluredir
```

## Bao cao Allure

Cai Allure Commandline mot lan (can Node.js va Java):

```powershell
npm install --global allure-commandline
```

Sau khi pytest chay xong, mo bao cao:

```powershell
allure serve allure-results
```

Hoac tao bao cao HTML tinh:

```powershell
allure generate allure-results --clean -o allure-report
```

Thu muc `allure-results/` va `allure-report/` la artifact duoc tao tren may chay test, duoc ignore boi Git va khong push len GitHub. Hay chay test tren may cua ban de tao report tu ket qua moi.

## Cau truc

```text
src/test/python/e2e/
|-- base/
|   |-- base_test.py       # Tao va dong WebDriver, fixture, cau hinh
|-- pages/
|   |-- base_page.py       # Thao tac Selenium chung
|   |-- login_page.py      # Page Object form dang nhap
|   |-- dashboard_page.py  # Kiem tra trang da dang nhap va dang xuat
|-- tests/
    |-- conftest.py        # Screenshot Allure khi test that bai
    |-- test_login_e2e.py  # 23 testcase pytest/Selenium
```

Tren website tai thoi diem kiem tra, TC12 phat hien username chi gom dau cach khong duoc xem la username trong de; test duoc giu lai de report ghi nhan sai lech nay.
