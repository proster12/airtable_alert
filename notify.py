from pyairtable import Api
import requests
import os

# Airtable 연결
api = Api(os.environ["AIRTABLE_TOKEN"])

table = api.table(
    os.environ["BASE_ID"],
    "tbl6s3XT9tcTIQ95f"
)

rows = table.all()
print(rows)

for row in rows:

    fields = row["fields"]

    remain = fields.get("남은일수")

    if remain is None:
        continue

    try:
        remain = int(float(remain))
    except:
        continue

    # 7일, 3일, 1일, 당일 알림
    if remain in [7, 3, 1, 0]:

        sponsor = fields.get("후원자", "")
        consume_date = fields.get("예상 소진일", "")

        message = (
            f"⚠️ 소비자 소진예정 알림\n\n"
            f"후원자 : {sponsor}\n"
            f"예상 소진일 : {consume_date}\n"
            f"남은일수 : {remain}일"
        )

        response = requests.post(
            f"https://api.telegram.org/bot{os.environ['BOT_TOKEN']}/sendMessage",
            data={
                "chat_id": os.environ["CHAT_ID"],
                "text": message
            }
        )

        print(
            f"{sponsor} / {remain}일 -> "
            f"{response.status_code}"
        )
