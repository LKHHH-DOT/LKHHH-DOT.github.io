---
name: vnc
description: 配置 x11vnc 服务，让手机通过 VNC 远程控制 Ubuntu 桌面。
---

# VNC 远程桌面配置 — 从零开始保姆级教程

> 适用场景：Ubuntu 22.04 系统，想用手机 VNC 客户端远程控制电脑桌面。
> 记录时间：2026-07-04（已实际验证成功）

---

## 背景知识：VNC 是怎么连接的？

```
┌─────────────┐       Tailscale 虚拟局域网       ┌──────────────┐
│  手机 VNC   │ ──────────────────────────────→  │  Ubuntu 电脑  │
│  (客户端)   │    连接地址:   │  (服务端) 
└─────────────┘                                   └──────────────┘
```

- **VNC 服务端** = 你的 Ubuntu 电脑（被控制端）
- **VNC 客户端** = 你的手机（控制端）
- **连接地址** = `Tailscale IP : 端口号`
  - Tailscale IP 是 Tailscale 给你电脑分配的虚拟 IP（类似局域网 IP）
  - 端口号 5900 是 VNC 服务的默认端口
  - **不是连域名，也不是连公网 IP，就是连 Tailscale IP**

---

## 第一步：安装 Tailscale（建立虚拟局域网）

> 手机和电脑必须在同一个 Tailscale 网络里才能连上。

### 1.1 电脑端安装 Tailscale

```bash
# 安装 Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# 启动并登录
sudo tailscale up
```
- 会弹出一个浏览器页面，用你的 Tailscale 账号登录
- 登录成功后，终端会显示：`Status: Connected`
- 查看你的 Tailscale IP：
  ```bash
  tailscale ip
  # 输出示例: 
  ```

### 1.2 手机端安装 Tailscale
- 去应用商店搜索 "Tailscale" 并安装
- 用同一个账号登录
- 登录后就能看到你电脑的 Tailscale IP

---

## 第二步：安装 x11vnc（VNC 服务端）

```bash
# 安装 x11vnc
sudo apt install -y x11vnc
```

验证安装成功：
```bash
x11vnc --version
# 输出示例: x11vnc: 0.9.16
```

---

## 第三步：设置 VNC 密码

```bash
# 设置密码（会交互式让你输入两次密码）
x11vnc -storepasswd
```


- 密码文件会自动生成到：`~/.vnc/passwd`

> ⚠️ 如果以后想改密码：
> ```bash
> x11vnc -storepasswd 新密码 ~/.vnc/passwd
> ```

---

## 第四步：解决端口冲突（最关键的一步！）

### 4.1 为什么会有这个问题？

Ubuntu 22.04 系统自带了 **GNOME 远程桌面服务**，它会占用 **5900 端口**。
而 x11vnc 也想用 5900 端口，结果 5900 被占用了，x11vnc 只能跳到 **5901 端口**。

但你的手机 VNC 客户端默认连的是 **5900**，所以一直连不上。

### 4.2 检查端口是否被占用

```bash
# 查看 5900 和 5901 端口被谁占了
ss -tlnp | grep -E '5900|5901'
```

如果看到这样的输出：
```
LISTEN 0      10    *:5900    *:*    users:(("gnome-remote-de",pid=3156,fd=30))
LISTEN 0      32    *:5901    *:*    users:(("x11vnc",pid=6213,fd=8))
```

说明：
- **5900** ← gnome-remote-desktop（系统自带的）
- **5901** ← x11vnc（被挤到 5901 了）

### 4.3 停用 GNOME 远程桌面

```bash
# 停掉它
systemctl --user stop gnome-remote-desktop.service

# 禁用开机自启（防止重启后又占端口）
systemctl --user disable gnome-remote-desktop.service
```

### 4.4 再次检查端口

```bash
ss -tlnp | grep 5900
```
应该没有输出了，说明 5900 端口已经释放。

---

## 第五步：启动 x11vnc

### 5.1 杀掉旧的 x11vnc 进程（如果有的话）

```bash
# 查看 x11vnc 进程
ps aux | grep x11vnc | grep -v grep

# 杀掉它（把 PID 换成实际的数字）
kill <PID>

# 或者简单粗暴全部杀掉
pkill x11vnc
```

### 5.2 启动 x11vnc（完整命令）

```bash
x11vnc -display :0 \
       -rfbauth /home/lazaxa/.vnc/passwd \
       -rfbport 5900 \
       -forever \
       -shared \
       -bg \
       -o /home/lazaxa/.vnc/x11vnc.log
```

> ⚠️ **关键参数解释**：
> - `-display :0` → 用当前桌面屏幕（就是你现在看到的这个桌面）
> - `-rfbauth ~/.vnc/passwd` → 用刚才设置的密码文件
> - `-rfbport 5900` → **强制用 5900 端口**（不加这个它可能又跳到 5901）
> - `-forever` → 手机断开后不退出，等着下次连接
> - `-shared` → 允许多个设备同时连
> - `-bg` → 后台运行（终端关掉也不影响）
> - `-o` → 日志文件位置

### 5.3 验证启动成功

```bash
ss -tlnp | grep 5900
```

应该看到：
```
LISTEN 0      32    *:5900    *:*    users:(("x11vnc",pid=XXXX,fd=8))
```

> ✅ 看到这个就说明 VNC 服务端已经成功跑起来了！

---

## 第六步：手机端连接

### 6.1 手机需要安装的软件

1. **Tailscale**（应用商店搜）
   - 用和电脑同一个账号登录
2. **VNC Viewer**（应用商店搜 "VNC Viewer" 或 "bVNC"）

### 6.2 连接步骤

1. 打开手机上的 **Tailscale**，确认已连接（显示 Connected）
2. 打开 **VNC Viewer**
3. 新建连接，填写：
   - **地址**: `
     - 前面是电脑的 Tailscale IP
     - 后面是端口号 5900
     - 中间用冒号隔开
   - **名称**: 随便填，比如 "我的电脑"
4. 点击连接
5. 输入密码：
6. ✅ 成功！现在你可以用手机控制电脑了

---

## 常见问题 FAQ

### Q1: 手机连不上，提示 Connection refused
**检查顺序**：
1. 电脑上有没有装 x11vnc？→ `which x11vnc`
2. x11vnc 有没有在运行？→ `ps aux | grep x11vnc`
3. 端口是不是 5900？→ `ss -tlnp | grep 5900`
4. 手机和电脑是不是同一个 Tailscale 网络？→ 手机 Tailscale 显示 Connected
5. Tailscale IP 对不对？→ 电脑上 `tailscale ip` 看一下

### Q2: 密码不对
```bash
# 重新设置密码
x11vnc -storepasswd 1 ~/.vnc/passwd
```

### Q3: 重启电脑后连不上了
每次重启后需要重新启动 x11vnc：
```bash
# 停掉 GNOME 远程桌面（重启后它又活了）
systemctl --user stop gnome-remote-desktop.service

# 启动 x11vnc
x11vnc -display :0 -rfbauth ~/.vnc/passwd -rfbport 5900 -forever -shared -bg
```

### Q4: 画面卡住不动或不更新
启动时加 `-noxdamage`：
```bash
x11vnc -display :0 -rfbauth ~/.vnc/passwd -rfbport 5900 -forever -shared -bg -noxdamage
```

---

## 一键启动脚本

把下面内容保存为 `~/start-vnc.sh`：

```bash
#!/bin/bash
# 停用 GNOME 远程桌面（释放 5900 端口）
systemctl --user stop gnome-remote-desktop.service 2>/dev/null
systemctl --user disable gnome-remote-desktop.service 2>/dev/null

# 杀掉旧 x11vnc
pkill -f "x11vnc" 2>/dev/null
sleep 1

# 启动 x11vnc
x11vnc -display :0 \
       -rfbauth /home/
       -rfbport 5900 \
       -forever \
       -shared \
       -bg \
       -o /home/lazaxa/.vnc/x11vnc.log

echo "VNC 服务已启动，端口 5900"
ss -tlnp | grep 5900
```

```bash
# 赋予执行权限
chmod +x ~/start-vnc.sh

# 以后重启了就运行这个
~/start-vnc.sh
```

---

## 完整命令速查表

| 目的 | 命令 |
|------|------|
| 安装 Tailscale | `curl -fsSL https://tailscale.com/install.sh \| sh` |
| 查看 Tailscale IP | `tailscale ip` |
| 安装 x11vnc | `sudo apt install -y x11vnc` |
| 设置 VNC 密码 | `x11vnc -storepasswd` |
| 停用 GNOME 远程桌面 | `systemctl --user stop gnome-remote-desktop.service` |
| 禁用开机自启 | `systemctl --user disable gnome-remote-desktop.service` |
| 启动 x11vnc | `x11vnc -display :0 -rfbauth ~/.vnc/passwd -rfbport 5900 -forever -shared -bg` |
| 查看 VNC 端口 | `ss -tlnp \| grep 5900` |
| 查看 VNC 日志 | `cat ~/.vnc/x11vnc.log` |
| 查看 x11vnc 进程 | `ps aux \| grep x11vnc` |
| 手机连接地址 | 
| VNC 密码 | |

---

## 核心概念一句话总结

> **VNC 连接 = 你的手机通过 Tailscale 虚拟局域网，连接到电脑的 5900 端口，输入密码后就能控制桌面。**
> 
> Tailscale IP 就像你电脑在虚拟局域网里的"门牌号"，5900 就是 VNC 服务的"门"。手机先通过 Tailscale 找到门牌号，再从 5900 这个门进去，输入密码就能进屋操作了。
