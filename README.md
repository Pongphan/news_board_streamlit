# Campus News Board — Streamlit + SQLite

เว็บแอปบอร์ดข่าวสาร 3 หน้า พัฒนาด้วย Streamlit และ SQLite พร้อม validation, หน้าผู้ดูแล, automated tests และไฟล์สำหรับ deploy

UI ใช้แนวทาง pastel glass-tech แบบ responsive รองรับ light/dark ตาม browser preference และสลับภาษา EN/TH จากมุมขวาบน โดยใช้ภาษาอังกฤษเป็นค่าเริ่มต้น

## Project Structure

```text
news_board_streamlit/
├── app.py                    # Dashboard: อ่าน/ค้นหา/กรองข่าว และปุ่มเพิ่มเนื้อหา
├── database.py               # SQLite schema และ data-access functions
├── admin_auth.py             # ตรวจรหัสผ่านและ session authentication
├── admin_export.py           # สร้าง CSV ฉบับเต็มสำหรับ Admin
├── validation.py             # ตรวจและ normalize ข้อมูลก่อนบันทึก
├── ui.py                     # page config, responsive CSS และ UI helpers
├── pages/
│   ├── add_content.py        # ฟอร์มเพิ่มข่าวและ navigation กลับ Dashboard
│   └── admin.py              # ตรวจสอบ ส่งออก ซ่อน กู้คืน และลบข้อมูล
├── tests/
│   ├── test_admin.py         # ทดสอบ password และ CSV export
│   ├── test_database.py      # ทดสอบ schema, insert, query และ constraints
│   ├── test_validation.py    # ทดสอบ Student ID, summary และ URL
│   └── test_smoke.py         # เปิด Dashboard ด้วย Streamlit AppTest
├── data/
│   └── .gitkeep              # news_board.db จะถูกสร้างอัตโนมัติ
├── .streamlit/
│   └── config.toml           # theme และซ่อน sidebar navigation
├── requirements.txt          # production dependencies
└── requirements-dev.txt      # test dependencies
```

## การทำงานของแต่ละส่วน

- `app.py` เรียก `initialize_database()` ทุกครั้งที่เริ่มแอป (คำสั่งเป็น idempotent), โหลดข่าวล่าสุด, ค้นหา/กรอง และแสดงการ์ด 2 คอลัมน์ ปุ่มเพิ่มเนื้อหาถูกตรึงไว้ที่มุมซ้ายล่างและเรียก `st.switch_page("pages/add_content.py")`
- `pages/add_content.py` รับ Section, Student ID, News Summary และ Source URI หลัง validation ผ่านจึง insert แบบ transaction จากนั้นล้าง `st.cache_data`, เก็บ success message ใน `st.session_state` และ `st.switch_page("app.py")` ทำให้ Dashboard โหลดข้อมูลใหม่อัตโนมัติ
- `pages/admin.py` ป้องกันข้อมูลด้วย session authentication แสดง Student ID ฉบับเต็ม ค้นหา/กรอง เปิดแหล่งข้อมูล ดาวน์โหลด CSV ซ่อน/กู้คืน และลบแบบยืนยันสองขั้น
- `database.py` ใช้ parameterized SQL, `CHECK` constraints, UTC timestamp, WAL mode และ busy timeout พร้อม migration เพิ่มสถานะ `published`/`hidden` โดยไม่ลบข้อมูลเดิม ฐานข้อมูลอยู่ที่ `data/news_board.db`
- `admin_auth.py` ตรวจ password แบบ constant-time จาก SHA-256 digest และรองรับการ override ผ่าน Streamlit Secrets
- `admin_export.py` ส่งออกข้อมูลที่กรองแล้วเป็น UTF-8 CSV พร้อม Student ID ฉบับเต็ม และป้องกัน spreadsheet formula injection
- `validation.py` อนุญาตเฉพาะ Section 1–3, Student ID 4–20 ตัว, summary 10–2,000 ตัว และ URL แบบ HTTP/HTTPS ที่มี hostname โดยคืน message key สำหรับแสดงผลสองภาษา
- `ui.py` รวมข้อความ EN/TH, language state, pastel glass-tech theme, responsive layout, helper ปกปิด Student ID บางส่วน และแปลงเวลา UTC เป็นเวลาไทย (UTC+7)
- `.streamlit/config.toml` กำหนด palette แยก `[theme.light]` และ `[theme.dark]` เพื่อให้ Streamlitเลือกตาม browser/system theme อัตโนมัติ

## Local Setup

ต้องใช้ Python 3.12 (แนะนำให้ใช้ version เดียวกับ Community Cloud)

### Windows PowerShell

```powershell
cd news_board_streamlit
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m streamlit run app.py
```

### macOS / Linux

```bash
cd news_board_streamlit
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m streamlit run app.py
```

เปิด `http://localhost:8501` แล้วทดสอบเพิ่มข่าว ระบบจะสร้าง `data/news_board.db` ให้อัตโนมัติ

## Admin

เข้าได้จากปุ่ม **Admin** มุมขวาบน หรือ URL `/admin` ของ multipage app

- Password เริ่มต้นตามข้อกำหนด: `isai12admin`
- สถานะการเข้าสู่ระบบเก็บเฉพาะ Streamlit session ปัจจุบัน เมื่อกด Sign out หรือ session สิ้นสุดต้องเข้าสู่ระบบใหม่
- `Published` แสดงบน Dashboard สาธารณะ
- `Hidden` ไม่แสดงบน Dashboard แต่ข้อมูลยังอยู่และ Admin กู้คืนได้
- `Delete` ลบถาวรหลังยืนยันครั้งที่สอง
- CSV จะส่งออกเฉพาะรายการที่ตรงกับตัวกรองปัจจุบัน พร้อม Student ID ฉบับเต็ม

สำหรับระบบ production ควรเปลี่ยนรหัสผ่านผ่าน `.streamlit/secrets.toml` ซึ่งถูก `.gitignore` ไว้แล้ว:

```toml
[admin]
password = "your-long-random-password"
```

หรือ paste ค่าเดียวกันใน **Streamlit Community Cloud → App settings → Secrets** รหัสผ่านเริ่มต้นมีไว้ตามข้อกำหนดของระบบนี้และไม่ควรใช้กับระบบสาธารณะระยะยาว

รัน automated tests:

```bash
python -m pytest -q
```

## Database Schema

```sql
CREATE TABLE news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL CHECK (section IN ('Section 1', 'Section 2', 'Section 3')),
    student_id TEXT NOT NULL CHECK (length(student_id) BETWEEN 4 AND 20),
    news_summary TEXT NOT NULL CHECK (length(news_summary) BETWEEN 10 AND 2000),
    source_uri TEXT NOT NULL,
    created_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'published'
        CHECK (status IN ('published', 'hidden')),
    moderated_at TEXT
);
```

## Deploy: Streamlit Community Cloud

1. สร้าง GitHub repository แล้ว commit/push โฟลเดอร์นี้ โดยไม่ commit `data/news_board.db`
2. เข้า [share.streamlit.io](https://share.streamlit.io) และเชื่อมบัญชี GitHub
3. เลือก **Create app** → **Yup, I have an app**
4. เลือก repository, branch และกำหนด main file path:
   - ถ้าโฟลเดอร์นี้เป็น root ของ repo: `app.py`
   - ถ้าอยู่ใน monorepo นี้: `news_board_streamlit/app.py`
5. หากใช้ monorepo ให้ copy/merge `.streamlit/config.toml` ไปที่ `.streamlit/config.toml` ของ **repo root** เพราะ Community Cloud อ่าน configuration จากตำแหน่ง root เพียงแห่งเดียว
6. ใน **Advanced settings** เลือก Python `3.12` หากต้องการเปลี่ยนรหัสผ่าน Admin ให้เพิ่ม `[admin] password = "..."` ใน Secrets แล้วกด **Deploy**
7. ตรวจ Cloud logs แล้วทดสอบเพิ่มข่าวและกลับ Dashboard

`requirements.txt` อยู่ข้าง entrypoint จึงถูก Community Cloud ตรวจพบอัตโนมัติ เมื่อ push โค้ดใหม่ Community Cloud จะ redeploy ให้

### ข้อควรรู้ก่อนใช้ Production

SQLite เหมาะสำหรับ local, prototype, ห้องเรียนขนาดเล็ก หรือ server เดียวที่มี persistent disk แต่ local filesystem ของ Streamlit Community Cloud **ไม่รับประกันการเก็บข้อมูลถาวร** ข้อมูลที่เพิ่มอาจหายเมื่อแอป reboot/redeploy/ย้ายเครื่อง

สำหรับ production ที่ต้องเก็บข้อมูลจริง ให้เปลี่ยน data-access layer ใน `database.py` เป็น PostgreSQL ภายนอก (เช่น managed PostgreSQL) และเก็บ connection string ใน Streamlit Secrets ห้าม commit credential ลง Git ระบบ validation และ UI สามารถใช้ต่อได้โดยไม่ต้องเปลี่ยน

เอกสารทางการ:

- [Deploy an app on Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)
- [File organization](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization)
- [App dependencies](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies)
- [Connecting to data — SQLite persistence note](https://docs.streamlit.io/develop/concepts/connections/connecting-to-data)
- [`st.switch_page`](https://docs.streamlit.io/develop/api-reference/navigation/st.switch_page)
- [Session State](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
- [Community Cloud secrets management](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
