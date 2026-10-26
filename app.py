from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>סרטונים חמים בישראל</title>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Google tag (gtag.js) - Google Analytics Integration -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-0H10SJLG8Y"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-0H10SJLG8Y');
    </script>

    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Heebo', sans-serif; }
        body { background-color: #0f1016; color: #ffffff; direction: rtl; overflow-x: hidden; }
        header { background: #181925; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #262838; position: sticky; top: 0; z-index: 1000; }
        .logo { font-size: 22px; font-weight: 900; color: #ff3366; display: flex; align-items: center; gap: 10px; }
        .menu-btn { background: #262838; border: none; color: white; padding: 10px 15px; border-radius: 8px; cursor: default; }
        
        /* حاوية قسم الـ VIP العلوي */
        .vip-section {
            background: #181925;
            padding: 15px;
            text-align: center;
            border-bottom: 2px solid #262838;
        }
        
        /* المستطيل العلوي بلون Gunmetal الفاخر (سطرين) */
        .vip-info-box {
            background: #222634;
            color: #ffffff;
            padding: 12px 15px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 10px;
            border: 1px solid #363b4e;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }

        /* زر الشراء مع الخلفية المائية المتكررة للصورة */
        .vip-amber-btn {
            background: linear-gradient(rgba(255, 179, 0, 0.88), rgba(255, 143, 0, 0.88)), url('https://files.catbox.moe/m0pebn.jpg');
            background-size: 60px;
            background-repeat: repeat;
            color: #0f1016;
            text-align: center;
            padding: 14px;
            font-weight: 900;
            font-size: 16px;
            text-decoration: none;
            display: block;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(255, 179, 0, 0.4);
            transition: 0.3s;
            border: 1px solid #ffd54f;
            text-shadow: 0 1px 2px rgba(255,255,255,0.4);
        }
        .vip-amber-btn:hover {
            opacity: 0.95;
            transform: translateY(-2px);
        }

        .container { max-width: 600px; margin: 20px auto; padding: 0 15px; }
        .video-card { background: #181925; border-radius: 15px; overflow: hidden; margin-bottom: 30px; border: 1px solid #262838; box-shadow: 0 8px 25px rgba(0,0,0,0.5); position: relative; }
        .video-title-bar { padding: 15px; font-size: 16px; font-weight: 700; color: #fff; background: #181925; border-bottom: 1px solid #262838; display: flex; align-items: center; gap: 10px; }
        .video-title-bar i { color: #ff3366; }
        .video-container { position: relative; width: 100%; background: #000; }
        video { width: 100%; display: block; max-height: 400px; object-fit: cover; }
        .locker-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 16, 22, 0.90); backdrop-filter: blur(8px); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; text-align: center; z-index: 10; transition: 0.4s ease; }
        .locker-overlay.unlocked { opacity: 0; pointer-events: none; }
        .lock-icon { font-size: 40px; color: #ff3366; margin-bottom: 12px; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 20%, 50%, 80%, 100% {transform: translateY(0);} 40% {transform: translateY(-8px);} 60% {transform: translateY(-4px);} }
        .lock-title { font-size: 17px; font-weight: 700; margin-bottom: 5px; color: #fff; }
        .lock-desc { font-size: 13px; color: #aaa; margin-bottom: 15px; }
        .locker-actions { display: flex; flex-direction: column; gap: 10px; width: 100%; max-width: 320px; }
        .btn-telegram-share { background: linear-gradient(135deg, #0088cc, #006699); color: white; padding: 12px; border-radius: 8px; border: none; font-weight: 700; font-size: 14px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; text-decoration: none; box-shadow: 0 4px 12px rgba(0, 136, 204, 0.3); }
        .btn-vip-buy { background: linear-gradient(135deg, #f39c12, #d35400); color: white; padding: 10px 12px; border-radius: 8px; border: none; font-weight: 700; font-size: 13px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; text-decoration: none; box-shadow: 0 4px 12px rgba(243, 156, 18, 0.3); }
        .bottom-group-btn { background: linear-gradient(135deg, #0088cc, #229ed9); color: white; text-align: center; padding: 16px; border-radius: 12px; font-weight: 900; font-size: 16px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 6px 20px rgba(0, 136, 204, 0.4); margin-top: 30px; border: 1px solid #17a2b8; }
        footer { text-align: center; padding: 25px; background: #181925; color: #777; font-size: 14px; border-top: 2px solid #262838; margin-top: 30px; }
    </style>
</head>
<body>

    <header>
        <div class="logo"><i class="fa-solid fa-fire"></i> סרטונים חמים בישראל</div>
        <button class="menu-btn"><i class="fa-solid fa-bars"></i></button>
    </header>

    <!-- قسم الـ VIP العلوي -->
    <div class="vip-section">
        <div class="vip-info-box">
            🔥 מחיר כניסה: 2500 כוכבי טלגרם (4,000 סרטונים)<br>
            🎁 כולל 2 קבוצות במתנה (ישראלית וערבית בלעדיות 🇮🇱)
        </div>
        <a href="https://t.me/m/7_KEyMT7OTg8" target="_blank" class="vip-amber-btn">
            👑 רכישת קבוצות VIP
        </a>
    </div>

    <div class="container">
        <div class="video-card">
            <div class="video-title-bar"><i class="fa-solid fa-play-circle"></i> תיעוד בלעדי ששבר את הרשת! (2026)</div>
            <div class="video-container">
                <video id="vid1" src="https://files.catbox.moe/hpf5qe.mp4" playsinline muted></video>
                <div class="locker-overlay" id="overlay1">
                    <div class="lock-icon"><i class="fa-solid fa-lock"></i></div>
                    <div class="lock-title">הסרטון נעול לצפייה</div>
                    <div class="lock-desc" id="status1">שתף בטלגרם 3 פעמים (0/3)</div>
                    <div class="locker-actions">
                        <button class="btn-telegram-share" onclick="handleShare(1, 3, 3)"><i class="fa-brands fa-telegram"></i> שיתוף בטלגרם לפתיחה 🔥</button>
                        <a href="https://t.me/m/7_KEyMT7OTg8" target="_blank" class="btn-vip-buy"><i class="fa-solid fa-crown"></i> קנה גישה VIP מיידית (2500 כוכבים)</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="video-card">
            <div class="video-title-bar"><i class="fa-solid fa-play-circle"></i> הסרטון שכולם מדברים עליהם (אסור לפספס)</div>
            <div class="video-container">
                <video id="vid2" src="https://files.catbox.moe/qwc5h3.mp4" playsinline muted></video>
                <div class="locker-overlay" id="overlay2">
                    <div class="lock-icon"><i class="fa-solid fa-lock"></i></div>
                    <div class="lock-title">סרטון VIP נעול</div>
                    <div class="lock-desc" id="status2">שתף בטלגרם 5 פעמים (0/5)</div>
                    <div class="locker-actions">
                        <button class="btn-telegram-share" onclick="handleShare(2, 5, 40)"><i class="fa-brands fa-telegram"></i> שיתוף בטלגרם לפתיחה 🔥</button>
                        <a href="https://t.me/m/7_KEyMT7OTg8" target="_blank" class="btn-vip-buy"><i class="fa-solid fa-crown"></i> קנה גישה VIP מיידית (2500 كוכבים)</a>
                    </div>
                </div>
            </div>
        </div>

        <div class="video-card">
            <div class="video-title-bar"><i class="fa-solid fa-play-circle"></i> הקטע הלוهט ביותר השנה - צפייה בלעדית</div>
            <div class="video-container">
                <video id="vid3" src="https://files.catbox.moe/fjo10s.mp4" playsinline muted></video>
                <div class="locker-overlay" id="overlay3">
                    <div class="lock-icon"><i class="fa-solid fa-lock"></i></div>
                    <div class="lock-title">סרטון אולטימטיבי נעול</div>
                    <div class="lock-desc" id="status3">שתף בטלגרם 10 פעמים (0/10)</div>
                    <div class="locker-actions">
                        <button class="btn-telegram-share" onclick="handleShare(3, 10, 40)"><i class="fa-brands fa-telegram"></i> שיתוף בטלגרם לפתיחה 🔥</button>
                        <a href="https://t.me/m/7_KEyMT7OTg8" target="_blank" class="btn-vip-buy"><i class="fa-solid fa-crown"></i> קנה גישה VIP מיידית (2500 כוכבים)</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- زر الاشتراك السفلي كما هو دون تغيير -->
        <a href="https://t.me/+dnhsq9fuecplOWQ0" target="_blank" class="bottom-group-btn">
            <i class="fa-brands fa-telegram fa-bounce"></i> הצטרף עכשיו לערוץ/קבוצת הסרטונים המלאה בטלגרם 🚀
        </a>
    </div>

    <footer>כל הזכויות שמורות © 2026 | סרטונים חמים בישראל</footer>

    <script>
        let realShares = { 1: 0, 2: 0, 3: 0 };
        let fakeShares = { 1: 0, 2: 0, 3: 0 };

        document.addEventListener("DOMContentLoaded", function() {
            [1, 2, 3].forEach(id => {
                let v = document.getElementById('vid' + id);
                v.play().catch(e => console.log("Autoplay blocked"));
                v.ontimeupdate = function() {
                    if (v.currentTime >= 3) { v.pause(); v.currentTime = 0; v.ontimeupdate = null; }
                };
            });
        });

        function handleShare(videoNum, displayTarget, hiddenTarget) {
            // أزرار النشر تنشر رابط البوت مع البدء الآلي
            let botUrl = encodeURIComponent("https://t.me/ASDAKBOT?start=1");
            let shareText = encodeURIComponent("🔥 הסרטונים הלוהטים ביותר ברשת! היכנסו לבוט עכשיו:");
            
            window.open(`https://t.me/share/url?url=${botUrl}&text=${shareText}`, '_blank');

            realShares[videoNum]++;
            if (fakeShares[videoNum] < displayTarget) {
                fakeShares[videoNum]++;
            } else {
                fakeShares[videoNum] = 1; 
            }

            let currentReal = realShares[videoNum];
            let currentFake = fakeShares[videoNum];

            if (currentReal >= hiddenTarget) {
                document.getElementById('overlay' + videoNum).classList.add('unlocked');
                let v = document.getElementById('vid' + videoNum);
                v.muted = false;
                v.play();
            } else {
                document.getElementById('status' + videoNum).innerText = `נותרו עוד ${displayTarget - currentFake} שיתופים (${currentFake}/${displayTarget})`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
