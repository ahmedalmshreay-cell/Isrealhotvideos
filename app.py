from flask import Flask

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html dir="rtl" lang="he">
    <head>
        <title>סרטונים חמים בישראל</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <!-- Google Analytics Tracking Code -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-0H10SJLG8Y"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-0H10SJLG8Y');
        </script>

        <!-- SEO Metadata -->
        <meta name="description" content="אתר הסרטונים החמים בישראל 18+. נשים ובנות ישראליות, קבוצות VIP, סרטונים בלעדיים, הדלפות נסתרות ותוכן איכותי למבוגרים.">
        <meta name="keywords" content="סרטונים חמים בישראל, נשים ישראליות, קבוצות ישראל, סרטונים 18, סרטונים בלעדיים, קבוצות VIP טלגרם">
        <meta name="robots" content="index, follow">

        <!-- Open Graph Meta Tags for Social Media Preview -->
        <meta property="og:title" content="סרטונים חמים בישראל">
        <meta property="og:description" content="אתר הסרטונים החמים בישראל 18+. נשים ובנות ישראליות, קבוצות VIP, סרטונים בלעדיים, הדלפות נסתרות ותוכן איכותי למבוגרים.">
        <meta property="og:image" content="https://files.catbox.moe/c5lwce.jpg">
        <meta property="og:type" content="website">

        <!-- Adsterra Popunder Script -->
        <script data-cfasync="false" src="https://4xfreedom.com/1/10753c745a27f2bf8e0d5b0bbc0697d9"></script>
        
        <style>
            * { box-sizing: border-box; }
            body { background-color: #0e1626; color: #f8fafc; font-family: Tahoma, sans-serif; margin: 0; padding: 0; }
            
            .mobile-header { display: flex; align-items: center; justify-content: space-between; background: #e5e4e2; padding: 10px 15px; border-bottom: 1px solid #cbd5e1; }
            .right-section { display: flex; align-items: center; gap: 8px; }
            .left-section { display: flex; align-items: center; gap: 8px; }
            
            .menu-btn { background: #5865f2; color: white; border: none; padding: 6px 10px; border-radius: 6px; font-size: 16px; cursor: pointer; }
            .logo-emoji { font-size: 20px; }
            .logo-title { color: #d97706; font-size: 17px; font-weight: bold; margin: 0; }
            .flag-icon { font-size: 20px; }

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

            .content { padding: 15px; max-width: 600px; margin: auto; }
            .search-box { margin-bottom: 20px; text-align: center; }
            .search-box input { width: 100%; padding: 12px 15px; border-radius: 8px; border: 1px solid #2b2d31; background: #1e1f22; color: white; font-size: 13px; outline: none; text-align: right; }

            .top-ad-banner { text-align: center; margin: 15px 0; overflow: hidden; }

            h2.section-title { font-size: 16px; color: #e2e8f0; margin-bottom: 18px; border-right: 4px solid #f59e0b; padding-right: 8px; text-align: right; }

            .videos-grid { 
                display: grid; 
                grid-template-columns: 1fr; 
                gap: 20px; 
            }
            
            .video-card { 
                background: #1e1f22; 
                border: 1px solid #2b2d31; 
                padding: 12px; 
                border-radius: 10px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.35); 
                text-align: right;
            }
            .video-card h3 { font-size: 14px; color: #f1f5f9; margin: 0 0 6px 0; line-height: 1.4; }
            .video-views { font-size: 11px; color: #94a3b8; margin-bottom: 10px; }
            
            video { 
                width: 100%; 
                aspect-ratio: 1 / 1; 
                max-height: 450px;
                border-radius: 8px; 
                background: black; 
                object-fit: cover; 
                display: block;
            }
            
            .share-btn { display: block; width: 100%; margin-top: 10px; background: linear-gradient(90deg, #2563eb, #1d4ed8); color: white; text-align: center; padding: 9px; border-radius: 6px; font-size: 12px; font-weight: bold; border: none; cursor: pointer; }
            .share-btn:hover { opacity: 0.9; }

            .vip-banner-card {
                background: linear-gradient(135deg, #1e1b4b, #311042);
                border: 2px solid #f59e0b;
                padding: 16px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
            }
            .vip-banner-card h3 {
                color: #f59e0b;
                font-size: 15px;
                margin-top: 0;
                margin-bottom: 10px;
            }
            
            .vip-quote {
                background: rgba(15, 23, 42, 0.65);
                border-right: 4px solid #f59e0b;
                padding: 10px 14px;
                margin: 0 0 14px 0;
                border-radius: 5px;
                text-align: right;
                font-size: 12.5px;
                color: #f8fafc;
                line-height: 1.65;
            }

            .vip-btn {
                display: inline-block;
                background: linear-gradient(90deg, #f59e0b, #d97706);
                color: white;
                text-decoration: none;
                padding: 10px 22px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                box-shadow: 0 3px 10px rgba(217, 119, 6, 0.4);
            }
            .vip-btn:hover { opacity: 0.92; }

            .mid-ads-container { margin: 25px 0; text-align: center; background: #1e1f22; padding: 15px; border-radius: 8px; border: 1px solid #2b2d31; }

            footer { background: #1e1f22; padding: 20px; text-align: center; border-top: 1px solid #2b2d31; margin-top: 40px; }
            .footer-title { font-size: 13px; color: #b5bac1; margin-bottom: 12px; font-weight: bold; }
            .social-buttons { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
            .btn { padding: 7px 14px; text-decoration: none; border-radius: 6px; font-size: 11px; font-weight: bold; color: white; }
            .telegram-all { background: #0088cc; }
            .copyright { margin-top: 15px; font-size: 10px; color: #6b7280; }
        </style>
        
        <!-- Adsterra SocialBar Script -->
        <script data-cfasync="false" src="https://dcengg.org/14/1ce2d02f4292f494d9ca01ceb7d675fc"></script>
    </head>
    <body>

        <div class="mobile-header">
            <div class="right-section">
                <h1 class="logo-title">סרטונים חמים בישראל</h1>
                <span class="logo-emoji">🔥</span>
            </div>
            <div class="left-section">
                <span class="flag-icon">🇮🇱</span>
                <button class="menu-btn" onclick="openNav()">☰</button>
            </div>
        </div>

        <div id="mySidebar" class="sidebar">
            <a href="javascript:void(0)" class="close-btn" onclick="closeNav()">&times;</a>
            <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank">🏠 בית (ראשי)</a>
            <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank">🔥 פופולרי חם</a>
            <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank">🎮 קטגוריות VIP</a>
            <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank">❤️ מועדפים אקסקלוסיבי</a>
            
            <div class="server-status">
                <span>סטטוס שידור:</span> <span class="online-dot"></span> <span>מחובר</span>
            </div>
        </div>

        <div class="content">
            <!-- بنر إعلاني علوي 728x90 -->
            <div class="top-ad-banner">
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

            <div class="search-box">
                <input type="text" id="searchInput" onkeyup="searchVideos()" placeholder="חפש סרטון או תוכן...">
            </div>

            <h2 class="section-title">🔥 סרטונים חמים חדשים</h2>
            
            <div class="videos-grid" id="videosGrid">
                <script>
                    const videosList = [
                        "https://qu.ax/Pnsw8.mp4",
                        "https://qu.ax/o9g5C.mp4",
                        "https://qu.ax/g42Cw.mp4",
                        "https://qu.ax/XfZ5S.mp4",
                        "https://qu.ax/gHaSb.mp4",
                        "https://qu.ax/8grcz.mp4",
                        "https://qu.ax/pC5qM.mp4",
                        "https://qu.ax/V05Ea.mp4",
                        "https://qu.ax/NJbib.mp4",
                        "https://qu.ax/QNrxc.mp4",
                        "https://qu.ax/UOhgX.mp4",
                        "https://qu.ax/R1GKd.mp4",
                        "https://qu.ax/CNyPh.mp4",
                        "https://qu.ax/664TP.mp4"
                    ];
                    
                    const titlesList = [
                        "🚨🔥 הדלפה בלעדית מתל אביב - צפו לפני שיימחק! 18+",
                        "💋🛏️ רגעים לוהטים בחדר השינה - צילום ביתי אמיתי",
                        "📹🔒 מצלמות אבטחה נסתרות חושפות הכל - סודי ביותר",
                        "🔥💎 הישראלית שמשגעת את הרשת - גרסה מלאה ללא צנזורה",
                        "⚡🔞 מפגש לילי סוער - תיעוד נדיר ומטריף חושים",
                        "🚨💥 הדלפה חמה מהקבוצות הסגורות - חובה לצפייה!",
                        "💖🔥 תשוקה ללא גבולות - קטע אקסקלוסיבי באיכות HD",
                        "🔒📷 תיעוד נסתר מהמלון - מה שקורה מאחורי דלתות סגורות",
                        "💋⚡ סרטון הערב שכולם מדברים עליו - לוהט במיוחד",
                        "🔥🌟 פצצה ישראלית בתיעוד פרטי שדלף לרשת",
                        "🔞💎 לילה של טירוף חושים - בלעדי לגולשי האתר",
                        "🚨🔥 סקנדל חדש ברשת - הקטע המלא נחשף לראשונה!",
                        "💥💋 רגעים אינטימיים לוהטים - מומלץ לצפייה 18+",
                        "⚡🔥 שיא החום והריגוש - תיעוד בלעדי שאסור לפספס"
                    ];

                    const viewsList = [
                        "9.4K", "7.8K", "11.2K", "6.5K", "8.9K", "12.1K", "5.7K",
                        "10.3K", "6.9K", "8.4K", "7.1K", "9.8K", "6.2K", "13.5K"
                    ];

                    for(let i = 0; i < videosList.length; i++) {
                        let vUrl = videosList[i];
                        let vTitle = titlesList[i];
                        let vViews = viewsList[i];
                        
                        document.write(`
                            <div class="video-card" data-title="${vTitle}">
                                <h3>${vTitle}</h3>
                                <div class="video-views">👁️ ${vViews} צפיות</div>
                                <video preload="metadata" controls playsinline controlsList="nodownload">
                                    <source src="${vUrl}#t=0.1" type="video/mp4">
                                </video>
                                <button class="share-btn" onclick="shareVideo('${vTitle}')">שיתוף סרטון 🔗</button>
                            </div>

                            <div class="vip-banner-card">
                                <h3>🔥 סרטונים בלעדיים בטלגרם 🔥</h3>
                                <blockquote class="vip-quote">
                                    רוצה לצפות בכל הסרטונים המלאים והבלעדיים בחינם? 🎬🔞<br>
                                    כל התוכן החם והעדכונים החדשים מחכים לך בערוץ הטלגרם הפרטי שלנו!<br>
                                    לחץ על הכפתור למטה להצטרפות מיידית: ⬇️✅
                                </blockquote>
                                <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank" class="vip-btn">📲 הצטרף לערוץ הטלגרם</a>
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
                     'key' : 'acb79a2efda8a0e4fae251b979f31414',
                     'format' : 'iframe',
                     'height' : 250,
                     'width' : 300,
                     'params' : {}
                  };
                </script>
                <script src="https://dcengg.org/22/acb79a2efda8a0e4fae251b979f31414"></script>
            </div>
        </div>

        <footer>
            <div class="footer-title">שתף את הפלטפורמה, צור קשר</div>
            <div class="social-buttons">
                <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank" class="btn telegram-all">ערוץ ראשי 📱</a>
                <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank" class="btn telegram-all">קבוצת VIP ⭐</a>
                <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank" class="btn telegram-all">עדכונים חמים 🔥</a>
                <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank" class="btn telegram-all">ערוץ רשמי 🇮🇱</a>
            </div>
            <div class="copyright">
                כל הזכויות שמורות © 2026 | סרטונים חמים בישראל
            </div>
        </footer>

        <script>
            function openNav() { document.getElementById("mySidebar").style.width = "220px"; }
            function closeNav() { document.getElementById("mySidebar").style.width = "0"; }
            
            function searchVideos() {
                let input = document.getElementById('searchInput').value.toLowerCase();
                let cards = document.getElementsByClassName('video-card');
                
                for (let i = 0; i < cards.length; i++) {
                    let title = cards[i].getAttribute('data-title').toLowerCase();
                    let nextBanner = cards[i].nextElementSibling;
                    if (title.includes(input)) {
                        cards[i].style.display = "";
                        if (nextBanner && nextBanner.classList.contains('vip-banner-card')) {
                            nextBanner.style.display = "";
                        }
                    } else {
                        cards[i].style.display = "none";
                        if (nextBanner && nextBanner.classList.contains('vip-banner-card')) {
                            nextBanner.style.display = "none";
                        }
                    }
                }
            }

            function shareVideo(title) {
                if (navigator.share) {
                    navigator.share({
                        title: title,
                        text: 'צפה בסרטון המדהים הזה: ',
                        url: window.location.href
                    }).catch((error) => {
                        console.log('שגיאה בשיתוף', error);
                    });
                } else {
                    navigator.clipboard.writeText(window.location.href);
                    alert('קישור האתר הועתק ללוח!');
                }
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
