import streamlit as st
import json
import os
import random

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
        font-size: 18px !important;
        border-radius: 12px !important;
        margin-top: 5px;
    }
    .main-title {
        text-align: center;
        color: #FF4B4B;
        font-size: 28px;
        font-weight: bold;
    }
    .card {
        background-color: #262730;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #FF4B4B;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة قاعدة البيانات والجلسة ---
if "users_db" not in st.session_state:
    st.session_state.users_db = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# بنك الأسئلة والتحديات التفاعلية للعبة
QUESTIONS_BANK = [
    {"q": "سؤال سرعة: مين فيكم يقدر يوقع التاني في الكلام الأول؟ 🤫", "type": "challenge", "pts": 10},
    {"q": "لو صاحبك طلب منك تدي له كل فلوسك عشان يشتري حاجة تافهة.. هتوافق؟", "options": ["أكيد، صاحب عمري", "مستحيل، أنا مش بوزع فلوس", "على حسب هو مين فيهم"], "pts": 5},
    {"q": "تحدي: اتصل بصاحبك المفضل ودلوقتي وقوله 'أنا في القسم ومحتاجك' وشوف رد فعله! 📞😂", "type": "challenge", "pts": 15},
    {"q": "مين فيكم الأكتر توقعاً إنه يتأخر عن أي ميعاد؟ ⏰", "options": ["أنا طبعاً", "صاحبي الخصم", "إحنا الاتنين بنتأخر"], "pts": 5},
    {"q": "سؤال صراحة: لو جالك سفرية ببلاش لشخص واحد بس.. هتاخد صاحبك معاك ولا تروح لوحدك؟ ✈️", "options": ["هاخده معايا أكيد", "هسافر لوحدي والاستجمام أهم", "هبيع التذكرة ونقسم الفلوس"], "pts": 10},
]

# --- 3. شاشة تسجيل الدخول / إنشاء حساب جديد ---
if not st.session_state.logged_in:
    st.markdown("<h1 class='main-title'>🍿 أهلاً بك في صاحبك خصمك</h1>", unsafe_allow_html=True)
    st.write("---")
    
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 حساب جديد"])

    with tab1:
        st.subheader("تسجيل الدخول")
        login_user = st.text_input("اسم المستخدم", key="login_u").strip()
        login_pass = st.text_input("كلمة السر", type="password", key="login_p").strip()
        
        if st.button("دخول للعبة 🚀"):
            db = st.session_state.users_db
            if login_user in db and db[login_user]["password"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success(f"مرحباً بك يا {login_user}!")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة السر غير صحيحة!")

    with tab2:
        st.subheader("إنشاء حساب جديد")
        new_user = st.text_input("اختر اسم مستخدم", key="new_u").strip()
        new_pass = st.text_input("اختر كلمة سر", type="password", key="new_p").strip()
        
        if st.button("إنشاء الحساب ودخول ✨"):
            db = st.session_state.users_db
            if not new_user or not new_pass:
                st.warning("برجاء إدخال اسم المستخدم وكلمة السر!")
            elif new_user in db:
                st.warning("اسم المستخدم هذا مستخدم بالفعل!")
            else:
                st.session_state.users_db[new_user] = {"password": new_pass, "score": 0}
                st.session_state.logged_in = True
                st.session_state.username = new_user
                st.success("تم إنشاء الحساب بنجاح!")
                st.rerun()

# --- 4. واجهة اللعبة الرئيسية (صاحبك خصمك) ---
else:
    username = st.session_state.username
    user_score = st.session_state.users_db[username].get("score", 0)

    # الشريط العلوي
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"👤 اللاعب: **{username}** | 🏆 نقاطك: **{user_score}**")
    with col2:
        if st.button("خروج 🚪"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    st.write("---")
    st.markdown("<h2 class='main-title'>🔥 ساحة اللعب: صاحبك خصمك 🔥</h2>", unsafe_allow_html=True)

    # متغيرات الجولة الحالية
    if "current_q" not in st.session_state:
        st.session_state.current_q = random.choice(QUESTIONS_BANK)

    q_data = st.session_state.current_q

    # عرض بطاقة السؤال/التحدي
    st.markdown(f"""
        <div class="card">
            <h3>🎯 الجولة الحالية</h3>
            <p style="font-size: 22px; font-weight: bold;">{q_data['q']}</p>
            <p style="color: #FFD700;">جائزة الجولة: +{q_data['pts']} نقاط</p>
        </div>
    """, unsafe_allow_html=True)

    # إذا كان السؤال يحتوي على خيارات
    if "options" in q_data:
        selected_option = st.radio("اختر إجابتك:", q_data["options"])
        if st.button("إرسال الإجابة وحسب النقاط 🎯"):
            st.session_state.users_db[username]["score"] += q_data["pts"]
            st.success(f"إجابة قوية! كسبت {q_data['pts']} نقاط 🥳")
            # اختيار سؤال جديد للجولة الجاية
            st.session_state.current_q = random.choice(QUESTIONS_BANK)
            st.rerun()

    # إذا كان تحدي مادي/عملي
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("نفذت التحدي بنجاح 💪"):
                st.session_state.users_db[username]["score"] += q_data["pts"]
                st.success(f"عاش يا بطل! كسبت {q_data['pts']} نقاط 🔥")
                st.session_state.current_q = random.choice(QUESTIONS_BANK)
                st.rerun()
        with col_b:
            if st.button("استسلمت / انسحبت ❌"):
                st.warning("ولا يهمك، الجولة الجاية تعوض!")
                st.session_state.current_q = random.choice(QUESTIONS_BANK)
                st.rerun()

    st.write("---")
    if st.button("🔄 تغيير السؤال / تحدي آخر"):
        st.session_state.current_q = random.choice(QUESTIONS_BANK)
        st.rerun()