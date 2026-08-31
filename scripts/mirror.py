#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""webmcpshield.com/data/ の封済みファイルをこのリポジトリへ取り込む。

【なぜ取りに行く形にしたか】
本番サーバーから push する形にすると、サーバーにもう1つデプロイキーを置く
ことになる。publish-snapshot.sh のコメントにあるとおり、あちらは push 失敗の
切り分けで一度つまずいている。鍵を増やすと同じ種類の障害が増える。
取りに行く形なら、サーバーは何も知らなくてよい。

【取りこぼしを自分で直せる】
index.json と手元を突き合わせるので、何日か止まっても次回にまとめて埋まる。

【検証してから書く】
index.json に載っている sha256 と照合し、一致したものだけ保存する。
「byte-identical な写しである」と README に書いている以上、
検証せずに保存してはいけない。
"""

import hashlib
import json
import os
import sys
import urllib.request

BASE = "https://webmcpshield.com/data"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def fetch(path: str) -> bytes:
    req = urllib.request.Request(f"{BASE}/{path}",
                                 headers={"User-Agent": "webmcp-shield-data-mirror"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    try:
        index_raw = fetch("index.json")
        index = json.loads(index_raw)
    except Exception as e:
        print(f"index.json を取得できない: {e}", file=sys.stderr)
        return 1

    added, skipped, failed = [], 0, []

    for snap in index.get("snapshots", []):
        date, want = snap.get("date"), snap.get("sha256")
        if not date or not want:
            continue
        dest = os.path.join(OUT, f"{date}.json")

        if os.path.exists(dest):
            with open(dest, "rb") as f:
                if hashlib.sha256(f.read()).hexdigest() == want:
                    skipped += 1
                    continue
            # 手元が index と食い違う。封済みファイルは書き換わらない約束なので、
            # ここに来ること自体が異常。上書きせず報告する。
            failed.append(f"{date}: 手元のファイルが index の sha256 と一致しない")
            continue

        try:
            body = fetch(f"{date}.json")
        except Exception as e:
            failed.append(f"{date}: 取得に失敗 ({e})")
            continue

        got = hashlib.sha256(body).hexdigest()
        if got != want:
            failed.append(f"{date}: sha256 不一致 (index={want[:12]}… 実物={got[:12]}…)")
            continue

        with open(dest, "wb") as f:
            f.write(body)
        added.append(date)

    # index.json は errata が追記されるので毎回書き直す
    with open(os.path.join(OUT, "index.json"), "wb") as f:
        f.write(index_raw)

    print(f"取り込み: {len(added)}件 / 既存: {skipped}件 / 失敗: {len(failed)}件")
    for d in added:
        print(f"  + {d}")
    for msg in failed:
        print(f"  ! {msg}")

    # 取得や検証に失敗したものがあれば、気づけるように異常終了する。
    # 既に手元にある分の取り込みは済んでいるので、部分的な成功は残る。
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
