import streamlit as st
import json
import os

# --- 1. إعدادات الصفحة والتجاوب مع الموبايل ---
st.set_page_config(
    page_title="🎈 صاحبك خصمك",
    page_icon="🍿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# تحسين مظهر الواجهة والأزرار لتناسب اللمس على الشاشات الذكية والموبايل
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    .stButton > button {
        width: 100% !important;
        padding: 12px !important;
        font-size: 20px !important;
        border-radius: 10px !important;
    }
    .main-title {
        text-align: center;
        color: #FF4B4B;
        font-size: 32px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات المحلية (JSON Database) ---
DB_FILE = "users_data.json"

def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

users_db = load_data()

# --- 3. إدارة جلسة المستخدم (Session State) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- 4. شاشة تسجيل الدخول / إنشاء حساب جديد ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-title'>🍿 أهلاً بك في صاحبك خصمك</h1>", unsafe_allow_html=True)
    st.write("---")
    
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 حساب جديد"])

    # تبويب تسجيل الدخول
    with tab1:
        st.subheader("تسجيل الدخول")
        login_user = st.text_input("اسم المستخدم", key="login_u")
        login_pass = st.text_input("كلمة السر", type="password", key="login_p")
        
        if st.button("دخول 🚀"):
            login_user_clean = login_user.strip()
            if login_user_clean in users_db and users_db[login_user_clean]["password"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user_clean
                st.success(f"مرحباً بك مجدداً يا {login_user_clean}! 👋")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة السر غير صحيحة!")

    # تبويب إنشاء حساب جديد
    with tab2:
        st.subheader("إنشاء حساب جديد")
        new_user = st.text_input("اختر اسم مستخدم", key="new_u")
        new_pass = st.text_input("اختر كلمة سر", type="password", key="new_p")
        
        if st.button("إنشاء الحساب ✨"):
            new_user_clean = new_user.strip()
            if not new_user_clean or not new_pass.strip():
                st.warning("برجاء إدخال اسم المستخدم وكلمة السر!")
            elif new_user_clean in users_db:
                st.warning("اسم المستخدم هذا مستخدم بالفعل، اختر اسماً آخر.")
            else:
                users_db[new_user_clean] = {
                    "password": new_pass,
                    "score": 0,
                    "games_played": 0
                }
                save_data(users_db)
                st.success("تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.")

# --- 5. واجهة اللعبة الرئيسية بعد تسجيل الدخول ---
else:
    username = st.session_state.username
    user_data = users_db.get(username, {"score": 0, "games_played": 0})

    # الشريط العلوي مع زر الخروج
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"👤 اللاعب: **{username}** | 🏆 النقاط: **{user_data.get('score', 0)}**")
    with col2:
        if st.button("خروج 🚪"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    st.write("---")
    st.markdown("<h2 style='text-align: center;'>🎯 ساحة اللعب</h2>", unsafe_allow_html=True)
    
    # عرض صور/خلفية اللعبة إذا كانت موجودة
    if os.path.exists("welcome_bg.jpg"):
        st.image("welcome_bg.jpg", use_container_width=True)

    st.info("اضغط على الزر بالأسفل لكسب النقاط وحفظ التقدم تلقائياً!")

    # أزرار التفاعل وحفظ التقدم
    if st.button("➕ زيادة نقطة وحفظ التقدم"):
        users_db[username]["score"] = users_db[username].get("score", 0) + 1
        users_db[username]["games_played"] = users_db[username].get("games_played", 0) + 1
        save_data(users_db)
        st.success("تم تسجيل النقطة وحفظ بياناتك بنجاح! 💾")
        st.rerun()