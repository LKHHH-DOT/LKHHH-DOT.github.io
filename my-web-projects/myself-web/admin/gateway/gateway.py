#!/usr/bin/env python3
"""
API 网关服务 — 接收内容管理请求，同时写入 JSON（网站用）和加密存 SQLite（安全备份）
"""

import json
import os
import re
import sys
import sqlite3
import hashlib
from datetime import date
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "src", "data")
GATEWAY_DIR = os.path.join(BASE_DIR, "admin", "gateway")

# 确保 gateway 目录存在
os.makedirs(GATEWAY_DIR, exist_ok=True)

# ===== 加密配置 =====
KEY_FILE = os.path.join(GATEWAY_DIR, ".gateway_key")
DB_PATH = os.path.join(GATEWAY_DIR, "secure.db")


def get_or_create_key():
    """获取或生成加密密钥"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key = f.read().strip().encode()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "w") as f:
            f.write(key.decode())
        os.chmod(KEY_FILE, 0o600)  # 仅所有者可读写
    return key


def get_cipher():
    return Fernet(get_or_create_key())


# ===== 数据库初始化 =====

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 个人信息表 — 加密存储
    c.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 动态更新表 — 每条记录单独加密
    c.execute("""
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 成就表
    c.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 操作日志表
    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            entity TEXT NOT NULL,
            entity_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 博客表
    c.execute("""
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 项目表
    c.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 状态表
    c.execute("""
        CREATE TABLE IF NOT EXISTS status_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def log_audit(action, entity, entity_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO audit_log (action, entity, entity_id) VALUES (?, ?, ?)",
        (action, entity, entity_id)
    )
    conn.commit()
    conn.close()


def encrypt_data(data):
    """加密 JSON 数据，返回 (密文, 校验和)"""
    cipher = get_cipher()
    json_str = json.dumps(data, ensure_ascii=False, sort_keys=True)
    encrypted = cipher.encrypt(json_str.encode("utf-8")).decode()
    checksum = hashlib.sha256(json_str.encode()).hexdigest()
    return encrypted, checksum


def decrypt_data(encrypted):
    """解密数据"""
    cipher = get_cipher()
    decrypted = cipher.decrypt(encrypted.encode("utf-8"))
    return json.loads(decrypted.decode("utf-8"))


# ===== JSON 文件读写工具 =====

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ===== 同步写入 JSON + 加密数据库 =====

def sync_profile(data):
    """同时写入 profile.json 和加密库（合并数据，保留完整字段）"""
    # 1. 读取现有 JSON，合并新数据
    profile_path = os.path.join(DATA_DIR, "profile.json")
    existing = load_json(profile_path, {})

    # 深合并：保留现有字段，用新数据覆盖
    for key in data:
        if key == "contact" and isinstance(data[key], dict) and isinstance(existing.get("contact"), dict):
            existing["contact"].update(data[key])
        elif key == "education" and isinstance(data[key], list):
            existing["education"] = data[key]
        else:
            existing[key] = data[key]

    # 确保所有必要字段存在
    defaults = {
        "name": "", "nickname": "", "avatar": "", "title": "", "bio": "", "location": "",
        "contact": {"email": "", "github": "", "wechat": "", "twitter": "", "website": ""},
        "education": [], "skills": [], "interests": []
    }
    for key, val in defaults.items():
        if key not in existing:
            existing[key] = val
        elif key == "contact":
            for k, v in val.items():
                if k not in existing["contact"]:
                    existing["contact"][k] = v

    save_json(profile_path, existing)

    # 2. 加密写入 SQLite（写合并后的完整数据）
    encrypted, checksum = encrypt_data(existing)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO profile (id, data_encrypted, checksum, updated_at)
        VALUES (1, ?, ?, CURRENT_TIMESTAMP)
    """, (encrypted, checksum))
    conn.commit()
    conn.close()

    log_audit("SAVE", "profile")
    return True


def sync_updates(data):
    """全量同步 updates（先清空再写入）"""
    # 1. 写入 JSON
    updates_path = os.path.join(DATA_DIR, "updates.json")
    save_json(updates_path, data)

    # 2. 全量加密写入 SQLite
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM updates")
    for item in data:
        encrypted, checksum = encrypt_data(item)
        c.execute(
            "INSERT INTO updates (data_encrypted, checksum) VALUES (?, ?)",
            (encrypted, checksum)
        )
    conn.commit()
    conn.close()

    log_audit("SYNC", "updates")
    return True


def sync_achievements(data):
    """全量同步 achievements"""
    achievements_path = os.path.join(DATA_DIR, "achievements.json")
    save_json(achievements_path, data)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM achievements")
    for item in data:
        encrypted, checksum = encrypt_data(item)
        c.execute(
            "INSERT INTO achievements (data_encrypted, checksum) VALUES (?, ?)",
            (encrypted, checksum)
        )
    conn.commit()
    conn.close()

    log_audit("SYNC", "achievements")
    return True


def sync_files(data):
    """全量同步 files"""
    files_path = os.path.join(DATA_DIR, "files.json")
    save_json(files_path, data)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 如果还没有 files 表，先创建
    c.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("DELETE FROM files")
    for item in data:
        encrypted, checksum = encrypt_data(item)
        c.execute(
            "INSERT INTO files (data_encrypted, checksum) VALUES (?, ?)",
            (encrypted, checksum)
        )
    conn.commit()
    conn.close()

    log_audit("SYNC", "files")
    return True


def sync_blogs(data):
    blogs_path = os.path.join(DATA_DIR, "blogs.json")
    save_json(blogs_path, data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM blogs")
    for item in data:
        encrypted, checksum = encrypt_data(item)
        c.execute("INSERT INTO blogs (data_encrypted, checksum) VALUES (?, ?)", (encrypted, checksum))
    conn.commit()
    conn.close()
    log_audit("SYNC", "blogs")
    return True


def sync_projects(data):
    projects_path = os.path.join(DATA_DIR, "projects.json")
    save_json(projects_path, data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM projects")
    for item in data:
        encrypted, checksum = encrypt_data(item)
        c.execute("INSERT INTO projects (data_encrypted, checksum) VALUES (?, ?)", (encrypted, checksum))
    conn.commit()
    conn.close()
    log_audit("SYNC", "projects")
    return True


def sync_status(data):
    status_path = os.path.join(DATA_DIR, "status.json")
    save_json(status_path, data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM status_items")
    for item in data:
        encrypted, checksum = encrypt_data(item)
        c.execute("INSERT INTO status_items (data_encrypted, checksum) VALUES (?, ?)", (encrypted, checksum))
    conn.commit()
    conn.close()
    log_audit("SYNC", "status")
    return True


# ===== API 接口（供 Flask 后台调用）=====

@app.route("/api/profile", methods=["GET", "POST"])
def handle_profile():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_profile(data)
        return jsonify({"status": "ok", "message": "个人信息已保存（JSON + 加密库）"})
    else:
        # 从加密库读取
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT data_encrypted FROM profile WHERE id = 1")
        row = c.fetchone()
        conn.close()
        if row:
            return jsonify(decrypt_data(row[0]))
        # 回退到 JSON
        return jsonify(load_json(os.path.join(DATA_DIR, "profile.json"), {}))


@app.route("/api/updates", methods=["GET", "POST"])
def handle_updates():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_updates(data)
        return jsonify({"status": "ok", "message": "动态已同步（JSON + 加密库）"})
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT data_encrypted FROM updates ORDER BY id")
        rows = c.fetchall()
        conn.close()
        if rows:
            return jsonify([decrypt_data(r[0]) for r in rows])
        return jsonify(load_json(os.path.join(DATA_DIR, "updates.json"), []))


@app.route("/api/achievements", methods=["GET", "POST"])
def handle_achievements():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_achievements(data)
        return jsonify({"status": "ok", "message": "成就已同步（JSON + 加密库）"})
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT data_encrypted FROM achievements ORDER BY id")
        rows = c.fetchall()
        conn.close()
        if rows:
            return jsonify([decrypt_data(r[0]) for r in rows])
        return jsonify(load_json(os.path.join(DATA_DIR, "achievements.json"), []))


@app.route("/api/files", methods=["GET", "POST"])
def handle_files():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_files(data)
        return jsonify({"status": "ok", "message": "文件已同步（JSON + 加密库）"})
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # 检查表是否存在
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
        if not c.fetchone():
            conn.close()
            raw = load_json(os.path.join(DATA_DIR, "files.json"), {"files": []})
            return jsonify(raw.get("files", []))
        c.execute("SELECT data_encrypted FROM files ORDER BY id")
        rows = c.fetchall()
        conn.close()
        if rows:
            return jsonify([decrypt_data(r[0]) for r in rows])
        raw = load_json(os.path.join(DATA_DIR, "files.json"), {"files": []})
        return jsonify(raw.get("files", []))


@app.route("/api/blogs", methods=["GET", "POST"])
def handle_blogs():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_blogs(data)
        return jsonify({"status": "ok", "message": "博客已同步（JSON + 加密库）"})
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT data_encrypted FROM blogs ORDER BY id")
        rows = c.fetchall()
        conn.close()
        if rows:
            return jsonify([decrypt_data(r[0]) for r in rows])
        return jsonify(load_json(os.path.join(DATA_DIR, "blogs.json"), []))


@app.route("/api/projects", methods=["GET", "POST"])
def handle_projects():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_projects(data)
        return jsonify({"status": "ok", "message": "项目已同步（JSON + 加密库）"})
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT data_encrypted FROM projects ORDER BY id")
        rows = c.fetchall()
        conn.close()
        if rows:
            return jsonify([decrypt_data(r[0]) for r in rows])
        return jsonify(load_json(os.path.join(DATA_DIR, "projects.json"), []))


@app.route("/api/status", methods=["GET", "POST"])
def handle_status():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_status(data)
        return jsonify({"status": "ok", "message": "状态已同步（JSON + 加密库）"})
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT data_encrypted FROM status_items ORDER BY id")
        rows = c.fetchall()
        conn.close()
        if rows:
            return jsonify([decrypt_data(r[0]) for r in rows])
        return jsonify(load_json(os.path.join(DATA_DIR, "status.json"), []))


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "API Gateway",
        "encryption": "Fernet (AES-128-CBC)",
        "db": os.path.exists(DB_PATH),
        "key": os.path.exists(KEY_FILE)
    })


@app.route("/api/audit")
def audit_log():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, action, entity, entity_id, timestamp FROM audit_log ORDER BY id DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {"id": r[0], "action": r[1], "entity": r[2], "entity_id": r[3], "timestamp": r[4]}
        for r in rows
    ])


@app.route("/api/videos/<filename>")
def serve_video(filename):
    """提供视频文件流式播放"""
    safe_name = secure_filename(filename)
    if not safe_name:
        return "", 400

    video_dir = os.path.join(DATA_DIR, "videos")
    file_path = os.path.join(video_dir, safe_name)

    if not os.path.exists(file_path):
        return "", 404

    # 获取文件大小
    file_size = os.path.getsize(file_path)

    # 处理 Range 请求（支持视频拖动进度条）
    range_header = request.headers.get("Range", None)
    if range_header:
        # 解析 Range 头: "bytes=start-end"
        byte1, byte2 = 0, None
        range_match = re.search(r"bytes=(\d+)-(\d*)", range_header)
        if range_match:
            byte1 = int(range_match.group(1))
            if range_match.group(2):
                byte2 = int(range_match.group(2))

        if byte2 is None:
            byte2 = file_size - 1

        length = byte2 - byte1 + 1

        with open(file_path, "rb") as f:
            f.seek(byte1)
            data = f.read(length)

        resp = app.response_class(
            data,
            206,
            mimetype="video/mp4",
            headers={
                "Content-Range": f"bytes {byte1}-{byte2}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(length),
                "Cache-Control": "public, max-age=86400"
            }
        )
        return resp

    # 没有 Range 头，返回完整文件
    return send_file(
        file_path,
        mimetype="video/mp4",
        as_attachment=False,
        conditional=True
    )

@app.route("/api/achievements/image/<filename>")
def proxy_achievement_image(filename):
    """通过 API 网关提供成就图片访问"""
    safe_name = secure_filename(filename)
    if not safe_name:
        return "", 400
    file_path = os.path.join(DATA_DIR, "achievements", safe_name)
    if os.path.exists(file_path):
        return send_file(file_path)
    return "", 404


# ===== 文件下载服务 =====

@app.route("/data/files/<filename>")
def serve_download_file(filename):
    """提供文件下载"""
    safe_name = secure_filename(filename)
    if not safe_name:
        return "", 400

    files_dir = os.path.join(DATA_DIR, "files")
    file_path = os.path.join(files_dir, safe_name)

    if not os.path.exists(file_path):
        return "", 404

    return send_file(
        file_path,
        as_attachment=True,
        download_name=safe_name,
        conditional=True
    )

@app.route("/api/gallery/image/<filename>")
def serve_gallery_image(filename):
    """提供相册图片访问"""
    safe_name = secure_filename(filename)
    if not safe_name:
        return "", 400
    gallery_dir = os.path.join(DATA_DIR, "gallery")
    file_path = os.path.join(gallery_dir, safe_name)
    if os.path.exists(file_path):
        return send_file(file_path)
    return "", 404


# ===== 留言板 API =====

def sync_messages(data):
    messages_path = os.path.join(DATA_DIR, "messages.json")
    save_json(messages_path, data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("DELETE FROM messages")
    for item in data:
        encrypted, checksum = encrypt_data(item)
        c.execute("INSERT INTO messages (data_encrypted, checksum) VALUES (?, ?)", (encrypted, checksum))
    conn.commit()
    conn.close()
    log_audit("SYNC", "messages")
    return True

@app.route("/api/messages", methods=["GET", "POST"])
def handle_messages():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_messages(data)
        return jsonify({"status": "ok", "message": "留言已同步（JSON + 加密库）"})
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
        if not c.fetchone():
            conn.close()
            return jsonify(load_json(os.path.join(DATA_DIR, "messages.json"), []))
        c.execute("SELECT data_encrypted FROM messages ORDER BY id")
        rows = c.fetchall()
        conn.close()
        if rows:
            return jsonify([decrypt_data(r[0]) for r in rows])
        return jsonify(load_json(os.path.join(DATA_DIR, "messages.json"), []))


# ===== 友链 API =====

def sync_links(data):
    links_path = os.path.join(DATA_DIR, "links.json")
    save_json(links_path, data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("DELETE FROM links")
    for item in data:
        encrypted, checksum = encrypt_data(item)
        c.execute("INSERT INTO links (data_encrypted, checksum) VALUES (?, ?)", (encrypted, checksum))
    conn.commit()
    conn.close()
    log_audit("SYNC", "links")
    return True

@app.route("/api/links", methods=["GET", "POST"])
def handle_links():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_links(data)
        return jsonify({"status": "ok", "message": "友链已同步（JSON + 加密库）"})
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='links'")
        if not c.fetchone():
            conn.close()
            return jsonify(load_json(os.path.join(DATA_DIR, "links.json"), []))
        c.execute("SELECT data_encrypted FROM links ORDER BY id")
        rows = c.fetchall()
        conn.close()
        if rows:
            return jsonify([decrypt_data(r[0]) for r in rows])
        return jsonify(load_json(os.path.join(DATA_DIR, "links.json"), []))


# ===== 相册 API =====

def sync_gallery(data):
    gallery_path = os.path.join(DATA_DIR, "gallery.json")
    save_json(gallery_path, data)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS gallery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_encrypted TEXT NOT NULL,
            checksum TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("DELETE FROM gallery")
    for item in data:
        encrypted, checksum = encrypt_data(item)
        c.execute("INSERT INTO gallery (data_encrypted, checksum) VALUES (?, ?)", (encrypted, checksum))
    conn.commit()
    conn.close()
    log_audit("SYNC", "gallery")
    return True

@app.route("/api/gallery", methods=["GET", "POST"])
def handle_gallery():
    if request.method == "POST":
        data = request.get_json(force=True)
        sync_gallery(data)
        return jsonify({"status": "ok", "message": "相册已同步（JSON + 加密库）"})
    else:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='gallery'")
        if not c.fetchone():
            conn.close()
            return jsonify(load_json(os.path.join(DATA_DIR, "gallery.json"), []))
        c.execute("SELECT data_encrypted FROM gallery ORDER BY id")
        rows = c.fetchall()
        conn.close()
        if rows:
            return jsonify([decrypt_data(r[0]) for r in rows])
        return jsonify(load_json(os.path.join(DATA_DIR, "gallery.json"), []))


# ===== 启动 =====

if __name__ == "__main__":
    init_db()
    print(f"🔐 API 网关服务启动")
    print(f"   📁 加密密钥: {KEY_FILE}")
    print(f"   🗄️  加密数据库: {DB_PATH}")
    print(f"   📂 同步目录: {DATA_DIR}")
    print(f"   🌐 监听端口: 7000")
    print(f"   ⚡ 健康检查: http://localhost:7000/api/health")
    app.run(host="0.0.0.0", port=7000, debug=False)
