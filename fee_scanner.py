"""
Fee Scanner — анализ комиссий в Bitcoin за последние блоки.
"""

import requests
import argparse

def fetch_recent_blocks(count):
    url = f"https://api.blockchair.com/bitcoin/blocks?limit={count}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("❌ Ошибка загрузки блоков.")
    return r.json()["data"]

def analyze_fees(blocks):
    print(f"📊 Анализ {len(blocks)} последних блоков:")
    total_fees = 0
    fee_list = []

    for block in blocks:
        height = block["id"]
        fees = block.get("fee_total", 0)
        size = block.get("size", 1)
        fee_per_byte = round(fees / size, 2) if size > 0 else 0
        fee_list.append(fee_per_byte)
        total_fees += fees
        print(f"  • Блок #{height}: {fee_per_byte} сат/байт")

    avg_fee = round(sum(fee_list) / len(fee_list), 2)
    print(f"
📈 Средняя комиссия: {avg_fee} сат/байт")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fee Scanner — утилита для анализа комиссий в блоках Bitcoin.")
    parser.add_argument("-n", "--num-blocks", type=int, default=10, help="Количество последних блоков (по умолчанию 10)")
    args = parser.parse_args()

    blocks = fetch_recent_blocks(args.num_blocks)
    analyze_fees(blocks)
