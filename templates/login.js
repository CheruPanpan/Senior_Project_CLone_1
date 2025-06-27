let lineUserId = null;

async function initializeLiff() {
    try {
        await liff.init({ liffId: "2006775290-kR3GJLnq" });
        console.log("LIFF initialized");

        if (!liff.isLoggedIn()) {
            console.log("Not logged in to LINE, starting login...");
            setTimeout(() => {
                if (!liff.isLoggedIn()) {
                    alert("LINE login timeout, please try again.");
                }
            }, 10000);
            liff.login();
            return;
        }

        const profile = await liff.getProfile();
        lineUserId = profile.userId;
        console.log("Got LINE User ID:", lineUserId);

        await checkMicrosoftLogin(lineUserId);

    } catch (error) {
        console.error("Error initializing LIFF:", error);
        alert("เกิดข้อผิดพลาดในการเชื่อมต่อ LIFF กรุณาลองใหม่อีกครั้ง");
    }
}

// Check Microsoft Login Status from server
async function checkMicrosoftLogin(userId) {
    try {
        const response = await fetch(`/api/check-login?lineUserId=${encodeURIComponent(userId)}`);
        const data = await response.json();

        if (data.microsoftLoggedIn) {
            console.log("Microsoft login found, redirecting to purchase...");
            window.location.replace(`/purchase.html?userId=${encodeURIComponent(userId)}`);
        } else {
            console.log("Microsoft login not found, staying at login page.");
            showLoginButton();
        }
    } catch (error) {
        console.error("Error checking Microsoft login:", error);
        alert("ไม่สามารถเช็กสถานะการเข้าสู่ระบบได้ กรุณาลองใหม่อีกครั้ง");
    }
}

// Show Microsoft Login Button
function showLoginButton() {
    const loginButton = document.getElementById('microsoft-login');
    if (loginButton) {
        loginButton.style.display = 'block';
        loginButton.addEventListener('click', loginWithMicrosoft);
    }
}

// Microsoft Login function
async function loginWithMicrosoft() {
    if (!lineUserId) {
        try {
            const profile = await liff.getProfile();
            lineUserId = profile.userId;
        } catch (error) {
            console.error("Error getting LINE profile:", error);
            alert("ไม่สามารถดึงข้อมูล LINE ได้ กรุณาลองใหม่");
            return;
        }
    }

    const redirectUrl = `/auth/microsoft?lineUserId=${encodeURIComponent(lineUserId)}`;
    console.log("Redirecting to Microsoft login:", redirectUrl);
    window.location.href = redirectUrl;
}

// Theme switch
function initializeThemeSwitch() {
    const themeSwitch = document.getElementById('theme-switch');
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
    themeSwitch.checked = savedTheme === 'dark';

    themeSwitch.addEventListener('click', function() {
        const theme = this.checked ? 'dark' : 'light';
        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    });
}

// Language switch
function initializeLanguageSwitch() {
    const langButtons = document.querySelectorAll('.lang-btn');
    const savedLang = localStorage.getItem('language') || 'th';
    setLanguage(savedLang);

    langButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            setLanguage(lang);
            localStorage.setItem('language', lang);
        });
    });
}

function setLanguage(lang) {
    const textContent = {
        th: {
            mainTitle: "ยินดีต้อนรับสู่",
            subTitle: "หน้าขอหนังสือของมหาวิทยาลัยเทคโนโลยีพระจอมเกล้าธนบุรี",
            message1: "ในหน้าต่างนี้จะเป็นการเข้าสู่ระบบเพื่อใช้ในการขอหนังสือให้แก่ผู้ใช้งาน",
            message2: "คุณสามารถเข้าสู่ระบบผ่าน Microsoft ได้ใต้ข้อความนี้",
            loginTitle: "เข้าสู่ระบบ",
            microsoftLoginText: "เข้าสู่ระบบด้วย Microsoft"
        },
        en: {
            mainTitle: "Welcome to",
            subTitle: "KMUTT Book Request System",
            message1: "This window will be used to log in to request books for users.",
            message2: "You can log in via Microsoft below.",
            loginTitle: "Login",
            microsoftLoginText: "Login with Microsoft"
        }
    };

    const elements = {
        mainTitle: document.getElementById('main-title'),
        subTitle: document.getElementById('sub-title'),
        message1: document.getElementById('message-1'),
        message2: document.getElementById('message-2'),
        loginTitle: document.getElementById('login-title'),
        microsoftLoginText: document.getElementById('microsoft-login-text')
    };

    Object.keys(elements).forEach(key => {
        if (elements[key]) {
            elements[key].textContent = textContent[lang][key];
        }
    });
}

// On page load
document.addEventListener('DOMContentLoaded', async () => {
    initializeThemeSwitch();
    initializeLanguageSwitch();
    await initializeLiff();
});
