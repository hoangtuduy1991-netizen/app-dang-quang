import streamlit as st
import google.generativeai as genai
import json
from PIL import Image

# Cấu hình trang
st.set_page_config(page_title="Đăng Quang Education", layout="wide")
st.title("🧮 ĐĂNG QUANG EDUCATION")

# Khởi tạo API key trong session_state
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Tạo 2 tab
tab1, tab2 = st.tabs(["📝 HỌC SINH NỘP BÀI", "📊 KHU VỰC ADMIN"])

with tab1:
    st.write("### Nộp bài tập Toán")
    anh = st.file_uploader("Tải ảnh bài làm của em lên đây:", type=["jpg", "png", "jpeg"])
    
    if anh is not None and st.button("🚀 CHẤM BÀI"):
        if st.session_state.api_key == "":
            st.warning("⚠️ Thầy/Cô chưa nhập API Key ở phần Admin!")
        else:
            try:
                # Cấu hình AI
                genai.configure(api_key=st.session_state.api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Chuẩn bị ảnh và câu lệnh
                image_parts = Image.open(anh)
                prompt = "Chấm điểm bài toán này theo thang 100. Chỉ trả về duy nhất một đoạn mã JSON (tuyệt đối không kèm văn bản khác) với cấu trúc chính xác sau: {\"tong_diem\": 90, \"nhan_xet\": \"Bài làm tốt...\"}"
                
                # Gọi AI
                with st.spinner("🤖 Trợ lý AI đang chấm bài..."):
                    response = model.generate_content([prompt, image_parts])
                
                # Làm sạch kết quả trả về cực kỳ cẩn thận để tránh lỗi JSON
                ket_qua = response.text.strip()
                if ket_qua.startswith("```json"):
                    ket_qua = ket_qua[7:]
                elif ket_qua.startswith("```"):
                    ket_qua = ket_qua[3:]
                if ket_qua.endswith("```"):
                    ket_qua = ket_qua[:-3]
                
                # Đọc JSON
                res = json.loads(ket_qua.strip())
                
                st.success("✅ Đã chấm xong!")
                st.write(f"### Điểm số: {res['tong_diem']}/100")
                st.write(f"**Nhận xét của AI:** {res['nhan_xet']}")
                
            except Exception as e:
                st.error("⚠️ Trợ lý AI không đọc được chữ trong ảnh hoặc ảnh chưa rõ nét. Em hãy chụp lại nhé!")

with tab2:
    st.write("### 🔐 Dành cho Thạc sĩ Hoàng Tư Duy")
    mk = st.text_input("Nhập mật khẩu quản trị:", type="password")
    if mk == "DangQuang2026":
        st.success("Đăng nhập thành công!")
        st.session_state.api_key = st.text_input("Nhập Google API Key của thầy:", type="password", value=st.session_state.api_key)
        st.write("*(Hệ thống đã sẵn sàng chấm bài sau khi nhập API Key)*")
    elif mk != "":st.error("Sai mật khẩu!")
