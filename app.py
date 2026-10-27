from flask import Flask

app = Flask(__name__)

HTML_PAGE = """
<html dir="rtl" lang="he">
    <head>
        <title>סרטונים חמים בישראל</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Adsterra Popunder Script -->
        <script data-cfasync="false" src="https://4xfreedom.com/1/10753c745a27f2bf8e0d5b0bbc0697d9"></script>
        
        <style>
            * { box-sizing: border-box; }
            body { background-color: #0e1626; color: #f8fafc; font-family: Tahoma, sans-serif; margin: 0; padding: 0; }
            
            .announcement-bar { background: linear-gradient(90deg, #7c3aed, #2563eb); color: white; font-size: 12px; padding: 8px; text-align: center; font-weight: bold; }
            .mobile-header { display: flex; align-items: center; justify-content: space-between; background: #1e1f22; padding: 10px 15px; border-bottom: 1px solid #2b2d31; }
            .menu-btn { background: #5865f2; color: white; border: none; padding: 6px 10px; border-radius: 6px; font-size: 16px; cursor: pointer; }
            .logo-container { display: flex; align-items: center; gap: 8px; }
            .logo-emoji { font-size: 18px; }
            .logo-title { color: #f59e0b; font-size: 15px; font-weight: bold; margin: 0; }

            .sidebar { 
                height: 100%; width: 0; position: fixed; z-index: 1000; top: 0; right: 0; 
                background-color: #1e1f22; overflow-x: hidden; transition: 0.3s; padding-top: 50px; 
                border-left: 1px solid #2b2d31; box-shadow: -5px 0 15px rgba(0,0,0,0.5);
            }
            .sidebar a { padding: 10px 20px; text-decoration: none; font-size: 13px; color: #b5bac1; display: block; transition: 0.2s; font-weight: bold; text-align: right; }
            .sidebar a:hover { background: #5865f2; color: white; }
            .sidebar .close-btn { position: absolute; top: 10px; left: 15px; font-size: 20px; color: white; cursor: pointer; }

            .server-status { margin: 20px; background: #2b2d31; padding: 10px; border-radius: 6px; font-size: 11px; text-align: center; color: #b5bac1; }
            .online-dot { height: 7px; width: 7px; background-color: #23a55a; border-radius: 50%; display: inline-block; margin-right: 5px; }

            .content { padding: 15px; max-width: 1200px; margin: auto; }
            .search-box { margin-bottom: 20px; text-align: center; }
            .search-box input { width: 100%; max-width: 500px; padding: 10px 15px; border-radius: 8px; border: 1px solid #2b2d31; background: #1e1f22; color: white; font-size: 12px; outline: none; text-align: right; }

            .top-ad-banner { text-align: center; margin: 15px 0; overflow: hidden; }

            h2.section-title { font-size: 15px; color: #e2e8f0; margin-bottom: 15px; border-right: 4px solid #f59e0b; padding-right: 8px; text-align: right; }

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
            .video-card h3 { font-size: 11px; color: #f1f5f9; margin: 0 0 4px 0; overflow: hidden; text-overflow: ellipsis; }
            .video-views { font-size: 10px; color: #94a3b8; margin-bottom: 6px; }
            
            video { width: 100%; height: 160px; border-radius: 6px; background: black; object-fit: cover; }
            
            .smart-btn { display: block; width: 100%; margin-top: 8px; background: linear-gradient(90deg, #f59e0b, #d97706); color: white; text-align: center; padding: 6px; border-radius: 5px; font-size: 11px; font-weight: bold; text-decoration: none; }
            .smart-btn:hover { opacity: 0.9; }

            .mid-ads-container { margin: 25px 0; text-align: center; background: #1e1f22; padding: 15px; border-radius: 8px; border: 1px solid #2b2d31; }

            footer { background: #1e1f22; padding: 20px; text-align: center; border-top: 1px solid #2b2d31; margin-top: 40px; }
            .footer-title { font-size: 13px; color: #b5bac1; margin-bottom: 12px; font-weight: bold; }
            .social-buttons { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
            .btn { padding: 7px 14px; text-decoration: none; border-radius: 6px; font-size: 11px; font-weight: bold; color: white; }
            .whatsapp { background: #248046; }
            .telegram { background: #0088cc; }
            .facebook { background: #1877f2; }
            .smart-link-btn { background: #7c3aed; }
            .copyright { margin-top: 15px; font-size: 10px; color: #6b7280; }
        </style>
        
        <!-- Adsterra SocialBar Script -->
        <script data-cfasync="false" src="https://dcengg.org/14/1ce2d02f4292f494d9ca01ceb7d675fc"></script>
    </head>
    <body>
        
        <div class="announcement-bar">
            🔥 בברוכים הבאים לפלטפורמת הוידאו הלוהטת בישראל 🔥
        </div>

        <div class="mobile-header">
            <div class="logo-container">
                <span class="logo-emoji">🔥🇮🇱</span>
                <h1 class="logo-title">סרטונים חמים בישראל</h1>
            </div>
            <button class="menu-btn" onclick="openNav()">☰</button>
        </div>

        <div id="mySidebar" class="sidebar">
            <a href="javascript:void(0)" class="close-btn" onclick="closeNav()">&times;</a>
            <a href="https://demper.org/4/cd97dd66aac08206ff8fcb6dc85e8b08" target="_blank">🏠 בית</a>
            <a href="https://demper.org/4/cd97dd66aac08206ff8fcb6dc85e8b08" target="_blank">🔥 פופולרי</a>
            <a href="https://demper.org/4/cd97dd66aac08206ff8fcb6dc85e8b08" target="_blank">🎮 קטגוריות VIP</a>
            <a href="https://demper.org/4/cd97dd66aac08206ff8fcb6dc85e8b08" target="_blank">❤️ מועדפים</a>
            
            <div class="server-status">
                <span>סטטוס שידור:</span> <span class="online-dot"></span> <span>מחובר</span>
            </div>
        </div>

        <div class="content">
            <!-- بنر إعلاني علوي 728x90 -->
            <div class="top-ad-banner">
                <script>
                  atOptions = {
                     key  :  '8a898fb2ff79e4f617a887a1fc16c862',
                     format  :  'iframe',
                     height  : 90,
                     width  : 728,
                     params  : {}
                  };
                </script>
                <script src="https://dcengg.org/22/8a898fb2ff79e4f617a887a1fc16c862"></script>
            </div>

            <div class="search-box">
                <input type="text" placeholder="חפש סרטון או תוכן...">
            </div>

            <h2 class="section-title">🔥 סרטונים חמים חדשים</h2>
            
            <div class="videos-grid">
                <script>
                    const videosList = [
                        "wio4kl.mp4", "vo29gf.mp4", "qseq0i.mp4", "762n5t.mp4", "6qs6t8.mp4", "xtrtpd.mp4", 
                        "xovx5v.mp4", "gca6vk.mp4", "sjj6dd.mp4", "vzginq.mp4", "lwbdy1.mp4", "o36fln.mp4", 
                        "rv9c5v.mp4", "lkqw9a.mp4", "y9teda.mp4", "ly7k1z.mp4", "15e5t5.mp4", "dtklvc.mp4", 
                        "k79dhg.mp4", "uk5hrq.mp4", "nvfstt.mp4", "9nps91.mp4"
                    ];
                    
                    const titlesList = [
                        "🔥 סרטון בלעדי חם מאוד - תל אביב VIP",
                        "💖 לוהט במיוחד - בלעדי HD",
                        "🔥 סודי ביותר - קטעים אסורים",
                        "⚡ בלעדי באתר - ללא צנזורה 18+",
                        "💎 חושני ומרגש - קטעים מיוחדים",
                        "🔥 מיוחד למבוגרים - קסם המזרח התיכון",
                        "💋 חדש וחם - יצירת מופת חזותית",
                        "🔥 אקסקלוסיבי - שידור חי לוהט",
                        "🌟 בלעדי ברשת - הרפתקאות לילה",
                        "🔥 שערורייה - סרטונים אסורים",
                        "💖 אهבה אסורה - סודות אפלים",
                        "🔥 טירוף חושים - פיצוץ חושים אמיתי",
                        "⚡ פצצת שsi - קטעים יוצאי דופן",
                        "🔥 סרטון מטורף - הנאה ללא גבולות",
                        "💎 VIP בלעדי - תוכן למבוגרים בלבד",
                        "🔥 חם מהתנור - בלעדי לחלוטין",
                        "💋 מגע של קסם - מפגשים לוהטים",
                        "🔥 סודות אפלים - ריגושים אבсолюטיי",
                        "🌟 אקסטרים - אתגרים לוהטים",
                        "🔥 שיא החום - שיא המתח והריגוש",
                        "💖 מומלץ ביותר - המבוקש ביותר",
                        "🔥 בלעדי לחברי האתר - לילה מיוחד"
                    ];

                    const viewsList = ["1.4K", "850", "3.2K", "620", "2.1K", "940", "4.5K", "1.1K", "780", "2.9K", "1.8K", "3.6K", "530", "1.2K", "2.4K", "890", "1.7K", "3.1K", "920", "4.0K", "1.3K", "2.7K"];

                    for(let i = 0; i < videosList.length; i++) {
                        let vName = videosList[i];
                        let vTitle = titlesList[i];
                        let vViews = viewsList[i];
                        document.write(`
                            <div class="video-card">
                                <h3>${vTitle}</h3>
                                <div class="video-views">👁️ ${vViews} צפיות</div>
                                <video preload="metadata" controls controlsList="nodownload" src="https://files.catbox.moe/${vName}#t=0.1"></video>
                                <a href="https://demper.org/4/cd97dd66aac08206ff8fcb6dc85e8b08" target="_blank" class="smart-btn">🔥 צפה באיכות גבוהה HD</a>
                            </div>
                        `);
                    }
                </script>
            </div>

            <!-- مكان عرض البانر الأصلي (Native Banner) و بنر 300x250 -->
            <div class="mid-ads-container">
                <script async="async" data-cfasync="false" src="https://dcengg.org/21/c09daea963d6cca1b172e88ddfa0ee51"></script>
                <div id="container-c09daea963d6cca1b172e88ddfa0ee51"></div>
            </div>

            <div class="mid-ads-container">
                <script>
                  atOptions = {
                     key  :  'acb79a2efda8a0e4fae251b979f31414',
                     format  :  'iframe',
                     height  : 250,
                     width  : 300,
                     params  : {}
                  };
                </script>
                <script src="https://dcengg.org/22/acb79a2efda8a0e4fae251b979f31414"></script>
            </div>
        </div>

        <footer>
            <div class="footer-title">שתף את הפלטפורמה וצור קשר</div>
            <div class="social-buttons">
                <a href="https://wa.me/" class="btn whatsapp">WhatsApp</a>
                <a href="https://t.me/" class="btn telegram">Telegram</a>
                <a href="https://facebook.com" class="btn facebook">Facebook</a>
                <a href="https://demper.org/4/cd97dd66aac08206ff8fcb6dc85e8b08" target="_blank" class="btn smart-link-btn">🔥 VIP מבצעי</a>
            </div>
            <div class="copyright">
                כל הזכויות שמורות © 2026 | סרטונים חמים בישראל
            </div>
        </footer>

        <script>
            function openNav() { document.getElementById("mySidebar").style.width = "220px"; }
            function closeNav() { document.getElementById("mySidebar").style.width = "0"; }
        </script>
    </body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
