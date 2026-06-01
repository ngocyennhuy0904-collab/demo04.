import csv
import ssl
import urllib.request

DATA_URL = (
    "https://data.kcg.gov.tw/File/DirectDownload/"
    "80bbbbd3-9ee4-4244-98e9-b4c08deda91b"
)


def fetch_csv_text(url: str) -> str:
    """Fetch CSV text from the given URL."""
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
        raw = resp.read()

    return raw.decode("utf-8-sig")


def parse_activities(csv_text: str) -> list[dict[str, str]]:
    """Parse the CSV text into a list of dictionaries."""
    reader = csv.DictReader(csv_text.splitlines())
    return [row for row in reader]


def display_activities(rows: list[dict[str, str]], limit: int = 20) -> None:
    """Print activity rows with the most important fields."""
    if not rows:
        print("沒有找到任何活動資料。")
        return

    print("===== 活動資料 =====")
    print(f"總筆數：{len(rows)}\n")

    for idx, row in enumerate(rows[:limit], 1):
        print(f"===== 第 {idx} 筆資料 =====")
        print(f"Id          : {row.get('Id', '')}")
        print(f"Name        : {row.get('Name', '')}")
        print(f"Description : {row.get('Description', '')}")
        print(f"Participation: {row.get('Particpation', '')}")
        print(f"Location    : {row.get('Location', '')}")
        print(f"Add         : {row.get('Add', '')}")
        print(f"Tel         : {row.get('Tel', '')}")
        print(f"Org         : {row.get('Org', '')}")
        print(f"Start       : {row.get('Start', '')}")
        print(f"End         : {row.get('End', '')}")
        print(f"Map         : {row.get('Map', '')}")
        print(f"Px          : {row.get('Px', '')}")
        print(f"Py          : {row.get('Py', '')}")
        print(f"Changetime  : {row.get('Changetime', '')}\n")

    print("顯示完畢。")


def main() -> None:
    print("讀取結果")
    print("URL: " + DATA_URL)

    csv_text = fetch_csv_text(DATA_URL)
    rows = parse_activities(csv_text)
    display_activities(rows, limit=20)


if __name__ == "__main__":
    main()
