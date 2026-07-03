import requests
from odoo import models, fields

class AITimKiem(models.Model):
    _name = 'ai_tim_kiem'
    _description = 'AI Chatbot tìm kiếm văn bản'

    cau_hoi = fields.Text(string="Câu hỏi")
    ket_qua = fields.Html(string="Kết quả", readonly=True)

    def action_hoi_ai(self):
        self.ensure_one()

        API_KEY = "AIzaSyBVxYNtvkmK08HGao0ijt9ctL4WCdeyqHQ"

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-2.5-flash:generateContent"
            f"?key={API_KEY}"
        )

        # 🔹 Lấy danh sách văn bản
        van_bans = self.env['danh_sach_van_ban'].search([])

        context = ""
        for vb in van_bans:
            context += f"- Mã: {vb.ma}, Tên: {vb.ten}, Trạng thái: {vb.trang_thai}\n"

        prompt = f"""
Bạn là trợ lý AI quản lý văn bản trong Odoo.

Danh sách văn bản:
{context}

Người dùng hỏi:
{self.cau_hoi}

Chỉ trả lời theo định dạng:
Mã: <ma>
"""

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        headers = {"Content-Type": "application/json"}
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        result = resp.json()

        if "candidates" not in result:
            self.ket_qua = f"<b style='color:red'>Lỗi Gemini API:</b> {result}"
            return

        ai_text = result["candidates"][0]["content"]["parts"][0]["text"]

        # 🔍 Tách mã văn bản AI trả về
        ma_vb = ai_text.replace("Mã:", "").strip()

        van_ban = self.env['danh_sach_van_ban'].search([
            ('ma', '=', ma_vb)
        ], limit=1)

        if not van_ban:
            self.ket_qua = f"<b style='color:red'>❌ Không tìm thấy văn bản mã {ma_vb}</b>"
            return

        # 🔗 Link mở form chi tiết
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        link = (
            f"{base_url}/web#"
            f"id={van_ban.id}"
            f"&model=danh_sach_van_ban"
            f"&view_type=form"
        )

        self.ket_qua = f"""
        <b>📄 Văn bản tìm được:</b><br/>
        <ul>
            <li><b>Mã:</b> {van_ban.ma}</li>
            <li><b>Tên:</b> {van_ban.ten}</li>
            <li><b>Trạng thái:</b> {van_ban.trang_thai}</li>
        </ul>
        👉 <a href="{link}" target="_blank"><b>MỞ CHI TIẾT VĂN BẢN</b></a>
        """
