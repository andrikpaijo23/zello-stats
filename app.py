
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
LOG_FILE = "zello_log.txt"

def parse_logs():
    per_user = defaultdict(int)
    per_user_durasi = defaultdict(int)
    per_channel = defaultdict(int)

    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) < 4:
                    continue
                waktu = datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S.%f")
                channel = parts[1].strip()
                user = parts[2].strip()
                durasi = int(parts[3].strip())

                per_user[user] += 1
                per_user_durasi[user] += durasi
                per_channel[channel] += 1
    except FileNotFoundError:
        pass

    return per_user, per_user_durasi, per_channel

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    users, durasi, channels = parse_logs()
    return jsonify({
        "user": users,
        "durasi": durasi,
        "channel": channels
    })

@app.route("/upload", methods=["POST"])
def upload():
    try:
        line = request.data.decode("utf-8")
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
        return "OK", 200
    except Exception as e:
        return str(e), 500
