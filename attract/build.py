"""Build attract.html: embed the real IEEE-118 data and the fonts into the template.
Usage: python build.py <blacksky/site dir> <template> <out>"""
import base64, json, math, pathlib, sys

here = pathlib.Path(__file__).resolve().parent
site = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else here.parent / "blacksky/site"
tpl = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else here / "attract.src.html"
out = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else here / "attract.html"
g = json.load(open(site / "data/grid_ieee118.json"))
c = json.load(open(site / "data/top_cascades_ieee118_k3.json"))[0]["dc"]
assert c["outage"] == [6, 67, 140]
nb = g["n_branch"]

frames = []
for f in c["frames"]:
    load = [round(f["loading"].get(str(b), -1.0), 3) for b in range(nb)]
    frames.append({"out": f["out_of_service"], "ovl": f["overloaded"], "en": [i - 1 for i in f["energized_buses"]],  # bus ids are 1-based in the export
                  
                   "served": round(f["load_served"], 6), "islands": f["islands"], "load": load})

# derived figures — must equal the project's published numbers
trips = len(frames[-1]["out"]) - 3
rounds = c["metrics"]["rounds"]
dark = g["n_bus"] - len(frames[-1]["en"])
S = round(c["metrics"]["S"] * 100, 1)
mx = max((v, r, b) for r, f in enumerate(frames) for b, v in enumerate(f["load"]))
assert (trips, rounds, dark, S) == (97, 7, 31, 22.8), (trips, rounds, dark, S)
assert mx[2] == 110 and round(mx[0] * 100) == 612, mx

data = {
    "x": [round(v, 4) for v in g["layout"]["x"]], "y": [round(v, 4) for v in g["layout"]["y"]],
    "load": [b["load_mw"] for b in g["buses"]], "gen": [1 if b["has_gen"] else 0 for b in g["buses"]],
    "kv": [b["base_kv"] for b in g["buses"]],
    "from": [b["from"] for b in g["branches"]], "to": [b["to"] for b in g["branches"]],
    "base": [round(b["base_loading_dc"], 3) for b in g["branches"]],
    "outage": c["outage"], "frames": frames, "totalLoad": g["total_load_mw"],
    "derived": {"trips": trips, "rounds": rounds, "dark": dark, "S": S, "maxLoad": round(mx[0] * 100), "maxBranch": mx[2], "maxRound": mx[1]},
    "sha": g["file_sha256"][:12],
}

fonts = ""
for fam, w, f in [("Archivo", 500, "archivo-latin-500-normal.woff2"), ("Archivo", 700, "archivo-latin-700-normal.woff2"),
                  ("JBM", 400, "jetbrains-mono-latin-400-normal.woff2"), ("JBM", 500, "jetbrains-mono-latin-500-normal.woff2")]:
    b64 = base64.b64encode((site / "fonts" / f).read_bytes()).decode()
    fonts += f'@font-face{{font-family:"{fam}";font-weight:{w};font-display:block;src:url(data:font/woff2;base64,{b64}) format("woff2")}}\n'

html = tpl.read_text().replace("/*__FONTS__*/", fonts).replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
out.write_text(html)
print("wrote", out, f"{out.stat().st_size/1024:.0f} KB", data["derived"])
