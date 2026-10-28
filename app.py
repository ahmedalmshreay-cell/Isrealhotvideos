from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# مسار خاص لخدمة ملف عامل الخدمة الخاص بـ OneSignal
@app.route('/OneSignalSDKWorker.js')
def serve_onesignal_worker():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'OneSignalSDKWorker.js')

HTML_PAGE = """
<html dir="rtl" lang="he">
    <head>
        <title>סרטונים חמים בישראל</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        
        <!-- OneSignal Web SDK مع النص بالعبرية -->
        <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
        <script>
          window.OneSignalDeferred = window.OneSignalDeferred || [];
          OneSignalDeferred.push(async function(OneSignal) {
            await OneSignal.init({
              appId: "083248fd-7d06-45bb-b775-112212132b43",
              notifyButton: {
                enable: true,
              },
              promptOptions: {
                slidedown: {
                  prompts: [
                    {
                      type: "push",
                      autoPrompt: true,
                      text: {
                        actionMessage: "📢 אנא היռשם כדי לקבל את כל הסרטונים החדשים מיד עם יציאתם 🔞",
                        acceptButton: "הירשם",
                        cancelButton: "מאוחר יותר"
                      }
                    }
                  ]
                }
              }
            });
          });
        </script>

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
            
            .share-btn { display: block; width: 100%; margin-top: 8px; background: linear-gradient(90deg, #2563eb, #1d4ed8); color: white; text-align: center; padding: 6px; border-radius: 5px; font-size: 11px; font-weight: bold; border: none; cursor: pointer; }
            .share-btn:hover { opacity: 0.9; }

            .vip-banner-card {
                grid-column: span 2;
                background: linear-gradient(135deg, #1e1b4b, #311042);
                border: 2px solid #f59e0b;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
            }
            .vip-banner-card h3 {
                color: #f59e0b;
                font-size: 14px;
                margin-top: 0;
                margin-bottom: 10px;
            }
            
            .vip-quote {
                background: rgba(15, 23, 42, 0.6);
                border-right: 4px solid #f59e0b;
                padding: 10px 12px;
                margin: 0 0 12px 0;
                border-radius: 4px;
                text-align: right;
                font-size: 12px;
                color: #f8fafc;
                line-height: 1.6;
                white-space: pre-line;
            }

            .vip-btn {
                display: inline-block;
                background: linear-gradient(90deg, #f59e0b, #d97706);
                color: white;
                text-decoration: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            .vip-btn:hover { opacity: 0.9; }

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
                     key : '8a898fb2ff79e4f617a887a1fc16c862',
                     format : 'iframe',
                     height : 90,
                     width : 728,
                     params : {}
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
                        "in681v.MOV", "yo3jfj.mp4", "oo7zyt.MP4",
                        "hpf5qe.mp4", "qwc5h3.mp4", "fjo10s.mp4", "qwc5h3.mp4",
                        "wio4kl.mp4", "vo29gf.mp4", "qseq0i.mp4", "762n5t.mp4", "6qs6t8.mp4", "xtrtpd.mp4", 
                        "xovx5v.mp4", "gca6vk.mp4", "sjj6dd.mp4", "vzginq.mp4", "lwbdy1.mp4", "o36fln.mp4", 
                        "rv9c5v.mp4", "lkqw9a.mp4", "y9teda.mp4", "ly7k1z.mp4", "15e5t5.mp4", "dtklvc.mp4", 
                        "k79dhg.mp4", "uk5hrq.mp4", "nvfstt.mp4", "9nps91.mp4"
                    ];
                    
                    const titlesList = [
                        "🚨📷 הדלפות מצלמות אבטחה נסתרות - בלעדי 18+",
                        "🛏️🔥 צפו במצלמת חדרי השינה של זוגות - לוהט במיוחד",
                        "📼🔒 קטעי וידאו אמיתיים ממצלמות אבטחה - סודי ביותר",
                        "🚨🔥 בלעדי ולוהט במיוחד - חובה צפייה 18+",
                        "💋💥 סרטון סודי ומטורף שעושה רושם רציני",
                        "🔥💎 אקסקלוסיבי ברשת - מראות קשים ומרגשים",
                        "⚡🔥 פצצת הערב - צפו לפני מחיקה!",
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
                        "💖 אהבה אסורה - סודות אפלים",
                        "🔥 טירוף חושים - פיצוץ חושים אמיתי",
                        "⚡ פצצת שסי - קטעים יוצאי דופן",
                        "🔥 סרטון מטורף - הנאה ללא גבולות",
                        "💎 VIP בלעדי - תוכן למבוגרים בלבד",
                        "🔥 חם מהתנור - בלעדי לחלוטין",
                        "💋 מגע של קסם - מפגשים לוהטים",
                        "🔥 סודות אפלים - ריגושים אבסולוטיים",
                        "🌟 אקסטרים - אתגרים לוהטים",
                        "🔥 שיא החום - שיא המתח והריגוש",
                        "💖 מומלץ ביותר - המבוקש ביותר",
                        "🔥 בלעדי לחברי האתר - לילה מיוחד"
                    ];

                    const viewsList = ["7.4K", "8.9K", "6.5K", "5.2K", "4.8K", "6.1K", "3.9K", "1.4K", "850", "3.2K", "620", "2.1K", "940", "4.5K", "1.1K", "780", "2.9K", "1.8K", "3.6K", "530", "1.2K", "2.4K", "890", "1.7K", "3.1K", "920", "4.0K", "1.3K", "2.7K"];

                    for(let i = 0; i < videosList.length; i++) {
                        let vName = videosList[i];
                        let vTitle = titlesList[i];
                        let vViews = viewsList[i];
                        
                        document.write(`
                            <div class="video-card" data-title="${vTitle}">
                                <h3>${vTitle}</h3>
                                <div class="video-views">👁️ ${vViews} צפיות</div>
                                <video preload="metadata" controls controlsList="nodownload" src="https://files.catbox.moe/${vName}#t=0.1"></video>
                                <button class="share-btn" onclick="shareVideo('${vTitle}')">שיתוף סרטון 🔗</button>
                            </div>
                        `);

                        if ((i + 1) % 6 === 0 && i < videosList.length - 1) {
                            document.write(`
                                <div class="vip-banner-card">
                                    <h3>📢 לצפייה בכל התוכן 🔥</h3>
                                    <blockquote class="vip-quote">
                                        👇 הירשמו לערוץ הרשמי כדי לקבל את כל הסרטונים החדשים והמיוחדים ברגע פרסומם וללא פרסומות 📲
                                    </blockquote>
                                    <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank" class="vip-btn">🔞 לחצו כאן להצטרפות 🔗</a>
                                </div>
                            `);
                        }
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
                     key : 'acb79a2efda8a0e4fae251b979f31414',
                     format : 'iframe',
                     height : 250,
                     width : 300,
                     params : {}
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
                    if (title.includes(input)) {
                        cards[i].style.display = "";
                    } else {
                        cards[i].style.display = "none";
                    }
                }
            }

            function shareVideo(title) {
                if (navigator.share) {
                    navigator.share({
                        title: title,
                        text: 'צפה בסרטון המדהים הזה:',
                        url: window.location.href
                    }).then(() => {
                        console.log('تمت المشاركة بنجاح');
                    }).catch((error) => {
                        console.log('خطأ في المشاركة', error);
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
