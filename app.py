import os
from flask import Flask, render_template_string, make_response

app = Flask(__name__)

# --- الإعدادات الأساسية القابلة للتعديل بسهولة ---
ADSGRAM_BLOCK_ID = "60722"
REQUIRED_SHARES = 5
SHARE_LINK = "https://t.me/+dnhsq9fuecplOWQ0"
SHARE_MESSAGE = "🔥 סרטונים בלעדיים והדלפות חמות 18+ בחינם! 🔞\nהגישה נפתחה עכשיו לזמן מוגבל 👇"
UNLOCK_REDIRECT_LINK = "https://t.me/+dnhsq9fuecplOWQ0"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>פתיחת גישה לתוכן המלא 🔒</title>

    <!-- Telegram WebApp SDK -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>

    <!-- Adsgram Rewarded Ads SDK -->
    <script src="https://sad.adsgram.ai/js/sad.min.js"></script>

    <!-- Google Fonts: Heebo -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@500;700;900&display=swap" rel="stylesheet">

    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-0H10SJLG8Y"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-0H10SJLG8Y');
    </script>

    <style>
        :root {
            --bg-dark: #080c14;
            --card-bg: #0f1522;
            --card-border: #1e293b;
            --primary-blue: #2563eb;
            --primary-blue-hover: #1d4ed8;
            --track-bg: #1e293b;
            --text-white: #f8fafc;
            --text-muted: #94a3b8;
            --success-green: #16a34a;
            --success-green-hover: #15803d;
        }

        * {
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
            user-select: none;
        }

        body {
            margin: 0;
            padding: 16px;
            min-height: 100vh;
            background-color: var(--bg-dark);
            color: var(--text-white);
            font-family: 'Heebo', sans-serif;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .lock-card {
            width: 100%;
            max-width: 400px;
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 22px;
            padding: 28px 22px;
            text-align: center;
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.65);
        }

        .lock-title {
            font-size: 21px;
            font-weight: 900;
            margin: 0 0 8px 0;
            letter-spacing: 0.3px;
            color: var(--text-white);
        }

        .lock-subtitle {
            font-size: 13.5px;
            color: var(--text-muted);
            margin: 0 0 22px 0;
            line-height: 1.5;
        }

        .progress-track {
            width: 100%;
            height: 12px;
            background-color: var(--track-bg);
            border-radius: 999px;
            overflow: hidden;
            margin-bottom: 10px;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
        }

        .progress-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #3b82f6, #2563eb);
            border-radius: 999px;
            transition: width 0.45s cubic-bezier(0.22, 1, 0.36, 1), background 0.3s ease;
        }

        .progress-fill.completed {
            background: linear-gradient(90deg, #22c55e, #16a34a);
        }

        .stats-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12.5px;
            font-weight: 700;
            color: var(--text-muted);
            margin-bottom: 24px;
            padding: 0 2px;
        }

        .btn {
            width: 100%;
            padding: 15px 18px;
            border-radius: 14px;
            font-family: 'Heebo', sans-serif;
            font-size: 15.5px;
            font-weight: 900;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: transform 0.15s ease, background-color 0.2s ease, box-shadow 0.2s ease;
            border: none;
        }

        .btn:active {
            transform: scale(0.97);
        }

        .btn-share {
            background-color: var(--primary-blue);
            color: #ffffff;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35);
            margin-bottom: 12px;
        }

        .btn-share:hover {
            background-color: var(--primary-blue-hover);
        }

        .btn-unlock {
            background-color: #161e2e;
            color: var(--text-muted);
            border: 1px solid #283548;
        }

        .btn-unlock.ready {
            background-color: var(--success-green);
            color: #ffffff;
            border-color: var(--success-green);
            box-shadow: 0 6px 20px rgba(22, 163, 74, 0.4);
            animation: pulseGreen 1.8s infinite;
        }

        .btn-unlock.ready:hover {
            background-color: var(--success-green-hover);
        }

        @keyframes pulseGreen {
            0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.6); }
            70% { box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
            100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
        }

        .status-alert {
            margin-top: 16px;
            padding: 11px 14px;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 700;
            display: none;
            line-height: 1.4;
        }

        .status-alert.warning {
            display: block;
            background-color: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.35);
            color: #fca5a5;
        }

        .status-alert.success {
            display: block;
            background-color: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.35);
            color: #86efac;
        }
    </style>
</head>
<body>

    <div class="lock-card">
        <h1 class="lock-title">התוכן המלא נעול 🔒🔞</h1>
        <p class="lock-subtitle">שתף את הקישור עם <b style="color:#fff;">{{ required_shares }} חברים</b> או קבוצות בטלגרם כדי לפתוח את הצפייה המלאה מיד</p>

        <div class="progress-track">
            <div class="progress-fill" id="progressBar"></div>
        </div>

        <div class="stats-row">
            <span id="tasksCounter">0 / {{ required_shares }} שיתופים</span>
            <span id="percentText">0% הושלם</span>
        </div>

        <button class="btn btn-share" id="shareBtn" onclick="handleShare()">
            <span id="shareBtnText">שתף עם חברים 🥵</span>
        </button>

        <button class="btn btn-unlock" id="unlockBtn" onclick="handleUnlock()">
            <span id="unlockBtnText">צפייה בסרטונים (0/{{ required_shares }})</span>
        </button>

        <div class="status-alert" id="statusAlert"></div>
    </div>

    <script>
        const ADSGRAM_BLOCK_ID = {{ block_id | tojson }};
        const REQUIRED_SHARES = {{ required_shares }};
        const SHARE_LINK = {{ share_link | tojson }};
        const SHARE_MESSAGE = {{ share_message | tojson }};
        const UNLOCK_URL = {{ unlock_url | tojson }};
        const STORAGE_KEY = "tg_share_progress_v2";

        let currentShares = parseInt(localStorage.getItem(STORAGE_KEY) || "0", 10);
        if (isNaN(currentShares) || currentShares < 0) currentShares = 0;
        if (currentShares > REQUIRED_SHARES) currentShares = REQUIRED_SHARES;

        let isVerifying = false;
        let pendingShareIncrement = false;
        let AdController = null;

        if (window.Telegram && window.Telegram.WebApp) {
            const tg = window.Telegram.WebApp;
            tg.ready();
            tg.expand();
            if (tg.setHeaderColor) tg.setHeaderColor('#080c14');
            if (tg.setBackgroundColor) tg.setBackgroundColor('#080c14');
        }

        if (window.Adsgram) {
            try {
                AdController = window.Adsgram.init({ blockId: ADSGRAM_BLOCK_ID });
            } catch (e) {
                console.warn("Adsgram init error:", e);
            }
        }

        function showRewardedAd(onFinish) {
            if (!AdController) {
                onFinish();
                return;
            }
            AdController.show()
                .then(() => {
                    onFinish();
                })
                .catch(() => {
                    onFinish();
                });
        }

        function updateUI() {
            const percent = Math.min(100, Math.round((currentShares / REQUIRED_SHARES) * 100));
            const progressBar = document.getElementById("progressBar");
            const tasksCounter = document.getElementById("tasksCounter");
            const percentText = document.getElementById("percentText");
            const unlockBtn = document.getElementById("unlockBtn");
            const unlockBtnText = document.getElementById("unlockBtnText");

            progressBar.style.width = percent + "%";
            tasksCounter.textContent = `${currentShares} / ${REQUIRED_SHARES} שיתופים`;
            percentText.textContent = `${percent}% הושלם`;

            if (currentShares >= REQUIRED_SHARES) {
                progressBar.classList.add("completed");
                unlockBtn.classList.add("ready");
                if (!isVerifying) {
                    unlockBtnText.textContent = "🔓 צפייה עכשיו - הגישה נפתחה!";
                }
            } else {
                progressBar.classList.remove("completed");
                unlockBtn.classList.remove("ready");
                if (!isVerifying) {
                    unlockBtnText.textContent = `צפייה בסרטונים (${currentShares}/${REQUIRED_SHARES})`;
                }
            }
        }

        function showAlert(msg, type) {
            const alertBox = document.getElementById("statusAlert");
            alertBox.textContent = msg;
            alertBox.className = "status-alert " + type;
        }

        function handleShare() {
            if (isVerifying) return;

            // وضع النص في الأعلى والرابط تحته مباشرة عبر ترك معامل url فارغاً
            const fullShareText = `${SHARE_MESSAGE}\n\n${SHARE_LINK}`;
            const tgShareUrl = `https://t.me/share/url?url=%20&text=${encodeURIComponent(fullShareText)}`;

            if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.openTelegramLink) {
                window.Telegram.WebApp.openTelegramLink(tgShareUrl);
            } else {
                window.open(tgShareUrl, "_blank");
            }

            pendingShareIncrement = true;
            setTimeout(() => {
                if (pendingShareIncrement) {
                    processShareWithAd();
                }
            }, 2200);
        }

        function processShareWithAd() {
            if (!pendingShareIncrement) return;
            pendingShareIncrement = false;

            const shareBtnText = document.getElementById("shareBtnText");
            shareBtnText.textContent = "מאמת שיתוף... ⏳";

            showRewardedAd(() => {
                shareBtnText.textContent = "שתף עם חברים 🥵";
                completeOneShare();
            });
        }

        function completeOneShare() {
            if (currentShares < REQUIRED_SHARES) {
                currentShares += 1;
                localStorage.setItem(STORAGE_KEY, currentShares.toString());
                updateUI();

                const remaining = REQUIRED_SHARES - currentShares;
                if (remaining > 0) {
                    showAlert(`✅ השיתוף נקלט! נותרו לך עוד ${remaining} שיתופים לפתיחת הגישה 📲`, "warning");
                } else {
                    showAlert("🎉 כל השיתופים הושלמו! לחץ על הכפתור הירוק לצפייה מיידית 👇", "success");
                }
            }
        }

        document.addEventListener("visibilitychange", () => {
            if (document.visibilityState === "visible" && pendingShareIncrement) {
                processShareWithAd();
            }
        });

        function handleUnlock() {
            if (isVerifying) return;

            if (currentShares >= REQUIRED_SHARES) {
                showRewardedAd(() => {
                    if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.openTelegramLink && UNLOCK_URL.startsWith("https://t.me/")) {
                        window.Telegram.WebApp.openTelegramLink(UNLOCK_URL);
                    } else {
                        window.location.href = UNLOCK_URL;
                    }
                });
                return;
            }

            isVerifying = true;
            let secondsLeft = 3;
            const unlockBtnText = document.getElementById("unlockBtnText");
            unlockBtnText.textContent = `בודק שיתופים... ${secondsLeft}s`;

            const timer = setInterval(() => {
                secondsLeft -= 1;
                if (secondsLeft > 0) {
                    unlockBtnText.textContent = `בודק שיתופים... ${secondsLeft}s`;
                } else {
                    clearInterval(timer);
                    showRewardedAd(() => {
                        isVerifying = false;
                        updateUI();
                        const remaining = REQUIRED_SHARES - currentShares;
                        showAlert(`⚠️ הגישה עדיין נעולה! נותרו לך עוד ${remaining} שיתופים כדי לפתוח את הסרטונים 🔒`, "warning");
                    });
                }
            }, 1000);
        }

        updateUI();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    response = make_response(render_template_string(
        HTML_TEMPLATE,
        block_id=ADSGRAM_BLOCK_ID,
        required_shares=REQUIRED_SHARES,
        share_link=SHARE_LINK,
        share_message=SHARE_MESSAGE,
        unlock_url=UNLOCK_REDIRECT_LINK
    ))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
