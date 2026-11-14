"""Cliente multiplataforma para enviar JSON sin problemas de comillas."""
import argparse
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("method", choices=["GET", "POST"])
    p.add_argument("url")
    p.add_argument("--file")
    p.add_argument("--key")
    p.add_argument("--auth", action="store_true")
    p.add_argument("--timeout", type=float, default=20)
    args = p.parse_args()
    scheme = urlparse(args.url).scheme
    if scheme not in ("http", "https"):
        p.error("La URL debe empezar por http:// o https://")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if args.auth:
        headers["Authorization"] = "Bearer " + (ROOT / "lab/token.txt").read_text(encoding="utf-8").strip()
    if args.key:
        headers["Idempotency-Key"] = args.key
    data = None
    if args.file:
        obj = json.loads(Path(args.file).read_text(encoding="utf-8"))
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    req = Request(args.url, data=data, headers=headers, method=args.method)
    try:
        with urlopen(req, timeout=args.timeout) as response:
            print("HTTP", response.status)
            print(response.read().decode("utf-8"))
    except HTTPError as e:
        print("HTTP", e.code)
        print(e.read().decode("utf-8"))
        sys.exit(1)
    except URLError as e:
        print("No se pudo conectar:", e.reason)
        sys.exit(2)


if __name__ == "__main__":
    main()
