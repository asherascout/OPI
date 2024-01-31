# pip install python-dotenv
# pip install psycopg2-binary

import os, sys, requests
from dotenv import load_dotenv
import time

if not os.path.isfile(".env"):
    print('.env file not found, please run "python3 reset_init.py" first')
    sys.exit(1)


## load env variables
load_dotenv()

report_url = "https://api.opi.network/report_block"
report_retries = 10
report_name = os.getenv("REPORT_NAME") or "opi_brc20_indexer"


def try_to_report_with_retries(to_send):
    global report_url, report_retries
    for _ in range(0, report_retries):
        try:
            r = requests.post(report_url, json=to_send)
            if r.status_code == 200:
                print("Reported hashes to metaprotocol indexer indexer.")
                return
            else:
                print(
                    "Error while reporting hashes to metaprotocol indexer indexer, status code: "
                    + str(r.status_code)
                )
        except:
            print(
                "Error while reporting hashes to metaprotocol indexer indexer, retrying..."
            )
        time.sleep(1)
    print("Error while reporting hashes to metaprotocol indexer indexer, giving up.")


def main():
    to_send = {}
    while True:
        time.sleep(5)
        response = requests.get("http://23.154.136.144:15000/json")
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析返回的JSON
            data = response.json()
            if (
                to_send["block_height"] == data["block_height"]
                and to_send["block_event_hash"] == data["block_event_hash"]
            ):
                print("Waiting for new blocks...")
                continue
            to_send = data
            to_send["name"] = report_name
            print("Sending hashes to metaprotocol indexer indexer...")
            try_to_report_with_retries(to_send)

        else:
            print(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    main()
