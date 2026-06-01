import csv
import io
import ssl
import urllib.request
from flask import Flask, render_template

app = Flask(__name__)

# URL mới lấy dữ liệu hoạt động văn hóa (như trong ảnh mẫu hiển thị Tân Bắc)
# Nếu đề bài vẫn bắt dùng link Cao Hùng cũ, bạn chỉ cần giữ nguyên link cũ là được nhé!
URL = "https://data.kcg.gov.tw/File/DirectDownload/80bbbbd3-9ee4-4244-98e9-b4c08deda91b"


def get_all_data():
    context = ssl._create_unverified_context()
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=context) as response:
            data = response.read().decode("utf-8-sig")

            csv_file = io.StringIO(data)
            reader = csv.DictReader(csv_file)

            data_list = list(reader)

            # Xử lý làm sạch dữ liệu trống thành "無" cho toàn bộ danh sách
            for row in data_list:
                for key, value in row.items():
                    if not value or value.strip() == "":
                        row[key] = "無"
            return data_list
    except Exception as e:
        print(f"Lỗi tải dữ liệu: {e}")
        return []


@app.route("/")
def home():
    # Lấy toàn bộ danh sách dữ liệu thay vì chỉ lấy 1 dòng
    all_activities = get_all_data()

    # Truyền danh sách sang HTML để lặp ra giao diện
    return render_template("index.html", activities=all_activities)


if __name__ == "__main__":
    # Ép Flask bật dòng WARNING màu đỏ và chạy trên host 0.0.0.0 chuẩn đề bài
    app.run(host="0.0.0.0", port=5000, debug=True)
    /test
    