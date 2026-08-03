import streamlit as st
import json
import os

# --- 1. إعدادات لوحة التحكم ---
st.set_page_config(
    page_title="👑 غرفة التحكم بالأدمن - مستودع التسالي",
    page_icon="⚙️",
    layout="wide"
)

DATA_FILE = "sahebk_data.json"
ADMIN_PASSWORD = "123"  # 🔒 تقدر تغير باسورد الأدمن من هنا

# --- 2. دالة تحميل وحفظ البيانات ---
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "users": {},
        "questions": {
            "أفلام وسينما مصرية": [],
            "كورة على السريع": [],
            "شخصيات مشهورة": []
        },
        "punishments": [],
        "announcements": ""
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

db = load_data()

# --- 3. تسجيل دخول الأدمن ---
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.title("⚙️ غرفة إدارة اللعبة (Admin Panel)")

if not st.session_state.admin_logged_in:
    pwd = st.text_input("🔑 أدخل كلمة سر الأدمن:", type="password")
    if st.button("تسجيل الدخول 🚀"):
        if pwd == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("تم الدخول بنجاح!")
            st.rerun()
        else:
            st.error("كلمة السر غير صحيحة!")
else:
    st.sidebar.success("👑 أهلاً بك يا مدير اللعبة!")
    if st.sidebar.button("خروج 🚪"):
        st.session_state.admin_logged_in = False
        st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs([
        "❓ إضافة أسئلة جديدة", 
        "🎡 إدارة عجلة العقاب", 
        "👥 إدارة اللاعبين والسكور", 
        "📢 إرسال إشعار عام"
    ])

    # ----------------------------------------
    # 🎯 التاب 1: إضافة أسئلة وتلميحات
    # ----------------------------------------
    with tab1:
        st.subheader("➕ إضافة سؤال وتلميح جديد للعبة")
        
        category = st.selectbox("اختار القسم:", ["أفلام وسينما مصرية", "كورة على السريع", "شخصيات مشهورة"])
        new_q = st.text_area("نص التلميح / السؤال الصعب:")
        new_a = st.text_input("الإجابة الصحيحة:")

        if st.button("✨ حفظ السؤال في اللعبة"):
            if new_q and new_a:
                if category not in db["questions"]:
                    db["questions"][category] = []
                
                db["questions"][category].append({"q": new_q, "a": new_a})
                save_data(db)
                st.success(f"تمت إضافة السؤال بنجاح إلى قسم ({category})!")
            else:
                st.warning("يرجى ملء جميع الحقول.")

        st.divider()
        st.write("📊 **الأسئلة الحالية المضافة عبر الأدمن:**")
        st.json(db.get("questions", {}))

    # ----------------------------------------
    # 🎯 التاب 2: إدارة عجلة العقاب
    # ----------------------------------------
    with tab2:
        st.subheader("🎡 إضافة عقاب جديد لعجلة العقاب")
        new_punish = st.text_input("اكتب العقاب الجديد (مثال: اعمل 15 ضغط):")
        
        if st.button("➕ إضافة العقاب"):
            if new_punish:
                if "punishments" not in db:
                    db["punishments"] = []
                db["punishments"].append(new_punish)
                save_data(db)
                st.success("تمت إضافة العقاب بنجاح!")
            else:
                st.warning("اكتب نص العقاب أولاً!")

        st.divider()
        st.write("📋 **قائمة العقابات الحالية:**")
        st.write(db.get("punishments", []))

    # ----------------------------------------
    # 🎯 التاب 3: تعديل بيانات السكور واللاعبين
    # ----------------------------------------
    with tab3:
        st.subheader("👥 التحكم في سكور وتفاصيل اللاعبين")
        user_id = st.text_input("أدخل الـ ID الخاص باللاعب (مثال: #12345):")
        new_score = st.number_input("السكور الجديد:", min_value=0, value=0)

        if st.button("💾 تعديل سكور اللاعب"):
            if user_id:
                if "users" not in db:
                    db["users"] = {}
                db["users"][user_id] = {"score": new_score}
                save_data(db)
                st.success(f"تم تعديل سكور اللاعب `{user_id}` إلى {new_score} نقطة!")

    # ----------------------------------------
    # 🎯 التاب 4: إشعار شريط الأخبار جوه اللعبة
    # ----------------------------------------
    with tab4:
        st.subheader("📢 نشر إشعار يظهر في أعلى الشاشة لكل اللاعبين")
        announcement = st.text_area("نص الإشعار:", value=db.get("announcements", ""))
        
        if st.button("📢 نشر الإشعار فوراً"):
            db["announcements"] = announcement
            save_data(db)
            st.success("تم نشر الإشعار بنجاح في اللعبة!")