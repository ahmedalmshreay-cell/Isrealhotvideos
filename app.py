import os
import json
import time
from flask import Flask, render_template_string, request, jsonify, make_response

app = Flask(__name__)

STATS_FILE = "stats.json"
TELEGRAM_LINK = "https://t.me/+dnhsq9fuecplOWQ0"

# الروابط المباشرة (Adsterra Smartlinks) - تُوزع بالتناوب على الضغطة الأولى لكل فيديو
DIRECT_AD_LINKS = [
    "https://auctionr.org/4/6bfa19f83ac495ec2ead3fa087d1f215",
    "https://auctionr.org/4/ebab6f78fa29a191514fed00aa160ace",
    "https://auctionr.org/4/67d3ead71b308f8710ec2a37290e7035"
]

# 1. الدفعة الأحدث من روابط qu.ax (تظهر أولاً في مقدمة الموقع)
LATEST_QUAX_CODES = [
    "IRdHn", "RKBPR", "bozyS", "CfhhS", "cxy2B", "TlfK6",
    "oF1mL", "FAoC4", "BFgUd", "RV3JK", "G0gpv", "N1LyN",
    "tsvu1", "6vShZ", "1jhfl", "buk9U", "QalSJ", "munzd"
]

# 2. الدفعة السابقة من روابط qu.ax (مع استبعاد المكرر تلقائياً)
PREVIOUS_QUAX_CODES = [
    "FDtnb", "qcZNk", "cOjTP", "RgLKI", "f7HEc", "QusqT", "oudjw",
    "78MO1", "p384b", "fMr2e", "LweOe", "lRKRZ", "AjwWg", "tqOoV",
    "DLF95", "7WK7s", "Qqlfz", "zoQc4", "ml7Cw", "f9ezf"
]

# 3. الروابط الأساسية القديمة
OLD_QUAX_CODES = [
    "Pnsw8", "o9g5C", "g42Cw", "XfZ5S", "gHaSb", "8grcz", "pC5qM",
    "V05Ea", "NJbib", "QNrxc", "UOhgX", "R1GKd", "CNyPh", "664TP"
]

# دمج جميع الأكواد بالترتيب مع منع أي تكرار
ALL_CODES = []
for code in (LATEST_QUAX_CODES + PREVIOUS_QUAX_CODES + OLD_QUAX_CODES):
    if code not in ALL_CODES:
        ALL_CODES.append(code)

ALL_URLS = [f"https://qu.ax/{code}.mp4" for code in ALL_CODES]

# نظام تتبع الزوار المتواجدين حالياً في الموقع (Real-Time Active Users)
ACTIVE_SESSIONS = {}

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_stats(data):
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass

VIDEO_STATS = load_stats()

# تجهيز قائمة الفيديوهات بنظام الأرشيف الذكي والوسوم وتوزيع الروابط المباشرة
def get_videos_list():
    total = len(ALL_URLS)
    categories = ["vip", "hot", "cam"]
    badges = ["VIP 💎", "בלעדי 🔥", "חדש 🆕", "HD 🎬"]
    tags_pool = [
        ["#בלעדי", "#ישראל", "#VIP"],
        ["#תיעוד_פרטי", "#חם", "#HD"],
        ["#הדלפה", "#טלגרם", "#18plus"],
        ["#ארכיון_VIP", "#ישראליות", "#ללא_צנזורה"]
    ]
    
    videos = []
    for idx, url in enumerate(ALL_URLS):
        vid_id = f"vid_{idx + 1}"
        archive_num = 100 + (total - idx)
        
        if vid_id not in VIDEO_STATS:
            VIDEO_STATS[vid_id] = {"views": 0, "likes": 0}
            
        cat = "vip" if idx < len(LATEST_QUAX_CODES) else categories[idx % len(categories)]
        badge = "חדש 🆕" if idx < len(LATEST_QUAX_CODES) else badges[idx % len(badges)]
        direct_ad = DIRECT_AD_LINKS[idx % len(DIRECT_AD_LINKS)]
        
        videos.append({
            "id": vid_id,
            "url": url,
            "direct_ad": direct_ad,
            "archive_title": f"תיעוד בלעדי #{archive_num} • ארכיון VIP",
            "tags": tags_pool[idx % len(tags_pool)],
            "category": cat,
            "badge": badge,
            "views": VIDEO_STATS[vid_id]["views"],
            "likes": VIDEO_STATS[vid_id]["likes"]
        })
    return videos

# مسارات API للإحصائيات الحقيقية
@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    data = request.get_json(silent=True) or {}
    sid = data.get("sid")
    now = time.time()
    
    if sid:
        ACTIVE_SESSIONS[sid] = now
        
    expired = [k for k, v in ACTIVE_SESSIONS.items() if now - v > 40]
    for k in expired:
        del ACTIVE_SESSIONS[k]
        
    online_count = max(1, len(ACTIVE_SESSIONS))
    return jsonify({"online": online_count})

@app.route('/api/view/<vid_id>', methods=['POST'])
def add_view(vid_id):
    if vid_id not in VIDEO_STATS:
        VIDEO_STATS[vid_id] = {"views": 0, "likes": 0}
    VIDEO_STATS[vid_id]["views"] += 1
    save_stats(VIDEO_STATS)
    return jsonify({"views": VIDEO_STATS[vid_id]["views"]})

@app.route('/api/like/<vid_id>', methods=['POST'])
def toggle_like(vid_id):
    data = request.get_json(silent=True) or {}
    action = data.get("action", "like")
    
    if vid_id not in VIDEO_STATS:
        VIDEO_STATS[vid_id] = {"views": 0, "likes": 0}
        
    if action == "like":
        VIDEO_STATS[vid_id]["likes"] += 1
    else:
        VIDEO_STATS[vid_id]["likes"] = max(0, VIDEO_STATS[vid_id]["likes"] - 1)
        
    save_stats(VIDEO_STATS)
    return jsonify({"likes": VIDEO_STATS[vid_id]["likes"]})

HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ISRAFLIX VIP | ארכיון הסרטונים הבלעדי בישראל 18+</title>
    
    <!-- Google Fonts: Heebo -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;900&display=swap" rel="stylesheet">

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-0H10SJLG8Y"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-0H10SJLG8Y');
    </script>

    <!-- SEO & Social Metadata -->
    <meta name="description" content="ISRAFLIX VIP - ארכיון הסרטונים החמים והבלעדיים בישראל 18+. הדלפות נדירות, תיעודים פרטיים וקבוצות VIP בטלגרם.">
    <meta name="keywords" content="סרטונים חמים בישראל, נשים ישראליות, קבוצות ישראל, סרטונים 18, סרטונים בלעדיים, קבוצות VIP טלגרם, ISRAFLIX">
    <meta name="robots" content="index, follow">
    <meta name="theme-color" content="#09090b">

    <meta property="og:title" content="ISRAFLIX VIP | ארכיון הסרטונים הבלעדי בישראל">
    <meta property="og:description" content="צפו בהדלפות החמות ביותר ובסרטונים הבלעדיים בישראל באיכות HD.">
    <meta property="og:image" content="https://files.catbox.moe/c5lwce.jpg">
    <meta property="og:type" content="website">

    <!-- Adsterra Popunder Script -->
    <script data-cfasync="false" src="https://4xfreedom.com/1/10753c745a27f2bf8e0d5b0bbc0697d9"></script>

    <style>
        :root {
            --bg-main: #09090b;
            --bg-card: #121215;
            --bg-elevated: #1c1c21;
            --border-color: #27272a;
            --primary: #e11d48;
            --gold: #f59e0b;
            --gold-dark: #d97706;
            --text-main: #fafafa;
            --text-muted: #a1a1aa;
            --telegram: #0088cc;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        
        body {
            background-color: var(--bg-main);
            color: var(--text-main);
            font-family: 'Heebo', sans-serif;
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }

        /* Sticky Glass Header */
        .navbar {
            position: sticky;
            top: 0;
            z-index: 999;
            background: rgba(9, 9, 11, 0.88);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 11px 16px;
        }

        .nav-container {
            max-width: 1120px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
        }

        .brand-logo {
            background: linear-gradient(135deg, var(--primary), var(--gold));
            color: white;
            font-weight: 900;
            font-size: 17px;
            padding: 4px 10px;
            border-radius: 8px;
            letter-spacing: 0.5px;
            box-shadow: 0 0 15px rgba(225, 29, 72, 0.35);
        }

        .brand-sub {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
        }

        .nav-actions {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .live-badge {
            display: flex;
            align-items: center;
            gap: 6px;
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            color: #4ade80;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 700;
        }

        .pulse-dot {
            width: 7px;
            height: 7px;
            background: #22c55e;
            border-radius: 50%;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
            70% { box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
            100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }

        .menu-btn {
            background: var(--bg-elevated);
            color: var(--text-main);
            border: 1px solid var(--border-color);
            width: 36px;
            height: 36px;
            border-radius: 10px;
            font-size: 17px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.2s;
        }
        .menu-btn:hover { border-color: var(--primary); color: var(--primary); }

        /* Sidebar Drawer */
        .sidebar-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.75);
            z-index: 1000;
            backdrop-filter: blur(3px);
        }

        .sidebar {
            height: 100%;
            width: 260px;
            position: fixed;
            z-index: 1001;
            top: 0;
            right: -260px;
            background-color: var(--bg-card);
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            padding-top: 20px;
            border-left: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
        }
        .sidebar.open { right: 0; }

        .sidebar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px 15px;
            border-bottom: 1px solid var(--border-color);
        }

        .close-btn {
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 26px;
            cursor: pointer;
        }

        .sidebar a {
            padding: 14px 20px;
            text-decoration: none;
            font-size: 14px;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 500;
            border-bottom: 1px solid rgba(255,255,255,0.03);
            transition: 0.2s;
        }
        .sidebar a:hover { background: var(--bg-elevated); color: var(--gold); padding-right: 25px; }

        .sidebar-vip-box {
            margin: 20px;
            padding: 15px;
            background: linear-gradient(135deg, rgba(225, 29, 72, 0.12), rgba(245, 158, 11, 0.12));
            border: 1px solid rgba(245, 158, 11, 0.5);
            border-radius: 12px;
            text-align: center;
        }

        /* Main Container */
        .main-wrapper {
            max-width: 1120px;
            margin: 0 auto;
            padding: 15px;
        }

        /* Responsive Top Ad */
        .ad-slot {
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 6px 0 16px;
            overflow: hidden;
            border-radius: 10px;
        }

        /* Search & Categories */
        .search-container {
            position: relative;
            margin-bottom: 12px;
        }

        .search-container input {
            width: 100%;
            padding: 12px 40px 12px 15px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            background: var(--bg-card);
            color: var(--text-main);
            font-family: 'Heebo', sans-serif;
            font-size: 13.5px;
            outline: none;
            transition: 0.2s;
        }
        .search-container input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.15);
        }

        .search-icon {
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 15px;
        }

        .categories-bar {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 8px;
            margin-bottom: 14px;
            scrollbar-width: none;
        }
        .categories-bar::-webkit-scrollbar { display: none; }

        .cat-pill {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 7px 15px;
            border-radius: 20px;
            font-size: 12.5px;
            font-weight: 700;
            white-space: nowrap;
            cursor: pointer;
            transition: 0.2s;
            font-family: 'Heebo', sans-serif;
        }
        .cat-pill.active, .cat-pill:hover {
            background: var(--primary);
            color: white;
            border-color: var(--primary);
        }

        /* Section Header */
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }

        .section-title {
            font-size: 17px;
            font-weight: 900;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .section-title::before {
            content: '';
            display: inline-block;
            width: 4px;
            height: 18px;
            background: var(--primary);
            border-radius: 4px;
        }

        /* Videos Grid */
        .videos-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 18px;
        }

        @media (min-width: 680px) {
            .videos-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (min-width: 1024px) {
            .videos-grid { grid-template-columns: repeat(3, 1fr); }
        }

        /* Video Card */
        .video-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
        }
        .video-card:hover {
            border-color: #3f3f46;
        }

        .video-wrapper {
            position: relative;
            width: 100%;
            background: #050507;
            aspect-ratio: 16 / 10;
            cursor: pointer;
        }

        video {
            width: 100%;
            height: 100%;
            object-fit: contain;
            background: #050507;
            display: block;
        }

        /* طبقة القفل الشفافة للضغطة الأولى (تحافظ على ظهور اللقطة الحقيقية #t=2.0 بالكامل) */
        .smart-ad-shield {
            position: absolute;
            inset: 0;
            z-index: 4;
            cursor: pointer;
            background: transparent;
        }

        .play-overlay {
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.22);
            transition: 0.2s;
            pointer-events: none;
            z-index: 3;
        }
        .video-wrapper:hover .play-overlay {
            background: rgba(0, 0, 0, 0.08);
        }
        .play-circle {
            width: 52px;
            height: 52px;
            background: rgba(225, 29, 72, 0.92);
            border: 2px solid rgba(255, 255, 255, 0.85);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
            box-shadow: 0 0 20px rgba(225, 29, 72, 0.65);
            padding-right: 3px;
            transition: 0.2s;
        }

        .video-badges {
            position: absolute;
            top: 10px;
            right: 10px;
            left: 10px;
            display: flex;
            justify-content: space-between;
            pointer-events: none;
            z-index: 5;
        }

        .badge-tag {
            background: rgba(9, 9, 11, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #fff;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            backdrop-filter: blur(4px);
        }

        .badge-hd {
            background: rgba(225, 29, 72, 0.92);
            color: #fff;
            font-size: 10px;
            font-weight: 900;
            padding: 3px 7px;
            border-radius: 6px;
        }

        .card-body {
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .archive-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 13px;
            font-weight: 700;
            color: var(--text-main);
        }

        .real-views {
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 500;
        }

        .tags-row {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }

        .smart-tag {
            font-size: 11px;
            color: #38bdf8;
            background: rgba(56, 189, 248, 0.08);
            padding: 2px 8px;
            border-radius: 6px;
            cursor: pointer;
            transition: 0.2s;
        }
        .smart-tag:hover {
            background: rgba(56, 189, 248, 0.2);
        }

        .card-actions {
            display: grid;
            grid-template-columns: 0.9fr 0.9fr 1.4fr;
            gap: 8px;
            margin-top: 2px;
        }

        .action-btn {
            background: var(--bg-elevated);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 8px 6px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
            text-decoration: none;
            font-family: 'Heebo', sans-serif;
            transition: 0.2s;
        }
        .action-btn:hover { background: #27272a; }
        .action-btn.liked { border-color: var(--primary); color: var(--primary); background: rgba(225, 29, 72, 0.12); }
        
        .btn-tg-full {
            background: linear-gradient(90deg, #0088cc, #0284c7);
            border: none;
            color: white;
        }
        .btn-tg-full:hover { opacity: 0.92; }

        /* شريط VIP المختصر والأنيق بعد كل 3 فيديوهات */
        .compact-vip-strip {
            grid-column: 1 / -1;
            background: linear-gradient(90deg, #16161a 0%, #241220 50%, #16161a 100%);
            border: 1px solid rgba(245, 158, 11, 0.45);
            border-radius: 12px;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        }

        .strip-info {
            display: flex;
            align-items: center;
            gap: 10px;
            text-align: right;
        }

        .strip-icon {
            width: 36px;
            height: 36px;
            min-width: 36px;
            background: rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.4);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }

        .strip-text h4 {
            margin: 0;
            font-size: 13.5px;
            font-weight: 900;
            color: var(--gold);
            line-height: 1.3;
        }

        .strip-text span {
            font-size: 11.5px;
            color: var(--text-muted);
            display: block;
        }

        .sleek-vip-btn {
            background: linear-gradient(135deg, var(--gold), var(--gold-dark));
            color: #09090b;
            text-decoration: none;
            padding: 8px 16px;
            border-radius: 50px;
            font-size: 12px;
            font-weight: 900;
            white-space: nowrap;
            box-shadow: 0 3px 12px rgba(245, 158, 11, 0.35);
            transition: transform 0.2s, box-shadow 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        .sleek-vip-btn:hover {
            transform: translateY(-1px) scale(1.03);
            box-shadow: 0 5px 16px rgba(245, 158, 11, 0.5);
        }

        /* Load More Button */
        .load-more-wrap {
            text-align: center;
            margin: 28px 0 15px;
        }

        .load-more-btn {
            background: var(--bg-elevated);
            border: 1px solid var(--primary);
            color: var(--text-main);
            padding: 12px 30px;
            border-radius: 12px;
            font-size: 13.5px;
            font-weight: 700;
            cursor: pointer;
            font-family: 'Heebo', sans-serif;
            transition: 0.2s;
        }
        .load-more-btn:hover {
            background: var(--primary);
            color: white;
        }

        /* Native & Banner Ads Box */
        .ads-section {
            margin: 22px 0;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 14px;
            text-align: center;
        }
        .ad-label {
            font-size: 10px;
            color: #52525b;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: block;
        }

        /* Footer */
        footer {
            background: var(--bg-card);
            border-top: 1px solid var(--border-color);
            padding: 28px 15px;
            text-align: center;
            margin-top: 35px;
        }

        .footer-links {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 16px;
        }

        .footer-btn {
            background: var(--bg-elevated);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 8px 15px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 12px;
            font-weight: 700;
            transition: 0.2s;
        }
        .footer-btn:hover { border-color: var(--telegram); color: #38bdf8; }

        .copyright {
            font-size: 11.5px;
            color: var(--text-muted);
        }

        .hidden-item { display: none !important; }
    </style>

    <!-- Adsterra SocialBar Script -->
    <script data-cfasync="false" src="https://dcengg.org/14/1ce2d02f4292f494d9ca01ceb7d675fc"></script>
</head>
<body>

    <!-- Sticky Header -->
    <header class="navbar">
        <div class="nav-container">
            <a href="/" class="brand">
                <span class="brand-logo">ISRAFLIX</span>
                <span class="brand-sub">VIP 🇮🇱</span>
            </a>

            <div class="nav-actions">
                <div class="live-badge" title="מבקרים פעילים באתר כעת">
                    <span class="pulse-dot"></span>
                    <span id="onlineCount">1</span> מחוברים
                </div>
                <button class="menu-btn" onclick="toggleSidebar()" aria-label="תפריט">☰</button>
            </div>
        </div>
    </header>

    <!-- Sidebar Drawer -->
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>
    <aside class="sidebar" id="mySidebar">
        <div class="sidebar-header">
            <span style="font-weight: 900; color: var(--gold);">ניווט מהיר</span>
            <button class="close-btn" onclick="toggleSidebar()">&times;</button>
        </div>
        <a href="{{ telegram_link }}" target="_blank">🏠 דף הבית</a>
        <a href="{{ telegram_link }}" target="_blank">🔥 הכי חם השבוע</a>
        <a href="{{ telegram_link }}" target="_blank">💎 ערוץ VIP סגור</a>
        <a href="{{ telegram_link }}" target="_blank">📹 ארכיון הדלפות</a>
        <a href="{{ telegram_link }}" target="_blank">📲 קבוצת הטלגרם הרשמית</a>

        <div class="sidebar-vip-box">
            <div style="font-weight: 900; color: var(--gold); margin-bottom: 5px; font-size: 14px;">גישה מלאה בחינם!</div>
            <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 12px;">כל הסרטונים המלאים מחכים לך בערוץ הטלגרם</div>
            <a href="{{ telegram_link }}" target="_blank" style="justify-content: center; background: var(--gold); color: #000; border-radius: 50px; padding: 9px; font-weight: 900; font-size: 12.5px;">הצטרף עכשיו ✈️</a>
        </div>
    </aside>

    <main class="main-wrapper">
        <!-- Top Banner Ad -->
        <div class="ad-slot">
            <script>
              atOptions = {
                 'key' : '8a898fb2ff79e4f617a887a1fc16c862',
                 'format' : 'iframe',
                 'height' : 90,
                 'width' : 728,
                 'params' : {}
              };
            </script>
            <script src="https://dcengg.org/22/8a898fb2ff79e4f617a887a1fc16c862"></script>
        </div>

        <!-- Search Bar -->
        <div class="search-container">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" onkeyup="filterContent()" placeholder="חפש לפי מספר ארכיון (#140) או תגית (#VIP)...">
        </div>

        <!-- Categories & Real Sorting Pills -->
        <div class="categories-bar">
            <button class="cat-pill active" onclick="setFilter('all', this)">הכל ({{ videos|length }})</button>
            <button class="cat-pill" onclick="sortByMostViewed(this)">👁️ הכי נצפים (אמיתי)</button>
            <button class="cat-pill" onclick="setFilter('vip', this)">💎 בלעדי VIP</button>
            <button class="cat-pill" onclick="setFilter('hot', this)">🔥 הכי חם</button>
            <button class="cat-pill" onclick="setFilter('cam', this)">📹 תיעוד פרטי</button>
        </div>

        <!-- Section Header -->
        <div class="section-header">
            <h1 class="section-title">עדכונים אחרונים בארכיון 18+</h1>
            <span style="font-size: 11.5px; color: var(--text-muted);">{{ videos|length }} סרטונים זמינים</span>
        </div>

        <!-- Videos Grid -->
        <div class="videos-grid" id="videosGrid">
            {% for video in videos %}
            <article class="video-card video-item {% if loop.index > 6 %}initial-hidden hidden-item{% endif %}" 
                     id="card-{{ video.id }}"
                     data-vid-id="{{ video.id }}"
                     data-search="{{ video.archive_title }} {{ video.tags|join(' ') }}" 
                     data-category="{{ video.category }}"
                     data-views="{{ video.views }}"
                     data-order="{{ loop.index }}">
                
                <div class="video-wrapper" onclick="playVideoFromWrapper(this)">
                    <video preload="metadata" controls playsinline controlsList="nodownload" onplay="handleVideoPlay(this, '{{ video.id }}')">
                        <source src="{{ video.url }}#t=2.0" type="video/mp4">
                    </video>
                    
                    <!-- طبقة شفافة تلتقط الضغطة الأولى لفتح الرابط المباشر ثم تختفي -->
                    <div class="smart-ad-shield" id="shield-{{ video.id }}" onclick="unlockVideoWithDirectAd(event, this, '{{ video.id }}', '{{ video.direct_ad }}')"></div>

                    <div class="play-overlay" id="overlay-{{ video.id }}">
                        <div class="play-circle" id="circle-{{ video.id }}">▶</div>
                    </div>
                    <div class="video-badges">
                        <span class="badge-tag">{{ video.badge }}</span>
                        <span class="badge-hd">HD</span>
                    </div>
                </div>

                <div class="card-body">
                    <div class="archive-row">
                        <span>{{ video.archive_title }}</span>
                        <span class="real-views">👁️ <span id="views-{{ video.id }}">{{ video.views }}</span> צפיות</span>
                    </div>

                    <div class="tags-row">
                        {% for tag in video.tags %}
                        <span class="smart-tag" onclick="searchByTag('{{ tag }}')">{{ tag }}</span>
                        {% endfor %}
                    </div>

                    <div class="card-actions">
                        <button class="action-btn like-btn" id="like-btn-{{ video.id }}" onclick="toggleLike('{{ video.id }}')">
                            ❤️ <span id="like-count-{{ video.id }}">{{ video.likes }}</span>
                        </button>
                        <button class="action-btn" onclick="shareVideo('{{ video.archive_title }}')">
                            🔗 שתף
                        </button>
                        <a href="{{ telegram_link }}" target="_blank" class="action-btn btn-tg-full">
                            📲 המלא בטלגרם
                        </a>
                    </div>
                </div>
            </article>

            <!-- شريط إعلان تيليجرام مختصر وأنيق بعد كل 3 فيديوهات -->
            {% if loop.index % 3 == 0 %}
            <div class="compact-vip-strip promo-item {% if loop.index > 6 %}initial-hidden hidden-item{% endif %}">
                <div class="strip-info">
                    <div class="strip-icon">🔥</div>
                    <div class="strip-text">
                        <h4>הסרטונים המלאים מחכים לך ב-VIP 🔞</h4>
                        <span>גישה חופשית לערוץ הסגור בטלגרם</span>
                    </div>
                </div>
                <a href="{{ telegram_link }}" target="_blank" class="sleek-vip-btn">
                    הצטרף עכשיו ✈️
                </a>
            </div>
            {% endif %}
            {% endfor %}
        </div>

        <!-- Load More Button -->
        <div class="load-more-wrap" id="loadMoreWrap">
            <button class="load-more-btn" onclick="loadMoreVideos()">טען עוד סרטונים מהארכיון ⬇️ ({{ videos|length - 6 }} נוספים)</button>
        </div>

        <!-- Native Banner Ad -->
        <div class="ads-section">
            <span class="ad-label">תוכן ממומן</span>
            <script async="async" data-cfasync="false" src="https://dcengg.org/21/c09daea963d6cca1b172e88ddfa0ee51"></script>
            <div id="container-c09daea963d6cca1b172e88ddfa0ee51"></div>
        </div>

        <!-- 300x250 Banner Ad -->
        <div class="ads-section">
            <span class="ad-label">מומלץ עבורך</span>
            <script>
              atOptions = {
                 'key' : 'acb79a2efda8a0e4fae251b979f31414',
                 'format' : 'iframe',
                 'height' : 250,
                 'width' : 300,
                 'params' : {}
              };
            </script>
            <script src="https://dcengg.org/22/acb79a2efda8a0e4fae251b979f31414"></script>
        </div>
    </main>

    <footer>
        <div class="footer-links">
            <a href="{{ telegram_link }}" target="_blank" class="footer-btn">ערוץ ראשי 📱</a>
            <a href="{{ telegram_link }}" target="_blank" class="footer-btn">קבוצת VIP ⭐</a>
            <a href="{{ telegram_link }}" target="_blank" class="footer-btn">הדלפות חדשות 🔥</a>
            <a href="{{ telegram_link }}" target="_blank" class="footer-btn">יצירת קשר 🇮🇱</a>
        </div>
        <div class="copyright">
            כל הזכויות שמורות © 2026 ISRAFLIX VIP | האתר מיועד לגילאי 18+ בלבד.
        </div>
    </footer>

    <script>
        let currentCategory = 'all';
        let allLoaded = false;
        const viewedInSession = new Set();

        let sessionId = sessionStorage.getItem('visitor_sid');
        if (!sessionId) {
            sessionId = 'sid_' + Math.random().toString(36).substring(2, 15) + Date.now();
            sessionStorage.setItem('visitor_sid', sessionId);
        }

        function sendHeartbeat() {
            fetch('/api/heartbeat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sid: sessionId })
            })
            .then(res => res.json())
            .then(data => {
                if (data.online) {
                    document.getElementById('onlineCount').textContent = data.online.toLocaleString();
                }
            })
            .catch(() => {});
        }

        function toggleSidebar() {
            const sidebar = document.getElementById("mySidebar");
            const overlay = document.getElementById("sidebarOverlay");
            sidebar.classList.toggle("open");
            overlay.style.display = sidebar.classList.contains("open") ? "block" : "none";
        }

        // الضغطة الأولى على الفيديو: فتح الرابط المباشر + فك القفل عن الفيديو للضغطة الثانية
        function unlockVideoWithDirectAd(event, shieldEl, vidId, adUrl) {
            event.stopPropagation();
            
            // فتح الرابط المباشر في نافذة جديدة
            window.open(adUrl, '_blank', 'noopener,noreferrer');
            
            // إزالة طبقة القفل عن هذا الفيديو ليتمكن الزائر من تشغيله في الضغطة الثانية
            shieldEl.remove();
            
            // تغيير لون زر التشغيل للأخضر للإشارة إلى أن الفيديو جاهز للتشغيل الآن
            const circle = document.getElementById('circle-' + vidId);
            if (circle) {
                circle.style.background = 'rgba(34, 197, 94, 0.92)';
                circle.style.boxShadow = '0 0 20px rgba(34, 197, 94, 0.7)';
            }
        }

        function playVideoFromWrapper(wrapper) {
            const video = wrapper.querySelector('video');
            if (video && video.paused) {
                video.play().catch(() => {});
            }
        }

        function handleVideoPlay(videoEl, vidId) {
            const overlay = document.getElementById('overlay-' + vidId);
            if (overlay) overlay.style.display = 'none';

            document.querySelectorAll('video').forEach(v => {
                if (v !== videoEl) v.pause();
            });

            if (!viewedInSession.has(vidId)) {
                viewedInSession.add(vidId);
                fetch('/api/view/' + vidId, { method: 'POST' })
                    .then(res => res.json())
                    .then(data => {
                        if (data.views !== undefined) {
                            document.getElementById('views-' + vidId).textContent = data.views;
                            const card = document.getElementById('card-' + vidId);
                            if (card) card.setAttribute('data-views', data.views);
                        }
                    })
                    .catch(() => {});
            }
        }

        function setFilter(cat, btnElement) {
            currentCategory = cat;
            document.querySelectorAll('.cat-pill').forEach(btn => btn.classList.remove('active'));
            btnElement.classList.add('active');
            
            if (!allLoaded) loadMoreVideos();
            restoreDefaultOrder();
            filterContent();
        }

        function sortByMostViewed(btnElement) {
            document.querySelectorAll('.cat-pill').forEach(btn => btn.classList.remove('active'));
            btnElement.classList.add('active');
            currentCategory = 'all';

            if (!allLoaded) loadMoreVideos();

            const grid = document.getElementById('videosGrid');
            const cards = Array.from(document.querySelectorAll('.video-item'));
            
            document.querySelectorAll('.promo-item').forEach(p => p.classList.add('hidden-item'));

            cards.sort((a, b) => {
                const viewsA = parseInt(a.getAttribute('data-views') || '0');
                const viewsB = parseInt(b.getAttribute('data-views') || '0');
                return viewsB - viewsA;
            });

            cards.forEach(card => {
                card.classList.remove('hidden-item');
                grid.appendChild(card);
            });
        }

        function restoreDefaultOrder() {
            const grid = document.getElementById('videosGrid');
            const cards = Array.from(document.querySelectorAll('.video-item'));
            cards.sort((a, b) => parseInt(a.getAttribute('data-order')) - parseInt(b.getAttribute('data-order')));
            cards.forEach(card => grid.appendChild(card));
        }

        function searchByTag(tag) {
            const input = document.getElementById('searchInput');
            input.value = tag;
            if (!allLoaded) loadMoreVideos();
            filterContent();
            window.scrollTo({ top: 120, behavior: 'smooth' });
        }

        function filterContent() {
            const query = document.getElementById('searchInput').value.toLowerCase().trim();
            const items = document.querySelectorAll('.video-item');
            const promos = document.querySelectorAll('.promo-item');

            items.forEach(card => {
                const searchData = card.getAttribute('data-search').toLowerCase();
                const cat = card.getAttribute('data-category');
                const matchesSearch = searchData.includes(query);
                const matchesCat = (currentCategory === 'all' || cat === currentCategory);

                if (matchesSearch && matchesCat) {
                    card.classList.remove('hidden-item');
                } else {
                    card.classList.add('hidden-item');
                }
            });

            promos.forEach(promo => {
                if (query.length > 0 || currentCategory !== 'all') {
                    promo.classList.add('hidden-item');
                } else if (allLoaded) {
                    promo.classList.remove('hidden-item');
                }
            });
        }

        function loadMoreVideos() {
            document.querySelectorAll('.initial-hidden').forEach(el => {
                el.classList.remove('hidden-item');
            });
            const wrap = document.getElementById('loadMoreWrap');
            if (wrap) wrap.style.display = 'none';
            allLoaded = true;
        }

        function toggleLike(vidId) {
            const btn = document.getElementById('like-btn-' + vidId);
            const countSpan = document.getElementById('like-count-' + vidId);
            const storageKey = 'liked_' + vidId;
            const isLiked = localStorage.getItem(storageKey) === 'true';
            const action = isLiked ? 'unlike' : 'like';

            if (isLiked) {
                localStorage.setItem(storageKey, 'false');
                btn.classList.remove('liked');
            } else {
                localStorage.setItem(storageKey, 'true');
                btn.classList.add('liked');
            }

            fetch('/api/like/' + vidId, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: action })
            })
            .then(res => res.json())
            .then(data => {
                if (data.likes !== undefined) {
                    countSpan.textContent = data.likes;
                }
            })
            .catch(() => {});
        }

        window.addEventListener('DOMContentLoaded', () => {
            sendHeartbeat();
            setInterval(sendHeartbeat, 15000);

            document.querySelectorAll('.like-btn').forEach(btn => {
                const vidId = btn.id.replace('like-btn-', '');
                if (localStorage.getItem('liked_' + vidId) === 'true') {
                    btn.classList.add('liked');
                }
            });
        });

        function shareVideo(title) {
            if (navigator.share) {
                navigator.share({
                    title: title,
                    text: 'צפה בתיעוד הבלעדי הזה ב-ISRAFLIX VIP: ',
                    url: window.location.href
                }).catch(() => {});
            } else {
                navigator.clipboard.writeText(window.location.href);
                alert('הקישור הועתק! שתף עם חברים 🔗');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    videos = get_videos_list()
    response = make_response(render_template_string(
        HTML_TEMPLATE, 
        videos=videos, 
        telegram_link=TELEGRAM_LINK
    ))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
