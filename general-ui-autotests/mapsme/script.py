import json

if __name__ == '__main__':
    with open("result.json", "r") as f:
        sting = f.read()
        res = json.loads(sting)
        all = len(res)
        banner = 0
        result = {}
        for r in res:
            banner = banner + r["banner"]
