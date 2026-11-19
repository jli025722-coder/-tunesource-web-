from flask import Flask, jsonify, request, render_template
import datetime

app = Flask(__name__)
SITE_DOMAIN = "https://tunesource-web.onrender.com"

music_list = [
    {"id":1, "title":"Sunny Day", "artist":"Alice", "cover":"cover1.jpg", "url":"#"},
    {"id":2, "title":"Midnight Wind", "artist":"Bob", "cover":"cover2.jpg", "url":"#"},
    {"id":3, "title":"Ocean Wave", "artist":"Cindy", "cover":"cover3.jpg", "url":"#"}
]
download_records = []

@app.route('/')
def index():
    return render_template("index.html", music=music_list)

@app.route('/history')
def history_page():
    return render_template("history.html", records=download_records)

@app.route('/admin')
def admin_page():
    return render_template("admin.html", music=music_list)

@app.route('/api/search')
def search_music():
    kw = request.args.get("kw","").lower()
    res = [m for m in music_list if kw in m["title"].lower() or kw in m["artist"].lower()]
    return jsonify(res)

@app.route('/api/download', methods=["POST"])
def add_download():
    data = request.json
    record = {
        "music_title": data["title"],
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    download_records.append(record)
    return jsonify({"msg":"success"})

@app.route('/robots.txt')
def robots():
    txt = f"""User-agent: *
Allow: /
Sitemap: {SITE_DOMAIN}/sitemap.xml
"""
    return txt, 200, {"Content-Type": "text/plain"}

@app.route('/sitemap.xml')
def sitemap():
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += f"<url><loc>{SITE_DOMAIN}/</loc></url>\n"
    xml += f"<url><loc>{SITE_DOMAIN}/history</loc></url>\n"
    xml += f"<url><loc>{SITE_DOMAIN}/admin</loc></url>\n"
    for m in music_list:
        xml += f"<url><loc>{SITE_DOMAIN}/</loc></url>\n"
    xml += "</urlset>"
    return xml, 200, {"Content-Type": "application/xml"}

if __name__ == '__main__':
    app.run(debug=True)
