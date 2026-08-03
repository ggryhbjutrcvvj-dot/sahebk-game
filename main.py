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

# تحسين مظهر الواجهة والأزرار للموبايل
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
        font-size: 30px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات في الذاكرة الحية (Session Database) ---
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# --- 3. شاشة تسجيل الدخول / إنشاء حساب جديد ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-title'>🍿 أهلاً بك في صاحبك خصمك</h1>", unsafe_allow_html=True)
    st.write("---")
    
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 حساب جديد"])

    # تبويب تسجيل الدخول
    with tab1:
        st.subheader("تسجيل الدخول")
        login_user = st.text_input("اسم المستخدم", key="login_u").strip()
        login_pass = st.text_input("كلمة السر", type="password", key="login_p").strip()
        
        if st.button("دخول 🚀"):
            db = st.session_state.users_db
            if login_user in db and db[login_user]["password"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success(f"مرحباً بك يا {login_user}! جاري تحويلك...")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة السر غير صحيحة! (إذا كنت جديداً اضغط على إنشاء حساب)")

    # تبويب إنشاء حساب جديد
    with tab2:
        st.subheader("إنشاء حساب جديد")
        new_user = st.text_input("اختر اسم مستخدم", key="new_u").strip()
        new_pass = st.text_input("اختر كلمة سر", type="password", key="new_p").strip()
        
        if st.button("إنشاء الحساب ودخول ✨"):
            db = st.session_state.users_db
            if not new_user or not new_pass:
                st.warning("برجاء إدخال اسم المستخدم وكلمة السر!")
            elif new_user in db:
                st.warning("اسم المستخدم هذا مستخدم بالفعل، اختر اسماً آخر.")
            else:
                # إنشاء الحساب وتسجيل الدخول فوراً
                st.session_state.users_db[new_user] = {
                    "password": new_pass,
                    "score": 0
                }
                st.session_state.logged_in = True
                st.session_state.username = new_user
                st.success("تم إنشاء الحساب بنجاح! جاري الدخول للعبة...")
                st.rerun()

# --- 4. واجهة اللعبة الرئيسية بعد تسجيل الدخول ---
else:
    username = st.session_state.username
    user_data = st.session_state.users_db.get(username, {"score": 0})

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
    
    # عرض صورة اللعبة إذا كانت موجودة
    if os.path.exists("welcome_bg.jpg.jpeg"):
        st.image("welcome_bg.jpg.jpeg", use_container_width=True)
    elif os.path.exists("welcome_bg.jpg"):
        st.image("welcome_bg.jpg", use_container_width=True)

    st.success("تم تسجيل دخولك بنجاح! أنت الآن داخل اللعبة 🥳")

    # أزرار التفاعل وحفظ النقاط
    if st.button("➕ زيادة نقطة ⭐"):
        st.session_state.users_db[username]["score"] += 1
        st.success("مبروك! زادت نقاطك 1 +")
        st.rerun()