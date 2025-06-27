let selectedBooks = new Set();
let expandedBooks = new Set();

function saveExpandedState() {
    localStorage.setItem('expandedBooks', JSON.stringify(Array.from(expandedBooks)));
}

function loadExpandedState() {
    try {
        const savedState = localStorage.getItem('expandedBooks');
        if (savedState) {
            expandedBooks = new Set(JSON.parse(savedState));
        }
    } catch (error) {
        console.error('Error loading expanded state:', error);
        expandedBooks = new Set();
    }
}

async function loadBookData() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const userId = urlParams.get('userId');
        if (!userId) throw new Error('User ID is required');

        document.getElementById('bookList').innerHTML = '<p>Loading books...</p>';
        loadExpandedState();

        const response = await fetch(`/api/recommended-books/${userId}`);
        const books = await response.json();

        const bookList = document.getElementById('bookList');
        if (books.length === 0) {
            bookList.innerHTML = `
                <div class="no-books-message">
                    <h2>No books available at the moment</h2>
                    <p>Please check back later</p>
                </div>
            `;
        } else {
            bookList.innerHTML = books.map((book, index) => {
                const isExpanded = expandedBooks.has(index.toString());
                return `
                <div class="book-item ${isExpanded ? 'expanded' : ''}" id="book-${index}">
                    <input type="checkbox" class="book-checkbox" data-query-id="${book.query_id}" data-title="${book.title}">
                    <img src="${book.coverImage}" alt="Book cover" class="book-cover">
                    <div class="book-info">
                        <h3>${book.title}</h3>
                        <p class="author">${book.author}</p>
                        <p class="description">${book.description}</p>
                        <div class="expand-btn" data-index="${index}">
                            ${isExpanded ? 'แสดงน้อยลง ▲' : 'แสดงเพิ่มเติม ▼'}
                        </div>
                    </div>
                </div>
                `;
            }).join('');

            document.querySelectorAll('.book-checkbox').forEach(checkbox => {
                checkbox.addEventListener('change', function () {
                    toggleBook(this.dataset.queryId, this.dataset.title);
                });
            });

            document.querySelectorAll('.expand-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const index = this.dataset.index;
                    const bookItem = document.getElementById(`book-${index}`);
                    const isExpanded = bookItem.classList.toggle('expanded');

                    if (isExpanded) {
                        this.textContent = 'แสดงน้อยลง ▲';
                        expandedBooks.add(index.toString());
                    } else {
                        this.textContent = 'แสดงเพิ่มเติม ▼';
                        expandedBooks.delete(index.toString());
                    }
                    saveExpandedState();
                });
            });
        }
    } catch (error) {
        console.error('Error loading book data:', error);
        document.getElementById('bookList').innerHTML = '<p>Error loading books.</p>';
    }
}

function toggleBook(queryId, title) {
    const key = `${queryId}|${title}`;
    if (selectedBooks.has(key)) {
        selectedBooks.delete(key);
    } else {
        selectedBooks.add(key);
    }
}

async function confirmPurchase() {
    if (selectedBooks.size === 0) {
        document.getElementById("warningPopup").style.display = "flex";
        return;
    }
    document.getElementById("confirmPopup").style.display = "flex";

    const confirmBtn = document.getElementById("popupConfirmBtn");
    const newConfirmBtn = confirmBtn.cloneNode(true);
    confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);

    newConfirmBtn.addEventListener("click", async () => {
        document.getElementById("confirmPopup").style.display = "none";

        try {
            const urlParams = new URLSearchParams(window.location.search);
            const userId = urlParams.get('userId');
            if (!userId) throw new Error('User ID is required');

            const queryIds = Array.from(selectedBooks).map(key => {
                const [query_id, title] = key.split('|');
                return { query_id, title };
            });

            const response = await fetch('/api/purchase', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ queryIds, userId })
            });

            if (response.ok) {
                document.getElementById("successPopup").style.display = "flex";
                selectedBooks.clear();
                document.querySelectorAll('.book-checkbox').forEach(checkbox => {
                    checkbox.checked = false;
                });
            } else {
                const errorData = await response.json();
                alert(`เกิดข้อผิดพลาด: ${errorData.error || 'กรุณาลองใหม่อีกครั้ง'}`);
            }
        } catch (error) {
            console.error('Error confirming purchase:', error);
            alert('เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
        }
    });
}

function initializeThemeSwitch() {
    const themeSwitch = document.getElementById('theme-switch');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.body.setAttribute('data-theme', savedTheme);
        themeSwitch.checked = savedTheme === 'dark';
    }

    themeSwitch.addEventListener('click', function() {
        const theme = this.checked ? 'dark' : 'light';
        document.body.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
    });
}

function setLanguage(lang) {
    const textContent = {
        th: {
            confirmBtn: "ยืนยันการขอหนังสือ",
            cancelBtn: "ลบรายการหนังสือทั้งหมด",
            logoutBtn: "ออกจากระบบ",
            popupConfirm: "คุณแน่ใจหรือไม่ว่าต้องการยืนยันการขอหนังสือ?",
            popupWarning: "กรุณาเลือกหนังสือก่อนทำการขอ!",
            popupOk: "ตกลง",
            popupCancelBtn: "ยกเลิก",
            popupConfirmBtn: "ยืนยัน",
            popupSuccessText: "คุณทำรายการสำเร็จแล้ว",
            popupSuccessOkBtn: "ตกลง",
            noBooksTitle: "ไม่มีหนังสือให้เลือกในขณะนี้",
            noBooksMessage: "กรุณาตรวจสอบภายหลัง",
            expandBtn: "แสดงเพิ่มเติม ▼",
            collapseBtn: "แสดงน้อยลง ▲"
        },
        en: {
            confirmBtn: "Confirm request",
            cancelBtn: "Delete all book items",
            logoutBtn: "Logout",
            popupConfirm: "Are you sure you want to confirm your book request?",
            popupWarning: "Please select a book before proceeding!",
            popupOk: "OK",
            popupCancelBtn: "Cancel",
            popupConfirmBtn: "Confirm",
            popupSuccessText: "You have successfully completed the transaction.",
            popupSuccessOkBtn: "OK",
            noBooksTitle: "No books available at the moment",
            noBooksMessage: "Please check back later",
            expandBtn: "Show more ▼",
            collapseBtn: "Show less ▲"
        }
    };

    document.getElementById('confirmBtn').textContent = textContent[lang].confirmBtn;
    document.getElementById('cancelBtn').textContent = textContent[lang].cancelBtn;
    document.getElementById('logoutBtn').textContent = textContent[lang].logoutBtn;
    document.getElementById('popupConfirmText').textContent = textContent[lang].popupConfirm;
    document.getElementById('popupWarningText').textContent = textContent[lang].popupWarning;
    document.getElementById('popupOkBtn').textContent = textContent[lang].popupOk;
    document.getElementById('popupCancelBtn').textContent = textContent[lang].popupCancelBtn;
    document.getElementById('popupConfirmBtn').textContent = textContent[lang].popupConfirmBtn;
    document.getElementById('popupSuccessText').textContent = textContent[lang].popupSuccessText;
    document.getElementById('popupSuccessOkBtn').textContent = textContent[lang].popupSuccessOkBtn;

    document.querySelectorAll('.expand-btn').forEach(btn => {
        const index = btn.dataset.index;
        const bookItem = document.getElementById(`book-${index}`);
        if (bookItem && bookItem.classList.contains('expanded')) {
            btn.textContent = textContent[lang].collapseBtn;
        } else {
            btn.textContent = textContent[lang].expandBtn;
        }
    });

    const noBooksTitle = document.querySelector('.no-books-message h2');
    const noBooksMessage = document.querySelector('.no-books-message p');
    if (noBooksTitle && noBooksMessage) {
        noBooksTitle.textContent = textContent[lang].noBooksTitle;
        noBooksMessage.textContent = textContent[lang].noBooksMessage;
    }
}

function initializeLanguageSwitch() {
    const langButtons = document.querySelectorAll('.lang-btn');
    const savedLang = localStorage.getItem('language') || 'th';
    setLanguage(savedLang);

    langButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === savedLang);
        btn.addEventListener('click', () => {
            const lang = btn.dataset.lang;
            langButtons.forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
            setLanguage(lang);
            localStorage.setItem('language', lang);
        });
    });
}

function toggleBook(queryId, title) {
    const key = `${queryId}|${title}`;
    if (selectedBooks.has(key)) {
        selectedBooks.delete(key);
    } else {
        selectedBooks.add(key);
    }
}

async function confirmPurchase() {
    if (selectedBooks.size === 0) {
        document.getElementById("warningPopup").style.display = "flex";
        return;
    }
    document.getElementById("confirmPopup").style.display = "flex";

    document.getElementById("popupConfirmBtn").addEventListener("click", async () => {
        document.getElementById("confirmPopup").style.display = "none";

        try {
            const urlParams = new URLSearchParams(window.location.search);
            const userId = urlParams.get('userId');
            if (!userId) throw new Error('User ID is required');

            const queryIds = Array.from(selectedBooks).map(key => {
                const [query_id, title] = key.split('|');
                return { query_id, title };
            });

            const response = await fetch('/api/purchase', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ queryIds, userId })
            });

            if (response.ok) {
                document.getElementById("successPopup").style.display = "flex";
                selectedBooks.clear();
                document.querySelectorAll('.book-checkbox').forEach(checkbox => {
                    checkbox.checked = false;
                });
            } else {
                const errorData = await response.json();
                alert(`เกิดข้อผิดพลาด: ${errorData.error || 'กรุณาลองใหม่อีกครั้ง'}`);
            }
        } catch (error) {
            console.error('Error confirming purchase:', error);
            alert('เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง');
        }
    }, { once: true });
}

async function clearRecommendations() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const userId = urlParams.get('userId');
        if (!userId) throw new Error('User ID is required');

        const response = await fetch('/api/cancel-recommendations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error(`Failed to clear recommendations: ${errorData.error}`);
        }
    } catch (error) {
        console.error('Error clearing recommendations:', error);
    }
}

async function logout() {
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const userId = urlParams.get('userId');
        if (!userId) {
            console.error('User ID is missing');
            throw new Error('User ID is required');
        }

        console.log(`Initiating logout for user ${userId}`);

        // เคลียร์คำแนะนำก่อน logout
        await clearRecommendations();

        // เรียก API เพื่อลบเซสชัน
        console.log('Calling /api/logout');
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userId })
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error(`Logout API failed: ${errorData.error}`);
            throw new Error(errorData.error || 'การ logout ล้มเหลว');
        }

        console.log('Logout API call successful');

        // เคลียร์ local storage (ยกเว้น theme และ language)
        localStorage.removeItem('expandedBooks');
        selectedBooks.clear();
        expandedBooks.clear();

        // ทำการ logout จาก LIFF และ redirect
        console.log('Checking LIFF environment');
        if (typeof liff !== 'undefined' && liff.isInClient()) {
            console.log('Logging out from LIFF');
            liff.logout();
        }

        console.log('Redirecting to /login.html?logout=true');
        window.location.href = '/login.html?logout=true';
    } catch (error) {
        console.error('Error during logout:', error.message, error.stack);
        // ลบ alert เพื่อป้องกัน popup ที่ไม่จำเป็น
        // alert('เกิดข้อผิดพลาดในการออกจากระบบ กรุณาลองใหม่อีกครั้ง');
        // Redirect แม้ว่าจะเกิดข้อผิดพลาด
        console.log('Fallback: Redirecting to /login.html?logout=true');
        window.location.href = '/login.html?logout=true';
    }
}

function closeSuccessPopup() {
    document.getElementById("successPopup").style.display = "none";
    if (typeof liff !== 'undefined' && liff.isInClient()) {
        liff.closeWindow();
    } else {
        alert('This would close the LIFF app in a real environment');
    }
}

// function showToast(message, duration = 3000) {
//     const toast = document.getElementById('toast');
//     const msg = document.getElementById('toast-message');
//     msg.textContent = message;
//     toast.style.display = 'block';
  
//     setTimeout(() => {
//       toast.style.display = 'none';
//     }, duration);
//   }

document.addEventListener('DOMContentLoaded', () => {
    initializeThemeSwitch();
    initializeLanguageSwitch();
    //initializeLiffWithRetry();
    loadBookData();

    document.getElementById('confirmBtn').addEventListener('click', confirmPurchase);
    document.getElementById('cancelBtn').addEventListener('click', async () => {
        await clearRecommendations();
        if (typeof liff !== 'undefined' && liff.isInClient()) {
            liff.closeWindow();
        } else {
            window.location.reload();
        }
    });

    document.getElementById('logoutBtn').addEventListener('click', logout);

    if (typeof liff !== 'undefined' && liff.isInClient()) {
        window.addEventListener('beforeunload', async () => {
            if (selectedBooks.size === 0) {
                await clearRecommendations();
            }
        });
    }

    document.getElementById('popupOkBtn').addEventListener('click', () => {
        document.getElementById('warningPopup').style.display = 'none';
    });
    document.getElementById('popupCancelBtn').addEventListener('click', () => {
        document.getElementById('confirmPopup').style.display = 'none';
    });
    document.getElementById('popupSuccessOkBtn').addEventListener('click', closeSuccessPopup);
});