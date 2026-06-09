import streamlit as st
import google.generativeai as genai
import pandas as pd
import io
import json
from PIL import Image
from datetime import datetime

# Cấu hình giao diện
st.set_page_config(page_title="Đăng Quang Education", page_icon="🧮", layout="wide")

st.title("🧮 ĐĂNG QUANG EDUCATION")
st.markdown("### **Hệ Thống Quản Lý Giáo Dục & Chấm Bài Toán AI Thông Minh**")
st.info("👨‍🏫 **Sáng lập:** Thạc sĩ Hoàng Tư Duy | 📞 **Hotline:** 0987.882.348")

# Khởi tạo dữ liệu hệ thống
if "api_key" not in st.session_state: st.session_state.api_key = ""
if "cau_truc_lop" not in st.session_state:
    st.session_state.cau_truc_lop = {
        "Khối 12": {"Chương 1: Hàm Số": {"loai": "Bài tập", "de_bai": "Bài 3, 4 Trang 45", "han_nop": "Thứ 5"}},
        "Khối 11": {"Chương 1: Lượng Giác": {"loai": "Bài tập", "de_bai": "Bài 1 Trang 20", "han_nop": "Chủ Nhật"}},
        "Khối 10": {"Chương 1: Mệnh Đề": {"loai": "Bài tập", "de_bai": "Bài 2 Trang 10", "han_nop": "Thứ 4"}}
    }
if "danh_sach_hs" not in st.session_state:
    st.session_state.danh_sach_hs = {"Khối 12": ["01. Nguyễn Hoàng An"], "Khối 11": ["01. Hoàng Văn Đạt"], "Khối 10": ["01. Bùi Khánh Linh"]}
if "ma_bao_mat" not in st.session_state:
    st.session_state.ma_bao_mat = {"Khối 12": "DQ12", "Khối 11": "DQ11", "Khối 10": "DQ10"}
if "lich_su_cham_diem" not in st.session_state: st.session_state.lich_su_cham_diem = []
if "ket_qua_vua_cham" not in st.session_state: st.session_state.ket_qua_vua_cham = None

# Giao diện chính
tab1, tab2, tab3 = st.tabs(["📝 HỌC SINH NỘP BÀI", "🔍 TRA CỨU NHANH", "📊 TRUNG TÂM QUẢN LÝ"])

with tab1:
    khoi = st.selectbox("Chọn khối:", list(st.session_state.cau_truc_lop.keys()))
    ma = st.text_input("Nhập mã bảo mật khối:", type="password")
    if ma == st.session_state.ma_bao_mat.get(khoi):
        ten = st.selectbox("Học sinh:", st.session_state.danh_sach_hs[khoi])
        muc = st.selectbox("Nội dung nộp:", list(st.session_state.cau_truc_lop[khoi].keys()))
        anh = st.file_uploader("Tải ảnh bài làm:", type=["jpg", "png"])
        if anh and st.button("🚀 NỘP BÀI & XEM ĐIỂM"):
            # Logic AI chấm điểm
            if st.session_state.api_key:
                genai.configure(api_key=st.session_state.api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(["Chấm điểm bài toán này theo thang 100, trả về JSON với logic, trinh_bay, tu_luc, nhan_xet", Image.open(anh)])
                res = json.loads(response.text.replace("```json", "").replace("
```", ""))
            else:
                res = {"logic": 35, "trinh_bay": 18, "tu_luc": 19, "tong_diem": 92, "nhan_xet": "Bài làm rất tốt!"}
            
            st.session_state.ket_qua_vua_cham = res
st.success(f"Đã nộp bài! Điểm: {res['tong_diem']}/100")
        
        if st.session_state.ket_qua_vua_cham:
            if st.button("📄 XEM BÁO CÁO BÀI TẬP HÔM NAY"):
                st.write(f"### Kết quả: {st.session_state.ket_qua_vua_cham['nhan_xet']}")
                st.metric("Điểm tổng", st.session_state.ket_qua_vua_cham['tong_diem'])

with tab2:
    st.write("Lịch trình bài tập hiện tại:", st.session_state.cau_truc_lop)

with tab3:
    mk = st.text_input("Nhập mật khẩu Admin:", type="password")
    if mk == "DangQuang2026":
        st.session_state.api_key = st.text_input("Cài đặt Google API Key:", type="password")
        st.write("---")
        st.subheader("📊 Quản lý điểm số")
        if st.session_state.lich_su_cham_diem:
            st.dataframe(pd.DataFrame(st.session_state.lich_su_cham_diem))