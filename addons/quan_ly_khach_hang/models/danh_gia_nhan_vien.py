from odoo import models, fields, api

# 1. Định nghĩa bảng Đánh giá
class DanhGiaNhanVien(models.Model):
    _name = 'danh_gia_nhan_vien'
    _description = 'Khách hàng đánh giá nhân viên'
    _rec_name = 'nhan_vien_id' # Để khi search hiện tên nhân viên
    _order = 'thoi_gian_danh_gia desc'

    khach_hang_id = fields.Many2one(
        comodel_name='khach_hang', # Lưu ý: Nếu bạn dùng model chuẩn Odoo thì là 'res.partner'
        string='Khách hàng',
        required=True
    )

    nhan_vien_id = fields.Many2one(
        comodel_name='nhan_vien',
        string='Nhân viên được đánh giá',
        required=True,
        ondelete='cascade' # Xóa nhân viên thì xóa luôn đánh giá
    )

    diem_danh_gia = fields.Selection(
        [
            ('1', '1 - Rất không hài lòng'),
            ('2', '2 - Không hài lòng'),
            ('3', '3 - Bình thường'),
            ('4', '4 - Hài lòng'),
            ('5', '5 - Rất hài lòng'),
        ],
        string='Điểm đánh giá',
        required=True,
        default='5'
    )

    nhan_xet = fields.Text(string='Nhận xét chi tiết')

    thoi_gian_danh_gia = fields.Datetime(
        string='Thời gian',
        default=fields.Datetime.now
    )

    trang_thai = fields.Selection(
        [
            ('moi', 'Mới'),
            ('da_duyet', 'Đã duyệt'),
        ],
        string='Trạng thái',
        default='moi'
    )

# 2. Kế thừa model Nhân viên để thêm field danh sách đánh giá
# Class này nằm cùng file này hoặc 1 file khác trong module quan_ly_khach_hang đều được
class NhanVienInherit(models.Model):
    _inherit = 'nhan_vien'

    danh_gia_ids = fields.One2many(
        comodel_name='danh_gia_nhan_vien',
        inverse_name='nhan_vien_id',
        string='Lịch sử được khách hàng đánh giá'
    )
    
    # (Optional) Tính điểm trung bình
    diem_trung_binh = fields.Float(string="Điểm TB", compute="_compute_diem_trung_binh")

    @api.depends('danh_gia_ids.diem_danh_gia')
    def _compute_diem_trung_binh(self):
        for rec in self:
            total = 0
            count = 0
            for dg in rec.danh_gia_ids:
                if dg.diem_danh_gia:
                    total += int(dg.diem_danh_gia)
                    count += 1
            rec.diem_trung_binh = total / count if count > 0 else 0.0