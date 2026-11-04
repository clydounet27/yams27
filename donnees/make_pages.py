# Génère : yams.html (artifact), carnet_yams.html (fichier autonome), yams27/public/index.html (site Firebase)
import sys, os
root = os.path.dirname(os.path.abspath(__file__))
tpl = open(os.path.join(root, "app_template.html"), encoding="utf-8").read()
data = open(os.path.join(root, "yams_data.json"), encoding="utf-8").read()
page = tpl.replace("__DATA__", data)
open(os.path.join(root, "yams.html"), "w", encoding="utf-8").write(page)
HEAD = '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
def wrap(p, extra_head="", extra_body=""):
    return HEAD + extra_head + p.replace('<div class="wrap">', '</head>\n<body>\n<div class="wrap">', 1) + "\n" + extra_body + "</body>\n</html>\n"
open(os.path.join(root, "carnet_yams.html"), "w", encoding="utf-8").write(wrap(page))
web_head = '''<meta name="theme-color" content="#2347a8">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Yam's">
<script>window.YAMS_WAIT=true</script>
'''
addon = open(os.path.join(root, "web_addon.html"), encoding="utf-8").read()
sw = '<script>if("serviceWorker" in navigator){navigator.serviceWorker.register("sw.js")}</script>\n'
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "yams27", "public", "index.html")
open(out, "w", encoding="utf-8").write(wrap(page, web_head, addon + sw))
print("ok", out)
