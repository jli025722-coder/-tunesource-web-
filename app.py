from flask import Flask, jsonify, request, render_template
import datetime

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
