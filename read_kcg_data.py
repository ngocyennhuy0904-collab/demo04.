import csv
import ssl
import urllib.request

DATA_URL = "https://data.ntpc.gov.tw/api/datasets/781b822e-214a-4b9a-b4db-32c9f4626d98/csv/file"


def fetch_csv_text(url: str) -> str:
    """Fetch CSV text from the given URL."""
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        raw = resp.read()

    return raw.decode("utf-8-sig")


def parse_activities(csv_text: str) -> tuple[list[dict[str, str]], list[str]]:
    """Parse the CSV text into a list of dictionaries and return headers."""
    reader = csv.DictReader(csv_text.splitlines())
    rows = [row for row in reader]
    return rows, reader.fieldnames or []


def display_activities(rows: list[dict[str, str]], headers: list[str], limit: int = 20) -> None:
    """Print activity rows and all available fields for verification."""
    if not rows:
        print("沒有找到任何活動資料。")
        return

    print("===== 活動資料 =====")
    print(f"總筆數：{len(rows)}")
    print(f"欄位數：{len(headers)}")
    print("欄位名稱：" + ", ".join(headers) + "\n")

    max_rows = len(rows) if limit is None else min(len(rows), limit)
    for idx in range(max_rows):
        row = rows[idx]
        print(f"===== 第 {idx + 1} 筆資料 =====")
        for header in headers:
            print(f"{header:20}: {row.get(header, '')}")
        print()

    if limit is not None and len(rows) > limit:
        print(f"已顯示前 {limit} 筆資料。若要顯示全部資料，請將 limit 設為 None。")

    print("顯示完畢。")


def main() -> None:
    print("讀取結果")
    print("URL: " + DATA_URL)

    csv_text = fetch_csv_text(DATA_URL)
    rows, headers = parse_activities(csv_text)
    display_activities(rows, headers, limit=None)


if __name__ == "__main__":
    main()
#test