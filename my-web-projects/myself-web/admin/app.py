#!/usr/bin/env python3
"""
小熙 · 个人网站 内容管理系统 (CMS)
Flask 后端 — 所有数据读写均通过 API 网关 (port 7000)
确保管理后台与前台看到的数据完全一致
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import date
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = "xiao-xi-cms-secret-2026"


# 自定义 Jinja2 过滤器：escapejs
@app.template_filter("escapejs")
def escapejs_filter(s):
    """将字符串转义为 JavaScript 安全字符串"""
    if s is None:
        return ""
    s = str(s)
    s = s.replace("\\", "\\\\")
    s = s.replace("'", "\\'")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "\\r")
    s = s.replace("<", "\\u003C")
    s = s.replace(">", "\\u003E")
    return Markup(s)

# 数据文件路径（相对于项目根目录，仅用于网关不可用时的回退）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_PATH = os.path.join(BASE_DIR, "src", "data", "profile.json")
UPDATES_PATH = os.path.join(BASE_DIR, "src", "data", "updates.json")
ACHIEVEMENTS_PATH = os.path.join(BASE_DIR, "src", "data", "achievements.json")
DEPLOY_PATH = os.path.join(BASE_DIR, "src", "data", "deploy.json")
FILES_PATH = os.path.join(BASE_DIR, "src", "data", "files.json")
BLOGS_PATH = os.path.join(BASE_DIR, "src", "data", "blogs.json")
PROJECTS_PATH = os.path.join(BASE_DIR, "src", "data", "projects.json")
STATUS_PATH = os.path.join(BASE_DIR, "src", "data", "status.json")
ACHIEVEMENT_IMAGES_DIR = os.path.join(BASE_DIR, "src", "data", "achievements")

# API 网关地址
GATEWAY_URL = "http://localhost:7000"

# 允许的图片格式
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}


# ===== Slug 生成工具 =====

def generate_slug(text):
    """将中文标题转为英文 slug（拼音 + 英文）"""
    if not text:
        return f"achievement-{int(time.time())}"

    # 尝试用 pypinyin 转换中文为拼音
    try:
        from pypinyin import pinyin, Style
        slug_parts = []
        for char in text:
            if re.match(r'[\u4e00-\u9fff]', char):
                py = pinyin(char, style=Style.NORMAL)[0][0]
                slug_parts.append(py)
            elif re.match(r'[a-zA-Z0-9]', char):
                slug_parts.append(char.lower())
            elif char in ' _-':
                slug_parts.append('-')
        slug = '-'.join([p for p in slug_parts if p and p != '-'])
    except ImportError:
        # 没有 pypinyin，用简单方法：移除中文，保留英文数字
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')

    # 如果 slug 为空（纯中文），用时间戳
    if not slug:
        slug = f"achievement-{int(time.time())}"

    # 限制长度
    return slug[:60]


# ===== 图片上传工具 =====

def handle_upload_images(files):
    """处理图片上传，返回文件名列表"""
    saved = []
    for f in files:
        if f and f.filename:
            ext = os.path.splitext(f.filename)[1].lower()
            if ext in ALLOWED_IMAGE_EXTENSIONS:
                # 用时间戳+随机数生成唯一文件名
                ts = int(time.time() * 1000)
                safe_name = f"achieve-{ts}{ext}"
                save_path = os.path.join(ACHIEVEMENT_IMAGES_DIR, safe_name)
                f.save(save_path)
                saved.append(safe_name)
    return saved


# ===== API 网关调用工具 =====

def gateway_post(endpoint, data):
    """向 API 网关发送 POST 请求（JSON 数据）"""
    url = f"{GATEWAY_URL}{endpoint}"
    json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"⚠️  网关 {url} 不可用: {e}")
        return None
    except Exception as e:
        print(f"⚠️  网关请求异常: {e}")
        return None


def gateway_get(endpoint):
    """向 API 网关发送 GET 请求"""
    url = f"{GATEWAY_URL}{endpoint}"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        print(f"⚠️  网关 {url} 不可用: {e}")
        return None
    except Exception as e:
        print(f"⚠️  网关请求异常: {e}")
        return None


# ===== 数据读写工具（统一走网关）=====

def load_json(path, default=None):
    """安全加载 JSON 文件（回退用）"""
    if default is None:
        default = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    """保存 JSON 文件（回退用）"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


PROFILE_DEFAULTS = {
    "name": "", "nickname": "", "avatar": "",
    "title": "", "bio": "", "location": "",
    "contact": {"email": "", "github": "", "wechat": "", "twitter": "", "website": ""},
    "education": [],
    "skills": [],
    "interests": []
}


def get_profile():
    """优先从 API 网关读取 profile，网关不可用时回退到本地 JSON"""
    data = gateway_get("/api/profile")
    if data is not None:
        return data
    return load_json(PROFILE_PATH, PROFILE_DEFAULTS)


def get_updates():
    """优先从 API 网关读取 updates"""
    data = gateway_get("/api/updates")
    if data is not None:
        return data
    return load_json(UPDATES_PATH, [])


def get_achievements():
    """优先从 API 网关读取 achievements"""
    data = gateway_get("/api/achievements")
    if data is not None:
        return data
    return load_json(ACHIEVEMENTS_PATH, [])


def get_files():
    """优先从 API 网关读取 files"""
    data = gateway_get("/api/files")
    if data is not None:
        return data
    return load_json(FILES_PATH, [])


def get_blogs():
    """优先从 API 网关读取 blogs"""
    data = gateway_get("/api/blogs")
    if data is not None:
        return data
    return load_json(BLOGS_PATH, [])


def get_projects():
    """优先从 API 网关读取 projects"""
    data = gateway_get("/api/projects")
    if data is not None:
        return data
    return load_json(PROJECTS_PATH, [])


def get_status():
    """优先从 API 网关读取 status"""
    data = gateway_get("/api/status")
    if data is not None:
        return data
    return load_json(STATUS_PATH, [])


def get_deploy_config():
    return load_json(DEPLOY_PATH, {"local": True, "public": False})


def save_deploy_config(data):
    save_json(DEPLOY_PATH, data)


# ===== 路由：管理首页 =====

@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    profile = get_profile()
    updates = get_updates()
    achievements = get_achievements()
    deploy = get_deploy_config()
    return render_template("dashboard.html",
                           profile=profile,
                           updates=updates,
                           achievements=achievements,
                           deploy=deploy)


# ===== 个人信息管理 =====
# 注意：profile.html 有 3 个独立的 <form> 都 POST 到 /profile
# 每个表单只包含部分字段，所以必须从网关读取完整数据，
# 然后只覆盖表单中实际提交的字段，未提交的字段保持不变

@app.route("/profile", methods=["GET", "POST"])
def edit_profile():
    if request.method == "POST":
        # 1. 从网关读取当前完整数据
        profile = get_profile()

        # 2. 只覆盖表单中实际提交的字段
        # 基本信息（第一个表单）
        if request.form.get("name") is not None:
            profile["name"] = request.form.get("name", "")
        if request.form.get("nickname") is not None:
            profile["nickname"] = request.form.get("nickname", "")
        if request.form.get("title") is not None:
            profile["title"] = request.form.get("title", "")
        if request.form.get("bio") is not None:
            profile["bio"] = request.form.get("bio", "")
        if request.form.get("location") is not None:
            profile["location"] = request.form.get("location", "")

        # 联系方式（第二个表单）
        if request.form.get("contact_email") is not None:
            profile["contact"]["email"] = request.form.get("contact_email", "")
        if request.form.get("contact_github") is not None:
            profile["contact"]["github"] = request.form.get("contact_github", "")
        if request.form.get("contact_wechat") is not None:
            profile["contact"]["wechat"] = request.form.get("contact_wechat", "")
        if request.form.get("contact_twitter") is not None:
            profile["contact"]["twitter"] = request.form.get("contact_twitter", "")
        if request.form.get("contact_website") is not None:
            profile["contact"]["website"] = request.form.get("contact_website", "")

        # 技能与兴趣（第三个表单）
        if request.form.get("skills") is not None:
            skills_raw = request.form.get("skills", "")
            profile["skills"] = [s.strip() for s in skills_raw.split(",") if s.strip()]
        if request.form.get("interests") is not None:
            interests_raw = request.form.get("interests", "")
            profile["interests"] = [s.strip() for s in interests_raw.split(",") if s.strip()]

        # 3. 走 API 网关保存
        result = gateway_post("/api/profile", profile)
        if result:
            flash(f"✅ 个人信息已更新（已加密存储）", "success")
        else:
            save_json(PROFILE_PATH, profile)
            flash("✅ 个人信息已更新（本地模式）", "success")

        return redirect(url_for("dashboard"))

    profile = get_profile()
    return render_template("profile.html", profile=profile)


# ===== 教育经历管理 =====

@app.route("/education/add", methods=["POST"])
def add_education():
    profile = get_profile()
    profile.setdefault("education", [])
    profile["education"].append({
        "school": request.form.get("school", ""),
        "degree": request.form.get("degree", ""),
        "major": request.form.get("major", ""),
        "period": request.form.get("period", "")
    })
    result = gateway_post("/api/profile", profile)
    if result:
        flash(f"✅ 教育经历已添加（已加密存储）", "success")
    else:
        save_json(PROFILE_PATH, profile)
        flash("✅ 教育经历已添加（本地模式）", "success")
    return redirect(url_for("edit_profile"))


@app.route("/education/delete/<int:index>", methods=["POST"])
def delete_education(index):
    profile = get_profile()
    if 0 <= index < len(profile.get("education", [])):
        profile["education"].pop(index)
        result = gateway_post("/api/profile", profile)
        if result:
            flash(f"✅ 教育经历已删除（已加密存储）", "success")
        else:
            save_json(PROFILE_PATH, profile)
            flash("✅ 教育经历已删除（本地模式）", "success")
    return redirect(url_for("edit_profile"))


# ===== 动态更新管理 =====

@app.route("/updates")
def list_updates():
    updates = get_updates()
    return render_template("updates.html", updates=updates)


@app.route("/updates/add", methods=["POST"])
def add_update():
    updates = get_updates()
    tags_raw = request.form.get("tags", "")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    new_id = max([u["id"] for u in updates], default=0) + 1
    updates.append({
        "id": new_id,
        "date": request.form.get("date", str(date.today())),
        "title": request.form.get("title", ""),
        "content": request.form.get("content", ""),
        "tags": tags
    })
    result = gateway_post("/api/updates", updates)
    if result:
        flash(f"✅ 动态已发布（已加密存储）", "success")
    else:
        save_json(UPDATES_PATH, updates)
        flash("✅ 动态已发布（本地模式）", "success")
    return redirect(url_for("list_updates"))


@app.route("/updates/edit/<int:update_id>", methods=["POST"])
def edit_update(update_id):
    updates = get_updates()
    for item in updates:
        if item["id"] == update_id:
            tags_raw = request.form.get("tags", "")
            item["date"] = request.form.get("date", item["date"])
            item["title"] = request.form.get("title", item["title"])
            item["content"] = request.form.get("content", item["content"])
            item["tags"] = [t.strip() for t in tags_raw.split(",") if t.strip()]
            break
    result = gateway_post("/api/updates", updates)
    if result:
        flash(f"✅ 动态已更新（已加密存储）", "success")
    else:
        save_json(UPDATES_PATH, updates)
        flash("✅ 动态已更新（本地模式）", "success")
    return redirect(url_for("list_updates"))


@app.route("/updates/delete/<int:update_id>", methods=["POST"])
def delete_update(update_id):
    updates = get_updates()
    updates = [u for u in updates if u["id"] != update_id]
    result = gateway_post("/api/updates", updates)
    if result:
        flash(f"✅ 动态已删除（已加密存储）", "success")
    else:
        save_json(UPDATES_PATH, updates)
        flash("✅ 动态已删除（本地模式）", "success")
    return redirect(url_for("list_updates"))


# ===== 成就管理 =====

@app.route("/achievements")
def list_achievements():
    achievements = get_achievements()
    return render_template("achievements.html", achievements=achievements)


@app.route("/achievements/add", methods=["POST"])
def add_achievement():
    achievements = get_achievements()
    tags_raw = request.form.get("tags", "")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    new_id = max([a["id"] for a in achievements], default=0) + 1

    # 自动生成 slug
    title = request.form.get("title", "")
    slug = generate_slug(title)

    # 处理图片上传
    images = handle_upload_images(request.files.getlist("images"))

    new_item = {
        "id": new_id,
        "slug": slug,
        "date": request.form.get("date", ""),
        "title": title,
        "description": request.form.get("description", ""),
        "link": request.form.get("link", ""),
        "tags": tags,
        "images": images
    }
    achievements.append(new_item)
    result = gateway_post("/api/achievements", achievements)
    if result:
        flash(f"✅ 成就已添加（slug: {slug}）", "success")
    else:
        save_json(ACHIEVEMENTS_PATH, achievements)
        flash("✅ 成就已添加（本地模式）", "success")
    return redirect(url_for("list_achievements"))


@app.route("/achievements/edit/<int:achievement_id>", methods=["POST"])
def edit_achievement(achievement_id):
    achievements = get_achievements()
    for item in achievements:
        if item["id"] == achievement_id:
            tags_raw = request.form.get("tags", "")
            item["date"] = request.form.get("date", item["date"])
            new_title = request.form.get("title", item["title"])
            if new_title != item["title"]:
                item["title"] = new_title
                item["slug"] = generate_slug(new_title)
            item["description"] = request.form.get("description", item["description"])
            item["link"] = request.form.get("link", item["link"])
            item["tags"] = [t.strip() for t in tags_raw.split(",") if t.strip()]

            # 处理图片上传（追加）
            new_images = handle_upload_images(request.files.getlist("images"))
            if new_images:
                item.setdefault("images", [])
                item["images"].extend(new_images)

            # 删除指定图片
            delete_images_str = request.form.get("delete_images", "")
            if delete_images_str and item.get("images"):
                delete_list = [x.strip() for x in delete_images_str.split(",") if x.strip()]
                item["images"] = [img for img in item["images"] if img not in delete_list]
                # 同时删除物理文件
                for img_name in delete_list:
                    img_path = os.path.join(ACHIEVEMENT_IMAGES_DIR, img_name)
                    if os.path.exists(img_path):
                        os.remove(img_path)

            break
    result = gateway_post("/api/achievements", achievements)
    if result:
        flash(f"✅ 成就已更新（已加密存储）", "success")
    else:
        save_json(ACHIEVEMENTS_PATH, achievements)
        flash("✅ 成就已更新（本地模式）", "success")
    return redirect(url_for("list_achievements"))


@app.route("/achievements/delete/<int:achievement_id>", methods=["POST"])
def delete_achievement(achievement_id):
    achievements = get_achievements()
    achievements = [a for a in achievements if a["id"] != achievement_id]
    result = gateway_post("/api/achievements", achievements)
    if result:
        flash(f"✅ 成就已删除（已加密存储）", "success")
    else:
        save_json(ACHIEVEMENTS_PATH, achievements)
        flash("✅ 成就已删除（本地模式）", "success")
    return redirect(url_for("list_achievements"))


# ===== 文件分享管理 =====

@app.route("/files")
def list_files():
    files = get_files()
    return render_template("files.html", files=files)


@app.route("/files/add", methods=["POST"])
def add_file():
    files = get_files()
    new_id = max([f["id"] for f in files], default=0) + 1

    name = request.form.get("name", "")
    file_type = request.form.get("type", "other")
    size = request.form.get("size", "")
    description = request.form.get("description", "")
    url = request.form.get("url", "")

    # 处理文件上传
    uploaded_file = request.files.get("local_file")
    if uploaded_file and uploaded_file.filename:
        files_dir = os.path.join(BASE_DIR, "src", "data", "files")
        os.makedirs(files_dir, exist_ok=True)
        safe_name = secure_filename(uploaded_file.filename)
        file_path = os.path.join(files_dir, safe_name)
        uploaded_file.save(file_path)

        # 自动计算文件大小
        file_size_bytes = os.path.getsize(file_path)
        if file_size_bytes < 1024:
            size = f"{file_size_bytes} B"
        elif file_size_bytes < 1024 * 1024:
            size = f"{file_size_bytes / 1024:.1f} KB"
        else:
            size = f"{file_size_bytes / 1024 / 1024:.1f} MB"

        # 自动检测文件类型
        ext = safe_name.rsplit(".", 1)[-1].lower() if "." in safe_name else ""
        type_map = {
            "pdf": "pdf", "md": "md", "markdown": "md",
            "zip": "zip", "rar": "zip", "7z": "zip", "tar": "zip", "gz": "zip",
            "mp4": "video", "webm": "video", "avi": "video", "mov": "video",
            "txt": "other", "json": "other", "yaml": "other", "yml": "other",
            "go": "other", "py": "other", "js": "other", "ts": "other",
            "doc": "doc", "docx": "doc", "xls": "xls", "xlsx": "xls",
            "jpg": "image", "jpeg": "image", "png": "image", "gif": "image",
            "mp3": "audio", "wav": "audio", "flac": "audio",
        }
        if file_type == "other" and ext in type_map:
            file_type = type_map[ext]

        # url 使用相对路径
        url = safe_name

    files.append({
        "id": new_id,
        "name": name,
        "type": file_type,
        "size": size,
        "description": description,
        "url": url
    })
    result = gateway_post("/api/files", files)
    if result:
        flash(f"✅ 文件「{name}」已添加", "success")
    else:
        save_json(FILES_PATH, files)
        flash("✅ 文件已添加（本地模式）", "success")
    return redirect(url_for("list_files"))


@app.route("/files/edit/<int:file_id>", methods=["POST"])
def edit_file(file_id):
    files = get_files()

    # 处理上传替换文件
    uploaded_file = request.files.get("local_file")
    new_url = None
    if uploaded_file and uploaded_file.filename:
        files_dir = os.path.join(BASE_DIR, "src", "data", "files")
        os.makedirs(files_dir, exist_ok=True)
        safe_name = secure_filename(uploaded_file.filename)
        file_path = os.path.join(files_dir, safe_name)
        uploaded_file.save(file_path)
        new_url = safe_name

        # 自动计算文件大小
        file_size_bytes = os.path.getsize(file_path)
        if file_size_bytes < 1024:
            size = f"{file_size_bytes} B"
        elif file_size_bytes < 1024 * 1024:
            size = f"{file_size_bytes / 1024:.1f} KB"
        else:
            size = f"{file_size_bytes / 1024 / 1024:.1f} MB"

    for item in files:
        if item["id"] == file_id:
            item["name"] = request.form.get("name", item["name"])
            item["type"] = request.form.get("type", item["type"])
            item["size"] = request.form.get("size", item["size"])
            item["description"] = request.form.get("description", item["description"])
            item["url"] = request.form.get("url", item["url"])
            # 如果上传了新文件，更新 url 和 size
            if new_url:
                # 删除旧文件
                old_url = item.get("url", "")
                if old_url and not old_url.startswith("http"):
                    old_path = os.path.join(BASE_DIR, "src", "data", "files", old_url)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                item["url"] = new_url
                item["size"] = size
            break
    result = gateway_post("/api/files", files)
    if result:
        flash(f"✅ 文件已更新", "success")
    else:
        save_json(FILES_PATH, files)
        flash("✅ 文件已更新（本地模式）", "success")
    return redirect(url_for("list_files"))


@app.route("/files/delete/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    files = get_files()

    # 找到要删除的文件，同时删除本地文件
    deleted_name = ""
    for item in files:
        if item["id"] == file_id:
            deleted_name = item.get("name", "")
            local_url = item.get("url", "")
            # 如果是本地文件（不是 http 开头），尝试删除
            if local_url and not local_url.startswith("http"):
                local_path = os.path.join(BASE_DIR, "src", "data", "files", local_url)
                if os.path.exists(local_path):
                    os.remove(local_path)
            break

    files = [f for f in files if f["id"] != file_id]
    result = gateway_post("/api/files", files)
    if result:
        flash(f"✅ 文件「{deleted_name}」已删除", "success")
    else:
        save_json(FILES_PATH, files)
        flash("✅ 文件已删除（本地模式）", "success")
    return redirect(url_for("list_files"))


# ===== 部署配置 =====

@app.route("/deploy", methods=["GET", "POST"])
def deploy_config():
    if request.method == "POST":
        config = {
            "local": request.form.get("local") == "on",
            "public": request.form.get("public") == "on"
        }
        save_deploy_config(config)
        flash("✅ 部署配置已更新", "success")
        return redirect(url_for("dashboard"))
    deploy = get_deploy_config()
    return render_template("deploy.html", deploy=deploy)


# ===== 静态文件服务（成就图片）=====

@app.route("/data/achievements/<filename>")
def serve_achievement_image(filename):
    """提供成就图片的静态访问"""
    safe_name = secure_filename(filename)
    file_path = os.path.join(ACHIEVEMENT_IMAGES_DIR, safe_name)
    if os.path.exists(file_path):
        return send_file(file_path)
    return "", 404


# ===== 成就详情预览（管理后台预览用）=====

@app.route("/achievement/<slug>")
def preview_achievement(slug):
    """预览成就详情页"""
    achievements = get_achievements()
    item = None
    for a in achievements:
        if a.get("slug") == slug:
            item = a
            break
    if not item:
        # 兼容旧数据（无 slug）
        for a in achievements:
            if a.get("id") == slug:
                item = a
                break
    if not item:
        return "成就未找到", 404
    return render_template("achievement_detail.html", achievement=item)


# ===== 博客管理 =====

@app.route("/admin/blogs")
def list_blogs():
    blogs = get_blogs()
    from datetime import date
    return render_template("blogs.html", blogs=blogs, today=str(date.today()))


@app.route("/admin/blogs/add", methods=["POST"])
def add_blog():
    blogs = get_blogs()
    new_id = max([b["id"] for b in blogs], default=0) + 1
    title = request.form.get("title", "")
    slug = request.form.get("slug", "").strip()
    if not slug:
        slug = generate_slug(title)
    tags_raw = request.form.get("tags", "")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    blogs.append({
        "id": new_id,
        "title": title,
        "summary": request.form.get("summary", ""),
        "date": request.form.get("date", str(date.today())),
        "tags": tags,
        "content": request.form.get("content", ""),
        "slug": slug
    })
    result = gateway_post("/api/blogs", blogs)
    if result:
        flash(f"✅ 博客「{title}」已发布（已加密存储）", "success")
    else:
        save_json(BLOGS_PATH, blogs)
        flash("✅ 博客已发布（本地模式）", "success")
    return redirect(url_for("list_blogs"))


@app.route("/admin/blogs/edit/<int:blog_id>", methods=["GET", "POST"])
def edit_blog(blog_id):
    blogs = get_blogs()
    blog = None
    for b in blogs:
        if b["id"] == blog_id:
            blog = b
            break
    if not blog:
        flash("❌ 博客未找到", "error")
        return redirect(url_for("list_blogs"))

    if request.method == "POST":
        title = request.form.get("title", blog["title"])
        slug = request.form.get("slug", "").strip()
        if not slug:
            slug = blog.get("slug", generate_slug(title))
        tags_raw = request.form.get("tags", "")
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        blog["title"] = title
        blog["summary"] = request.form.get("summary", blog["summary"])
        blog["date"] = request.form.get("date", blog["date"])
        blog["tags"] = tags
        blog["content"] = request.form.get("content", blog["content"])
        blog["slug"] = slug
        result = gateway_post("/api/blogs", blogs)
        if result:
            flash(f"✅ 博客「{title}」已更新（已加密存储）", "success")
        else:
            save_json(BLOGS_PATH, blogs)
            flash("✅ 博客已更新（本地模式）", "success")
        return redirect(url_for("list_blogs"))

    return render_template("blog_edit.html", blog=blog)


@app.route("/admin/blogs/delete/<int:blog_id>", methods=["POST"])
def delete_blog(blog_id):
    blogs = get_blogs()
    deleted_title = ""
    for b in blogs:
        if b["id"] == blog_id:
            deleted_title = b.get("title", "")
            break
    blogs = [b for b in blogs if b["id"] != blog_id]
    result = gateway_post("/api/blogs", blogs)
    if result:
        flash(f"✅ 博客「{deleted_title}」已删除（已加密存储）", "success")
    else:
        save_json(BLOGS_PATH, blogs)
        flash("✅ 博客已删除（本地模式）", "success")
    return redirect(url_for("list_blogs"))


# ===== 项目管理 =====

@app.route("/admin/projects")
def list_projects():
    projects = get_projects()
    return render_template("projects.html", projects=projects)


@app.route("/admin/projects/add", methods=["POST"])
def add_project():
    projects = get_projects()
    new_id = max([p["id"] for p in projects], default=0) + 1
    tech_raw = request.form.get("tech", "")
    tech = [t.strip() for t in tech_raw.split(",") if t.strip()]
    projects.append({
        "id": new_id,
        "title": request.form.get("title", ""),
        "description": request.form.get("description", ""),
        "tech": tech,
        "link": request.form.get("link", ""),
        "github": request.form.get("github", ""),
        "image": request.form.get("image", ""),
        "status": request.form.get("status", "进行中")
    })
    result = gateway_post("/api/projects", projects)
    if result:
        flash(f"✅ 项目已添加（已加密存储）", "success")
    else:
        save_json(PROJECTS_PATH, projects)
        flash("✅ 项目已添加（本地模式）", "success")
    return redirect(url_for("list_projects"))


@app.route("/admin/projects/edit/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    projects = get_projects()
    project = None
    for p in projects:
        if p["id"] == project_id:
            project = p
            break
    if not project:
        flash("❌ 项目未找到", "error")
        return redirect(url_for("list_projects"))

    if request.method == "POST":
        tech_raw = request.form.get("tech", "")
        tech = [t.strip() for t in tech_raw.split(",") if t.strip()]
        project["title"] = request.form.get("title", project["title"])
        project["description"] = request.form.get("description", project["description"])
        project["tech"] = tech
        project["link"] = request.form.get("link", project["link"])
        project["github"] = request.form.get("github", project["github"])
        project["image"] = request.form.get("image", project["image"])
        project["status"] = request.form.get("status", project["status"])
        result = gateway_post("/api/projects", projects)
        if result:
            flash(f"✅ 项目已更新（已加密存储）", "success")
        else:
            save_json(PROJECTS_PATH, projects)
            flash("✅ 项目已更新（本地模式）", "success")
        return redirect(url_for("list_projects"))

    return render_template("project_edit.html", project=project)


@app.route("/admin/projects/delete/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    projects = get_projects()
    deleted_title = ""
    for p in projects:
        if p["id"] == project_id:
            deleted_title = p.get("title", "")
            break
    projects = [p for p in projects if p["id"] != project_id]
    result = gateway_post("/api/projects", projects)
    if result:
        flash(f"✅ 项目「{deleted_title}」已删除（已加密存储）", "success")
    else:
        save_json(PROJECTS_PATH, projects)
        flash("✅ 项目已删除（本地模式）", "success")
    return redirect(url_for("list_projects"))


# ===== 状态管理 =====

@app.route("/admin/status")
def list_status():
    status_list = get_status()
    from datetime import date
    return render_template("status.html", status_list=status_list, today=str(date.today()))


@app.route("/admin/status/add", methods=["POST"])
def add_status():
    status_list = get_status()
    new_id = max([s["id"] for s in status_list], default=0) + 1
    status_list.append({
        "id": new_id,
        "title": request.form.get("title", ""),
        "icon": request.form.get("icon", ""),
        "date": request.form.get("date", str(date.today())),
        "detail": request.form.get("detail", "")
    })
    result = gateway_post("/api/status", status_list)
    if result:
        flash(f"✅ 状态已添加（已加密存储）", "success")
    else:
        save_json(STATUS_PATH, status_list)
        flash("✅ 状态已添加（本地模式）", "success")
    return redirect(url_for("list_status"))


@app.route("/admin/status/edit/<int:status_id>", methods=["GET", "POST"])
def edit_status(status_id):
    status_list = get_status()
    status_item = None
    for s in status_list:
        if s["id"] == status_id:
            status_item = s
            break
    if not status_item:
        flash("❌ 状态未找到", "error")
        return redirect(url_for("list_status"))

    if request.method == "POST":
        status_item["title"] = request.form.get("title", status_item["title"])
        status_item["icon"] = request.form.get("icon", status_item.get("icon", ""))
        status_item["date"] = request.form.get("date", status_item["date"])
        status_item["detail"] = request.form.get("detail", status_item.get("detail", ""))
        result = gateway_post("/api/status", status_list)
        if result:
            flash(f"✅ 状态已更新（已加密存储）", "success")
        else:
            save_json(STATUS_PATH, status_list)
            flash("✅ 状态已更新（本地模式）", "success")
        return redirect(url_for("list_status"))

    return render_template("status_edit.html", status_item=status_item)


@app.route("/admin/status/delete/<int:status_id>", methods=["POST"])
def delete_status(status_id):
    status_list = get_status()
    deleted_title = ""
    for s in status_list:
        if s["id"] == status_id:
            deleted_title = s.get("title", "")
            break
    status_list = [s for s in status_list if s["id"] != status_id]
    result = gateway_post("/api/status", status_list)
    if result:
        flash(f"✅ 状态「{deleted_title}」已删除（已加密存储）", "success")
    else:
        save_json(STATUS_PATH, status_list)
        flash("✅ 状态已删除（本地模式）", "success")
    return redirect(url_for("list_status"))


# ===== 留言管理 =====

MESSAGES_PATH = os.path.join(BASE_DIR, "src", "data", "messages.json")

def get_messages():
    result = gateway_get("/api/messages")
    if result is not None:
        return result
    return load_json(MESSAGES_PATH, [])

@app.route("/admin/messages")
def list_messages():
    messages = get_messages()
    # 按时间倒序
    messages.sort(key=lambda x: x.get("date", ""), reverse=True)
    return render_template("messages.html", messages=messages)

@app.route("/admin/messages/reply/<int:msg_id>", methods=["POST"])
def reply_message(msg_id):
    reply_text = request.form.get("reply", "").strip()
    messages = get_messages()
    for msg in messages:
        if msg["id"] == msg_id:
            msg["reply"] = reply_text
            break
    result = gateway_post("/api/messages", messages)
    if result:
        flash("✅ 回复已保存", "success")
    else:
        save_json(MESSAGES_PATH, messages)
        flash("✅ 回复已保存（本地模式）", "success")
    return redirect(url_for("list_messages"))

@app.route("/admin/messages/approve/<int:msg_id>", methods=["POST"])
def approve_message(msg_id):
    messages = get_messages()
    for msg in messages:
        if msg["id"] == msg_id:
            msg["is_approved"] = not msg.get("is_approved", False)
            break
    result = gateway_post("/api/messages", messages)
    if result:
        flash("✅ 审核状态已更新", "success")
    else:
        save_json(MESSAGES_PATH, messages)
        flash("✅ 审核状态已更新（本地模式）", "success")
    return redirect(url_for("list_messages"))

@app.route("/admin/messages/delete/<int:msg_id>", methods=["POST"])
def delete_message(msg_id):
    messages = get_messages()
    deleted_name = ""
    for msg in messages:
        if msg["id"] == msg_id:
            deleted_name = msg.get("name", "")
            break
    messages = [m for m in messages if m["id"] != msg_id]
    result = gateway_post("/api/messages", messages)
    if result:
        flash(f"✅ 留言「{deleted_name}」已删除", "success")
    else:
        save_json(MESSAGES_PATH, messages)
        flash("✅ 留言已删除（本地模式）", "success")
    return redirect(url_for("list_messages"))


# ===== 友链管理 =====

LINKS_PATH = os.path.join(BASE_DIR, "src", "data", "links.json")

def get_links():
    result = gateway_get("/api/links")
    if result is not None:
        return result
    return load_json(LINKS_PATH, [])

@app.route("/admin/links")
def list_links():
    links = get_links()
    return render_template("links.html", links=links)

@app.route("/admin/links/add", methods=["POST"])
def add_link():
    name = request.form.get("name", "").strip()
    url = request.form.get("url", "").strip()
    description = request.form.get("description", "").strip()
    icon = request.form.get("icon", "").strip()

    if not name or not url:
        flash("❌ 名称和链接不能为空", "error")
        return redirect(url_for("list_links"))

    links = get_links()
    new_id = max([l.get("id", 0) for l in links], default=0) + 1
    links.append({
        "id": new_id,
        "name": name,
        "url": url,
        "description": description,
        "icon": icon
    })

    result = gateway_post("/api/links", links)
    if result:
        flash(f"✅ 友链「{name}」已添加", "success")
    else:
        save_json(LINKS_PATH, links)
        flash("✅ 友链已添加（本地模式）", "success")
    return redirect(url_for("list_links"))

@app.route("/admin/links/edit/<int:link_id>", methods=["POST"])
def edit_link(link_id):
    name = request.form.get("name", "").strip()
    url = request.form.get("url", "").strip()
    description = request.form.get("description", "").strip()
    icon = request.form.get("icon", "").strip()

    links = get_links()
    for link in links:
        if link["id"] == link_id:
            if name: link["name"] = name
            if url: link["url"] = url
            link["description"] = description
            link["icon"] = icon
            break

    result = gateway_post("/api/links", links)
    if result:
        flash("✅ 友链已更新", "success")
    else:
        save_json(LINKS_PATH, links)
        flash("✅ 友链已更新（本地模式）", "success")
    return redirect(url_for("list_links"))

@app.route("/admin/links/delete/<int:link_id>", methods=["POST"])
def delete_link(link_id):
    links = get_links()
    deleted_name = ""
    for l in links:
        if l["id"] == link_id:
            deleted_name = l.get("name", "")
            break
    links = [l for l in links if l["id"] != link_id]
    result = gateway_post("/api/links", links)
    if result:
        flash(f"✅ 友链「{deleted_name}」已删除", "success")
    else:
        save_json(LINKS_PATH, links)
        flash("✅ 友链已删除（本地模式）", "success")
    return redirect(url_for("list_links"))


# ===== 相册管理 =====

GALLERY_PATH = os.path.join(BASE_DIR, "src", "data", "gallery.json")

def get_gallery():
    result = gateway_get("/api/gallery")
    if result is not None:
        return result
    return load_json(GALLERY_PATH, [])

@app.route("/admin/gallery")
def list_gallery():
    albums = get_gallery()
    return render_template("gallery.html", albums=albums)

@app.route("/admin/gallery/add", methods=["POST"])
def add_album():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        flash("❌ 相册名称不能为空", "error")
        return redirect(url_for("list_gallery"))

    albums = get_gallery()
    new_id = max([a.get("id", 0) for a in albums], default=0) + 1
    albums.append({
        "id": new_id,
        "title": title,
        "description": description,
        "images": []
    })

    result = gateway_post("/api/gallery", albums)
    if result:
        flash(f"✅ 相册「{title}」已创建", "success")
    else:
        save_json(GALLERY_PATH, albums)
        flash("✅ 相册已创建（本地模式）", "success")
    return redirect(url_for("list_gallery"))

@app.route("/admin/gallery/edit/<int:album_id>", methods=["POST"])
def edit_album(album_id):
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    albums = get_gallery()
    for album in albums:
        if album["id"] == album_id:
            if title: album["title"] = title
            album["description"] = description
            break

    result = gateway_post("/api/gallery", albums)
    if result:
        flash("✅ 相册已更新", "success")
    else:
        save_json(GALLERY_PATH, albums)
        flash("✅ 相册已更新（本地模式）", "success")
    return redirect(url_for("list_gallery"))

@app.route("/admin/gallery/delete/<int:album_id>", methods=["POST"])
def delete_album(album_id):
    albums = get_gallery()
    deleted_title = ""
    for a in albums:
        if a["id"] == album_id:
            deleted_title = a.get("title", "")
            break
    albums = [a for a in albums if a["id"] != album_id]
    result = gateway_post("/api/gallery", albums)
    if result:
        flash(f"✅ 相册「{deleted_title}」已删除", "success")
    else:
        save_json(GALLERY_PATH, albums)
        flash("✅ 相册已删除（本地模式）", "success")
    return redirect(url_for("list_gallery"))

@app.route("/admin/gallery/upload_image/<int:album_id>", methods=["POST"])
def upload_gallery_image(album_id):
    if "image" not in request.files:
        flash("❌ 请选择图片", "error")
        return redirect(url_for("list_gallery"))

    file = request.files["image"]
    if file.filename == "":
        flash("❌ 请选择图片", "error")
        return redirect(url_for("list_gallery"))

    title = request.form.get("title", "").strip()
    caption = request.form.get("caption", "").strip()

    # 保存图片到 data/gallery 目录
    gallery_images_dir = os.path.join(BASE_DIR, "src", "data", "gallery")
    os.makedirs(gallery_images_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    # 添加时间戳防止重名
    name_parts = filename.rsplit(".", 1)
    if len(name_parts) > 1:
        filename = f"{name_parts[0]}_{int(time.time())}.{name_parts[1]}"
    file.save(os.path.join(gallery_images_dir, filename))

    albums = get_gallery()
    for album in albums:
        if album["id"] == album_id:
            album["images"].append({
                "url": f"/api/gallery/image/{filename}",
                "title": title,
                "caption": caption
            })
            break

    result = gateway_post("/api/gallery", albums)
    if result:
        flash("✅ 图片已上传", "success")
    else:
        save_json(GALLERY_PATH, albums)
        flash("✅ 图片已上传（本地模式）", "success")
    return redirect(url_for("list_gallery"))

@app.route("/admin/gallery/delete_image/<int:album_id>/<int:image_index>", methods=["POST"])
def delete_gallery_image(album_id, image_index):
    albums = get_gallery()
    for album in albums:
        if album["id"] == album_id:
            if 0 <= image_index < len(album["images"]):
                album["images"].pop(image_index)
            break

    result = gateway_post("/api/gallery", albums)
    if result:
        flash("✅ 图片已删除", "success")
    else:
        save_json(GALLERY_PATH, albums)
        flash("✅ 图片已删除（本地模式）", "success")
    return redirect(url_for("list_gallery"))


# ===== 启动 =====

if __name__ == "__main__":
    print(f"📝 CMS 管理后台启动")
    print(f"   🌐 监听端口: 5000")
    print(f"   🔗 API 网关: {GATEWAY_URL}")
    print(f"   ⚡ 管理界面: http://localhost:5000/")
    app.run(host="0.0.0.0", port=5000, debug=False)
