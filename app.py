from flask import Flask

app = Flask(__name__)

HTML_PAGE = """
<html>
    <head>
        <title>Mind Master | منصة البث الأسطورية</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; }
            body { background-color: #0e1626; color: #f8fafc; font-family: Tahoma, sans-serif; margin: 0; padding: 0; }
            
            .announcement-bar { background: linear-gradient(90deg, #7c3aed, #2563eb); color: white; font-size: 11px; padding: 6px; text-align: center; font-weight: bold; }
            .mobile-header { display: flex; align-items: center; justify-content: space-between; background: #1e1f22; padding: 10px 15px; border-bottom: 1px solid #2b2d31; }
            .menu-btn { background: #5865f2; color: white; border: none; padding: 6px 10px; border-radius: 6px; font-size: 16px; cursor: pointer; }
            .logo-title { color: #5865f2; font-size: 15px; font-weight: bold; margin: 0; }

            .sidebar { 
                height: 100%; width: 0; position: fixed; z-index: 1000; top: 0; right: 0; 
                background-color: #1e1f22; overflow-x: hidden; transition: 0.3s; padding-top: 50px; 
                border-left: 1px solid #2b2d31; box-shadow: -5px 0 15px rgba(0,0,0,0.5);
            }
            .sidebar a { padding: 10px 20px; text-decoration: none; font-size: 13px; color: #b5bac1; display: block; transition: 0.2s; font-weight: bold; text-align: right; }
            .sidebar a:hover { background: #5865f2; color: white; }
            .sidebar .close-btn { position: absolute; top: 10px; left: 15px; font-size: 20px; color: white; cursor: pointer; }

            .server-status { margin: 20px; background: #2b2d31; padding: 10px; border-radius: 6px; font-size: 11px; text-align: center; color: #b5bac1; }
            .online-dot { height: 7px; width: 7px; background-color: #23a55a; border-radius: 50%; display: inline-block; margin-left: 5px; }

            .content { padding: 15px; max-width: 1200px; margin: auto; }
            .search-box { margin-bottom: 20px; text-align: center; }
            .search-box input { width: 100%; max-width: 500px; padding: 10px 15px; border-radius: 8px; border: 1px solid #2b2d31; background: #1e1f22; color: white; font-size: 12px; outline: none; }

            h2.section-title { font-size: 15px; color: #e2e8f0; margin-bottom: 15px; border-right: 4px solid #5865f2; padding-right: 8px; text-align: right; }

            /* شبكة عرض الفيديوهات: فيديوهين (2) في كل صف */
            .videos-grid { 
                display: grid; 
                grid-template-columns: repeat(2, 1fr); 
                gap: 12px; 
            }
            
            .video-card { 
                background: #1e1f22; 
                border: 1px solid #2b2d31; 
                padding: 8px; 
                border-radius: 8px; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.3); 
                text-align: right;
            }
            .video-card h3 { font-size: 11px; color: #f1f5f9; margin: 0 0 4px 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
            .video-views { font-size: 10px; color: #94a3b8; margin-bottom: 6px; }
            
            /* أبعاد الفيديو لتناسب عرض فيديوهين في الصف بحجم أكبر وأوضح */
            video { width: 100%; height: 160px; border-radius: 6px; background: black; object-fit: cover; }

            footer { background: #1e1f22; padding: 20px; text-align: center; border-top: 1px solid #2b2d31; margin-top: 40px; }
            .footer-title { font-size: 13px; color: #b5bac1; margin-bottom: 12px; font-weight: bold; }
            .social-buttons { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
            .btn { padding: 7px 14px; text-decoration: none; border-radius: 6px; font-size: 11px; font-weight: bold; color: white; }
            .whatsapp { background: #248046; }
            .telegram { background: #0088cc; }
            .facebook { background: #1877f2; }
            .copyright { margin-top: 15px; font-size: 10px; color: #6b7280; }
        </style>
    </head>
    <body>
        
        <div class="announcement-bar" id="top-banner">
            🔥 أهلاً بك في منصة البث الأسطورية | تواصل معنا عبر أزرار الدعم في الأسفل
        </div>

        <div class="mobile-header">
            <h1 class="logo-title">⚡ Mind Master</h1>
            <button class="menu-btn" onclick="openNav()">☰</button>
        </div>

        <div id="mySidebar" class="sidebar">
            <a href="javascript:void(0)" class="close-btn" onclick="closeNav()">&times;</a>
            <a href="#" id="nav-home">🏠 الرئيسية</a>
            <a href="#" id="nav-trending">🔥 الرائجة</a>
            <a href="#" id="nav-categories">🎮 الأقسام والألعاب</a>
            <a href="#" id="nav-fav">❤️ المفضلة</a>
            
            <div class="server-status">
                <span id="status-text">حالة البث:</span> <span class="online-dot"></span> <span id="status-online">متصل</span>
            </div>
        </div>

        <div class="content">
            <div class="search-box">
                <input type="text" id="search-input" placeholder="ابحث عن فيديو أو محتوى...">
            </div>

            <h2 class="section-title" id="section-heading">أحدث المقاطع المضافة</h2>
            
            <div class="videos-grid">
                <script>
                    const videosList = [
                        "wio4kl.mp4", "vo29gf.mp4", "qseq0i.mp4", "762n5t.mp4", "6qs6t8.mp4", "xtrtpd.mp4", 
                        "xovx5v.mp4", "gca6vk.mp4", "sjj6dd.mp4", "vzginq.mp4", "lwbdy1.mp4", "o36fln.mp4", 
                        "rv9c5v.mp4", "lkqw9a.mp4", "y9teda.mp4", "ly7k1z.mp4", "15e5t5.mp4", "dtklvc.mp4", 
                        "k79dhg.mp4", "uk5hrq.mp4", "nvfstt.mp4", "9nps91.mp4"
                    ];
                    const viewsList = ["1.4K", "850", "3.2K", "620", "2.1K", "940", "4.5K", "1.1K", "780", "2.9K", "1.8K", "3.6K", "530", "1.2K", "2.4K", "890", "1.7K", "3.1K", "920", "4.0K", "1.3K", "2.7K"];

                    for(let i = 0; i < videosList.length; i++) {
                        let vName = videosList[i];
                        let vViews = viewsList[i];
                        document.write(`
                            <div class="video-card">
                                <h3 dir="ltr">${vName}</h3>
                                <div class="video-views">👁️ ${vViews}</div>
                                <video preload="metadata" controls controlsList="nodownload" src="https://files.catbox.moe/${vName}#t=0.1"></video>
                            </div>
                        `);
                    }
                </script>
            </div>
        </div>

        <footer>
            <div class="footer-title" id="footer-text">شارك المنصة وتواصل مع المطور مباشرة</div>
            <div class="social-buttons">
                <a href="https://wa.me/" class="btn whatsapp" id="btn-wa">واتساب</a>
                <a href="https://t.me/" class="btn telegram" id="btn-tg">تيليجرام</a>
                <a href="https://facebook.com" class="btn facebook" id="btn-fb">فيسبوك</a>
            </div>
            <div class="copyright" id="copyright-text">
                جميع الحقوق محفوظة © 2026 | تم التصميم والتطوير بفخر عبر الهاتف
            </div>
        </footer>

        <script>
            function openNav() { document.getElementById("mySidebar").style.width = "220px"; }
            function closeNav() { document.getElementById("mySidebar").style.width = "0"; }

            // تحديد اللغة تلقائياً (عربي، إنجليزي، عبري)
            const userLang = navigator.language || navigator.userLanguage;
            if (userLang.startsWith('he')) {
                document.documentElement.setAttribute('dir', 'rtl');
                document.getElementById('top-banner').innerText = "🔥 בآبا الحضور إلى منصة البث الأسطورية | التواصل معنا في الأسفل";
                document.getElementById('nav-home').innerText = "🏠 الرئيسية (בית)";
                document.getElementById('nav-trending').innerText = "🔥 الرائجة (פופולרי)";
                document.getElementById('nav-categories').innerText = "🎮 الأقسام والألعاب";
                document.getElementById('nav-fav').innerText = "❤️ المفضلة";
                document.getElementById('status-text').innerText = "حالة البث:";
                document.getElementById('status-online').innerText = "متصل (מחובר)";
                document.getElementById('search-input').placeholder = "חפש סרטון أو תוכן...";
                document.getElementById('section-heading').innerText = "أحدث المقاطع المضافة";
                document.getElementById('footer-text').innerText = "شارك المنصة وتواصل مع المطور";
                document.getElementById('btn-wa').innerText = "واتساب";
                document.getElementById('btn-tg').innerText = "تيليجرام";
                document.getElementById('btn-fb').innerText = "فيسبوك";
                document.getElementById('copyright-text').innerText = "جميع الحقوق محفوظة © 2026";
            } else if (userLang.startsWith('en')) {
                document.documentElement.setAttribute('dir', 'ltr');
                document.getElementById('top-banner').innerText = "🔥 Welcome to the Epic Streaming Platform | Contact us below";
                document.getElementById('nav-home').innerText = "🏠 Home";
                document.getElementById('nav-trending').innerText = "🔥 Trending";
                document.getElementById('nav-categories').innerText = "🎮 Categories & Games";
                document.getElementById('nav-fav').innerText>document.getElementById('nav-fav').innerText = "❤️ Favorites";
                document.getElementById('status-text').innerText = "Status:";
                document.getElementById('status-online').innerText = "Online";
                document.getElementById('search-input').placeholder = "Search for a video or content...";
                document.getElementById('section-heading').innerText = "Latest Added Clips";
                document.getElementById('footer-text').innerText = "Share the platform & connect with the developer";
                document.getElementById('btn-wa').innerText = "WhatsApp";
                document.getElementById('btn-tg').innerText = "Telegram";
                document.getElementById('btn-fb').innerText = "Facebook";
                document.getElementById('copyright-text').innerText = "All rights reserved © 2026 | Developed on Mobile";
            }
        </script>
    </body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
