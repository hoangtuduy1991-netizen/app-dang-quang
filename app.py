import streamlit as st
import google.generativeai as genai
import json
from PIL import Image

st.set_page_config(page_title="Đăng Quang Education", layout="wide")
st.title("🧮 ĐĂNG QUANG EDUCATION")

# Sử dụng st.secrets nếu có, hoặc dùng session_state để lưu API Key
if "api_key" not in st.session_state: st.session_state.api_key = ""

tab1, tab2 = st.tabs(["📝 HỌC SINH NỘP BÀI", "📊 KHU VỰC ADMIN"])

with tab1:
    st.subheader("Nộp bài tập")
    ma_de = st.text_input("Nhập Mã đề/Trang bài tập:")
    anh = st.file_uploader("Tải ảnh bài làm:", type=["jpg", "png", "jpeg"])
    
    if st.button("🚀 CHẤM BÀI CHUYÊN SÂU"):
        if not st.session_state.api_key:
            st.error("Chưa cấu hình API Key trong mục Admin!")
        elif not anh or not ma_de:
            st.warning("Vui lòng nhập mã đề và tải ảnh lên.")
        else:
            try:
                genai.configure(api_key=st.session_state.api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Bạn là trợ lý giáo viên. Hãy chấm bài cho mã đề {ma_de} dựa trên ảnh này.
                Trả về JSON duy nhất với các trường: 
                "diem": (0-100), "loi_sai": "...", "nguyen_nhan": "...", "huong_giai_quyet": "...", "canh_bao_gian_lan": "Có/Không và lý do".
                """
                response = model.generate_content([prompt, Image.open(anh)])
                res = json.loads(response.text.replace("```json", "").replace("```", "").strip())
                
                st.metric("Điểm số", f"{res['diem']}/100")
                st.write(f"**❌ Lỗi sai:** {res['loi_sai']}")
                st.write(f"**💡 Nguyên nhân:** {res['nguyen_nhan']}")
                st.write(f"**🛠 Hướng giải quyết:** {res['huong_giai_quyet']}")
                st.error(f"**⚠️ Cảnh báo gian lận:** {res['canh_bao_gian_lan']}")
            except Exception as e:
                st.error(f"Lỗi: {e}")

with tab2:
    st.subheader("🔐 Cấu hình Admin")
    mk = st.text_input("Mật khẩu:", type="password")
    if mk == "DangQuang2026":
        st.session_state.api_key = st.text_input("Nhập API Key:", value=st.session_state.api_key, type="password")
        st.info("API Key đã được cập nhật cho phiên làm việc này.")
