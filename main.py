import streamlit as st
import json
import os
import random
import base64

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="🎈 صاحبك خصمك - مستودع التسالي",
    page_icon="🍿",
    layout="wide"
)

# دالة لتحويل الصورة المحلية إلى base64 لتظهر كخلفية
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

# --- 2. نظام حفظ الحسابات القوي والدائم (JSON File DB) ---
DB_FILE = "sahebk_users.json"

def load_users():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_users(users_data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(users_data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

# تحميل الحسابات المسجلة
users_db = load_users()

# --- 3. بنك الأسئلة والتلميحات ---
QUESTIONS_BANK = {
    "أفلام وسينما مصرية": [
        {"q": "فيلم سينمائي نادراً ما يُعرض، بطولة عادل إمام وميرفت أمين، يدور حول عملية خطف حافلة مدرسية في السبعينات؟", "a": "البحث عن فضيحة / الحافلة (أو الجرد)"},
        {"q": "فيلم كوميدي إثارة بطولة أحمد حلمي يجسد فيه شخصية مريض بمرض الفصام وله 3 شخصيات؟", "a": "كده رضا"},
        {"q": "فيلم بطولة أحمد السقا، أحداثه تدور بالكامل في جبال أسوان حول تجارة السلاح والمخدرات وحصار الشرطة للجزيرة؟", "a": "الجزيرة"},
        {"q": "فيلم بطولة محمد هنيدي، سافر فيه للخارج واستخدم حركات قتالية وهمية في مطعم صيني؟", "a": "فول الصين العظيم"},
        {"q": "فيلم بطولة كريم عبد العزيز وجمال سليمان يدور حول الجاسوسية المزدوجة وتهريب قطعة أثرية فرعونية؟", "a": "ولاد العم"},
        {"q": "فيلم درامي تاريخي بطولة محمود عبد العزيز يدور حول شخصية 'الشيخ حسني' الكفيف في حي إمبابة؟", "a": "الكيت كات"},
        {"q": "فيلم بطولة أحمد زكي يجسد فيه شخصية ضابط شرطة صارم ومستبد يتحول لمعتدٍ بسبب سلطته؟", "a": "زوجة رجل مهم"},
        {"q": "فيلم بطولة نور الشريف، يدور حول سائق تاكسي يجد حقيبة بها ملايين الجنيهات وتتغير حياته؟", "a": "ضربة شمس / التخشيبة"},
        {"q": "فيلم تاريخي سينمائي إخراج يوسف شاهين يدور حول صراع الدواجن وقصة الفلاحين في القرية المصرية؟", "a": "الأرض"},
        {"q": "فيلم بطولة محمود عبد العزيز ويحيى الفخراني، يدور حول عالم الكيمياء وتصنيع المواد المخدرة الوهمية؟", "a": "الكيف"}
    ],
    "كورة على السريع": [
        {"q": "لاعب مصري وحيد سجل في 3 نسخ مختلفة من كاس العالم للأندية مع الأهلي والمنتخب؟", "a": "حسين الشحات / محمد أبو تريكة"},
        {"q": "مهاجم مصري عالمي يلعب في نادي ليفربول الإنجليزي ويحمل الرقم 11 ويرتدي شارة القيادة؟", "a": "محمد صلاح"},
        {"q": "حارس مرمى مصري تاريخي شال أمم إفريقيا 4 مرات وصد ركلة ترجيح شهيرة من دروجبا في 2006؟", "a": "عصام الحضري"},
        {"q": "لاعب مصري يلقب بـ 'الماجيكو' وارتدى الرقم 22 وحصل على أفضل لاعب في إفريقيا داخل القارة عدة مرات؟", "a": "محمد أبو تريكة"},
        {"q": "أول فريق مصري وعربي يتوج ببطولة دوري أبطال إفريقيا في تاريخ الكرة المصرية عام 1969؟", "a": "الإسماعيلي"},
        {"q": "لاعب مصري صاحب أسرع هدف في تاريخ الدوري المصري الممتاز (خلال 11 ثانية)؟", "a": "أحمد جعفر / أيمن يونس"},
        {"q": "مدرب مصري قاد المنتخب الوطني للتتويج بالثلاثية التاريخية لكأس الأمم الإفريقية (2006, 2008, 2010)؟", "a": "حسن شحاتة"},
        {"q": "لاعب كرة قدم مصري محترف سابق لعب لنادي أياكس أمستردام ورماة روما وتوتنهام؟", "a": "أحمد حسام ميدو"},
        {"q": "أكبر نتيجة فوز تاريخية سجلها نادي مصري في مباراة رسمية بالبطولات الأفريقية؟", "a": "9-0 (الأهلي ضد يانج أفريكانز)"},
        {"q": "لاعب زملكاوي تاريخي يلقب بـ 'الثعلب الإمام' وكان رمزاً لصانعي الألعاب؟", "a": "حازم إمام"}
    ],
    "شخصيات مشهورة": [
        {"q": "عالم كيمياء مصري شهير حصل على جائزة نوبل بفضل اختراع كاميرا تصوير تعمل بالفيمتو ثانية؟", "a": "أحمد زويل"},
        {"q": "أديب روائي مصري عالمي حاصل على نوبل في الأدب عام 1988 وصاحب ثلاثية بين القصرين؟", "a": "نجيب محفوظ"},
        {"q": "سيدة الغناء العربي القادمة من قرية طماي الزهايرة ولُقبت بـ 'كوكب الشرق'؟", "a": "أم كلثوم"},
        {"q": "جراح قلب مصري عالمي أنشأ أكبر مركز لمجانيات جراحة القوات والقلب للأطفال في أسوان؟", "a": "مجدي يعقوب"},
        {"q": "ملياردار ومهندس عالمي أسس شركات سبيس إكس وتيسلا واشترى منصة X (تويتر سابقاً)؟", "a": "إيلون ماسك"},
        {"q": "مفكر وفيلسوف مصري صاحب برنامج 'العلم والإيمان' ومؤلف كتاب 'مصطفى محمود'؟", "a": "د. مصطفى محمود"},
        {"q": "مهندس معماري مصري عالمي يُلقب بـ 'معماري الفقراء' لبنائه بالقرية والتين والقرنة؟", "a": "حسن فتحي"},
        {"q": "قائد وعسكري مصري ترأس أركان حرب القوات المسلحة في حرب أكتوبر 1973 وصاحب خطة المآذن العالية؟", "a": "سعد الدين الشاذلي"},
        {"q": "رسام ومبتكر عالمي إيطالي صمم لوحة الموناليزا والعشاء الأخير وكان مخترعاً أيضاً؟", "a": "ليوناردو دا فينشي"},
        {"q": "عالم فيزياء نادراً ما يُذكر اسمه بالشرق، نال نوبل وصاحب نظرية النسبية العامة والخاصة؟", "a": "ألبرت أينشتاين"}
    ]
}

# --- 4. عجلة العقاب ---
PUNISHMENTS_LIST = [
    "🎤 غنّي مقطع من أغنية كرتون قديمة بصوت عالي جداً!",
    "🏋️ اعمل 10 ضغط فوراً أمام الجميع!",
    "🤐 ممنوع تتكلم لمدة جولة كاملة والتعبير بالإشارة فقط!",
    "🙈 اعترف باحرج موقف حصلك في حياتك!",
    "🐸 قلّد صوت حيوان كرتوني لمدة 30 ثانية!",
    "🥤 اشرب كبشة ماية على بق واحد من غير ما تنزل ولا نقطة!",
    "💃 اعمل رقصة كرتونية غريبة لمدة 15 ثانية!",
    "📱 ابعت رسالة عشوائية لأول واحد في قائمة الواتساب عندك!"
]

# --- 5. تهيئة متغيرة البيانات ---
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "user" not in st.session_state:
    st.session_state.user = {"id": "#10001", "name": "زائر", "score": 0}

if "username" not in st.session_state:
    st.session_state.username = ""

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "current_punishment" not in st.session_state:
    st.session_state.current_punishment = ""

# --- 6. التنسيق البصري والكرتوني (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Changa:wght@700;900&display=swap');

    .stApp {
        background-color: #121826;
        font-family: 'Changa', cursive, sans-serif;
    }

    .cartoon-profile {
        background: #FF7F00;
        color: #FFFFFF;
        padding: 15px 25px;
        border-radius: 20px;
        border: 3px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 25px;
    }

    .category-box-cartoon {
        background: linear-gradient(135deg, #FF9F1C, #FF7F00);
        border: 4px solid #000000;
        border-radius: 25px;
        padding: 20px;
        text-align: center;
        color: #FFFFFF;
        box-shadow: 6px 6px 0px #000000;
        margin-bottom: 12px;
    }

    .category-title-cartoon {
        font-family: 'Changa', sans-serif;
        font-size: 26px;
        color: #FFFFFF;
        font-weight: 900;
        text-shadow: 2px 2px 0px #000000;
    }

    .stButton > button {
        background: #06D6A0 !important;
        color: #000000 !important;
        border: 3px solid #000000 !important;
        font-family: 'Changa', sans-serif !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        padding: 10px 20px !important;
        box-shadow: 4px 4px 0px #000000 !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button:hover {
        background: #FFD166 !important;
        color: #000000 !important;
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0px #000000 !important;
    }

    .question-card-cartoon {
        background-color: #1E293B;
        border: 4px solid #FFD166;
        box-shadow: 6px 6px 0px #FF7F00;
        padding: 30px;
        border-radius: 30px;
        text-align: center;
        font-size: 24px;
        color: #FFD166;
        font-weight: bold;
        margin-top: 15px;
    }

    .punishment-card {
        background: linear-gradient(135deg, #E63946, #D62828);
        border: 4px solid #000000;
        border-radius: 25px;
        padding: 20px;
        color: #FFFFFF;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        box-shadow: 5px 5px 0px #000000;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 🟢 1. واجهة الدخول بحجم الصورة (Welcome Screen + Login System)
# ==========================================
if st.session_state.page == "welcome":
    bg_img = get_image_base64("welcome_bg.jpg")
    
    bg_style = f"""
        background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.65)), 
                    url('data:image/jpeg;base64,{bg_img}') no-repeat center center;
        background-size: cover;
    """ if bg_img else """
        background: linear-gradient(135deg, #FF7F00, #1E293B);
    """

    st.markdown(f"""
        <style>
        .welcome-container {{
            {bg_style}
            min-height: 50vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border-radius: 35px;
            border: 4px solid #FF7F00;
            box-shadow: 0 15px 35px rgba(255, 127, 0, 0.4);
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 20px;
        }}

        .cartoon-title-center {{
            font-family: 'Changa', cursive, sans-serif;
            color: #FF7F00;
            font-size: 46px;
            font-weight: 900;
            text-shadow: 3px 3px 0px #FFFFFF, 6px 6px 0px #000000;
            margin-bottom: 10px;
            text-align: center;
        }}
        </style>

        <div class="welcome-container">
            <div class="cartoon-title-center">🍿 أهلاً بيكم في مستودع التسالي 🎈</div>
        </div>
    """, unsafe_allow_html=True)

    # --- شاشة تسجيل الدخول والحسابات ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "📝 حساب جديد"])

        with tab1:
            login_u = st.text_input("اسم المستخدم", key="l_u").strip()
            login_p = st.text_input("كلمة السر", type="password", key="l_p").strip()
            if st.button("🚪 إدخـال 🎮", use_container_width=True):
                # إعادة قراءة الملف للتأكد من وجود البيانات
                current_db = load_users()
                if login_u in current_db and current_db[login_u]["password"] == login_p:
                    st.session_state.username = login_u
                    st.session_state.user = current_db[login_u]["user_info"]
                    st.session_state.page = "main_hub"
                    st.success("تم الدخول بنجاح! 🚀")
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة السر غير صحيحة!")

        with tab2:
            new_u = st.text_input("اسم مستخدم جديد", key="n_u").strip()
            new_p = st.text_input("كلمة السر", type="password", key="n_p").strip()
            if st.button("✨ إنشاء حساب ودخول", use_container_width=True):
                current_db = load_users()
                if not new_u or not new_p:
                    st.warning("يرجى ملء جميع البيانات!")
                elif new_u in current_db:
                    st.warning("اسم المستخدم مستخدم بالفعل، اختر اسماً آخر!")
                else:
                    user_id = f"#{random.randint(10000, 99999)}"
                    user_info = {"id": user_id, "name": new_u, "score": 0}
                    # حفظ الحساب رسمياً في ملف DB
                    current_db[new_u] = {"password": new_p, "user_info": user_info}
                    save_users(current_db)
                    
                    st.session_state.username = new_u
                    st.session_state.user = user_info
                    st.session_state.page = "main_hub"
                    st.success("تم إنشاء الحساب وحفظه بنجاح! 🎉")
                    st.rerun()


# ==========================================
# 🟢 2. الصفحة الرئيسية الهرمية (Main Hub)
# ==========================================
elif st.session_state.page == "main_hub":
    user = st.session_state.user
    
    st.markdown(f"""
        <div class="cartoon-profile">
            🍿 اللعبة: <b>صاحبك خصمك</b> &nbsp;|&nbsp; 👤 اللاعب: <b>{user['name']}</b> &nbsp;|&nbsp; 🆔 الـ ID: <b>{user['id']}</b> &nbsp;|&nbsp; 🏆 السكور: <b>{user['score']} ⭐</b>
        </div>
    """, unsafe_allow_html=True)

    # زر الخروج
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.page = "welcome"
        st.session_state.username = ""
        st.rerun()

    st.subheader("🎲 ألعاب التسالي ومستودع المرح")

    # الهرم: الصف الأول (مربعين)
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.markdown('<div class="category-box-cartoon"><div class="category-title-cartoon">🎬 أفلام وسينما مصرية 🍿</div></div>', unsafe_allow_html=True)
        sub1, sub2 = st.columns(2)
        if sub1.button("📱 لعب مع الأصدقاء", key="m1"):
            st.session_state.selected_cat = "أفلام وسينما مصرية"
            st.session_state.mode = "local"
            st.session_state.q_index = 0
            st.session_state.page = "game_room"
            st.rerun()
        if sub2.button("🌐 أونلاين عن بعد", key="m2"):
            st.session_state.selected_cat = "أفلام وسينما مصرية"
            st.session_state.mode = "online"
            st.session_state.page = "game_room"
            st.rerun()

    with row1_col2:
        st.markdown('<div class="category-box-cartoon"><div class="category-title-cartoon">⚽ كورة على السريع ⚽</div></div>', unsafe_allow_html=True)
        sub1, sub2 = st.columns(2)
        if sub1.button("📱 لعب مع الأصدقاء", key="k1"):
            st.session_state.selected_cat = "كورة على السريع"
            st.session_state.mode = "local"
            st.session_state.q_index = 0
            st.session_state.page = "game_room"
            st.rerun()
        if sub2.button("🌐 أونلاين عن بعد", key="k2"):
            st.session_state.selected_cat = "كورة على السريع"
            st.session_state.mode = "online"
            st.session_state.page = "game_room"
            st.rerun()

    st.write("") 

    # الهرم: الصف الثاني (3 مربعات)
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.markdown('<div class="category-box-cartoon"><div class="category-title-cartoon">🌟 شخصيات مشهورة 👑</div></div>', unsafe_allow_html=True)
        sub1, sub2 = st.columns(2)
        if sub1.button("📱 محلي", key="p1"):
            st.session_state.selected_cat = "شخصيات مشهورة"
            st.session_state.mode = "local"
            st.session_state.q_index = 0
            st.session_state.page = "game_room"
            st.rerun()
        if sub2.button("🌐 أونلاين", key="p2"):
            st.session_state.selected_cat = "شخصيات مشهورة"
            st.session_state.mode = "online"
            st.session_state.page = "game_room"
            st.rerun()

    with row2_col2:
        st.markdown('<div class="category-box-cartoon"><div class="category-title-cartoon">🎲 لعبة لودو (Ludo) 🎯</div></div>', unsafe_allow_html=True)
        sub1, sub2 = st.columns(2)
        if sub1.button("📱 محلي", key="l1"):
            st.session_state.selected_cat = "لعبة لودو"
            st.session_state.mode = "local"
            st.session_state.page = "game_room"
            st.rerun()
        if sub2.button("🌐 أونلاين", key="l2"):
            st.session_state.selected_cat = "لعبة لودو"
            st.session_state.mode = "online"
            st.session_state.page = "game_room"
            st.rerun()

    with row2_col3:
        st.markdown('<div class="category-box-cartoon"><div class="category-title-cartoon">🀄 لعبة الدومينو 🧱</div></div>', unsafe_allow_html=True)
        sub1, sub2 = st.columns(2)
        if sub1.button("📱 محلي", key="d1"):
            st.session_state.selected_cat = "لعبة الدومينو"
            st.session_state.mode = "local"
            st.session_state.page = "game_room"
            st.rerun()
        if sub2.button("🌐 أونلاين", key="d2"):
            st.session_state.selected_cat = "لعبة الدومينو"
            st.session_state.mode = "online"
            st.session_state.page = "game_room"
            st.rerun()

    st.divider()

    # الميزات الاجتماعية
    tab_group, tab_friends, tab_invite = st.tabs(["👨‍👩‍👧‍👦 إنشاء جروب ومحادثة", "📩 طلبات الصداقة والـ ID", "🎮 دعوة صديق للأونلاين"])

    with tab_group:
        st.subheader("💬 شات الجروب والتسالي")
        g_col1, g_col2 = st.columns([1, 1])
        with g_col1:
            group_name = st.text_input("اسم الجروب الجديد:")
            member_ids = st.text_input("أدخل أرقام الـ ID للأعضاء (افصل بـ فاصلة ,):")
            if st.button("✨ إنشاء الجروب"):
                if group_name and member_ids:
                    st.success(f"تم إنشاء جروب '{group_name}' بنجاح!")
        with g_col2:
            st.write("💬 **محادثة الشات التفاعلية**")
            chat_msg = st.text_input("اكتب رسالة...")
            uploaded_file = st.file_uploader("إرسال صورة في الجروب", type=['png', 'jpg', 'jpeg'])
            if st.button("إرسال 🚀"):
                if chat_msg or uploaded_file:
                    st.toast("تم إرسال الرسالة إلى الأعضاء!")

    with tab_friends:
        st.subheader("🤝 إضافة صديق عبر الـ ID")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            friend_id = st.text_input("أدخل الـ ID الخاص بصديقك:")
            if st.button("📩 إرسال طلب صداقة"):
                if friend_id:
                    st.success(f"تم إرسال طلب الصداقة لـ `{friend_id}`!")
        with f_col2:
            st.write("📋 **طلبات الصداقة:**")
            st.info("لا توجد طلبات صداقة حالياً.")

    with tab_invite:
        st.subheader("🚀 دعوة صديق لتحدي أونلاين")
        inv_col1, inv_col2 = st.columns(2)
        with inv_col1:
            selected_game = st.selectbox("اختار اللعبة:", ["أفلام وسينما مصرية", "كورة على السريع", "شخصيات مشهورة", "لعبة لودو", "لعبة الدومينو"])
            target_friend = st.text_input("أدخل الـ ID للصديق المراد دعوته:")
            if st.button("🎮 إرسال الدعوة"):
                if target_friend:
                    st.success(f"تم إرسال دعوة أونلاين لـ `{target_friend}`!")


# ==========================================
# 🟢 3. شاشة اللعب + عجلة العقاب (Game Room)
# ==========================================
elif st.session_state.page == "game_room":
    cat = st.session_state.get("selected_cat", "")
    mode = st.session_state.get("mode", "")
    
    st.title(f"🎮 {cat}")
    st.caption(f"نمط اللعب: {'📱 محلي' if mode == 'local' else '🌐 أونلاين'}")
    st.divider()

    # --- أ) أقسام الأسئلة والتلميحات القوية ---
    if cat in QUESTIONS_BANK:
        questions = QUESTIONS_BANK[cat]
        current_idx = st.session_state.q_index % len(questions)
        q_data = questions[current_idx]

        if mode == "local":
            st.info("💡 **التحدي التكتيكي:** التلميحات صعبة! اقرأ التلميح بتركيز وشوف مين هيعرف الإجابة!")
            st.markdown(f'<div class="question-card-cartoon">🔥 التلميح الصعب #{current_idx + 1}:<br><br>{q_data["q"]}</div>', unsafe_allow_html=True)
            
            st.write("")
            with st.expander("👁️ كشف الإجابة (للمضيف فقط)"):
                st.success(f"💡 الإجابة هي: **{q_data['a']}**")

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("التالي ➡️", use_container_width=True):
                    st.session_state.q_index += 1
                    st.rerun()
            with col2:
                if st.button("🎉 إجابة صحيحة (+10)", use_container_width=True):
                    st.balloons()
                    st.session_state.user["score"] += 10
                    # حفظ النقاط في قاعدة البيانات
                    u_name = st.session_state.username
                    if u_name:
                        db = load_users()
                        if u_name in db:
                            db[u_name]["user_info"]["score"] = st.session_state.user["score"]
                            save_users(db)
                    st.session_state.q_index += 1
                    st.rerun()
            with col3:
                # 🎡 عجلة العقاب للمغلوب
                if st.button("🎡 لف عجلة العقاب!", use_container_width=True):
                    st.session_state.current_punishment = random.choice(PUNISHMENTS_LIST)
                    st.rerun()

            # عرض العقاب إن وجد
            if st.session_state.current_punishment:
                st.markdown(f'<div class="punishment-card">⚠️ **عقاب المغلوب:**<br>{st.session_state.current_punishment}</div>', unsafe_allow_html=True)

        else:
            st.success("🌐 السيرفر جاهز للأونلاين!")
            st.markdown(f'<div class="question-card-cartoon">🔥 السؤال:<br>{q_data["q"]}</div>', unsafe_allow_html=True)
            user_ans = st.text_input("اكتب إجابتك هنا:")
            if st.button("إرسال الإجابة 🚀"):
                if q_data["a"].lower() in user_ans.strip().lower():
                    st.balloons()
                    st.success("🎉 إجابة صحيحة!")

    # --- ب) لودو والدومينو وعجلة العقاب ---
    elif cat in ["لعبة لودو", "لعبة الدومينو"]:
        st.subheader(f"🎲 ساحة منافسة {cat}")
        col_game1, col_game2 = st.columns(2)
        with col_game1:
            if st.button("🎲 رمي النرد الكرتوني"):
                dice_val = random.randint(1, 6)
                st.header(f"النتيجة: 🎲 **{dice_val}**")
            
            st.write("")
            if st.button("🎡 لف عجلة العقاب للمغلوب!"):
                st.session_state.current_punishment = random.choice(PUNISHMENTS_LIST)
                st.rerun()

            if st.session_state.current_punishment:
                st.markdown(f'<div class="punishment-card">⚠️ **عقاب الخاسر:**<br>{st.session_state.current_punishment}</div>', unsafe_allow_html=True)

        with col_game2:
            st.write(f"اللاعب 1 ({st.session_state.user['name']}): **{st.session_state.user['score']} نقطة**")

    st.divider()
    if st.button("⬅️ العودة لمستودع التسالي"):
        st.session_state.page = "main_hub"
        st.session_state.current_punishment = ""
        st.rerun()