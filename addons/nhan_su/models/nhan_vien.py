import datetime
import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten'
    
    _sql_constraints = [
        (
            'unique_ma_nhan_vien',
            'unique(ma_nhan_vien)',
            'Mã nhân viên đã tồn tại!'
        ),
        (
            'unique_email',
            'unique(email)',
            'Email đã tồn tại!'
        ),
    ] 
    ma_nhan_vien = fields.Char(
        string="Mã nhân viên",
        required=True
    )

    ho_ten = fields.Char(string="Họ tên", required=True)
    ngay_sinh = fields.Date(string="Ngày sinh")
    gioi_tinh = fields.Selection(
        [
            ('nam', 'Nam'),
            ('nu', 'Nữ'),
            ('khac', 'Khác'),
        ],
        string="Giới tính",
        required=True
    )
    que_quan = fields.Char(string="Quê quán")
    email = fields.Char(string="Email")
    so_dien_thoai = fields.Char(string="Số điện thoại")

    image_1920 = fields.Image(
        string="Ảnh nhân viên",
        max_width=1920,
        max_height=1920
    )

    trang_thai = fields.Selection(
    [
            ('dang_lam_viec', 'Đang làm việc'),
            ('da_nghi_viec', 'Đã nghỉ việc'),
        ],
        string='Trạng thái',
        default='dang_lam_viec',
        required=True
    )
    
    phong_ban_ids = fields.Many2many(comodel_name='phong_ban', string="Phòng ban")
    lich_su_cong_tac_ids = fields.One2many(
        comodel_name='lich_su_cong_tac', 
        inverse_name="nhan_vien_id",
        string="Lịch sử công tác"
    )
    chung_chi_ids = fields.One2many(
        comodel_name='chung_chi', 
        inverse_name="nhan_vien_id",
        string="Chứng chỉ"
    )
    
    
    # Các field tính toán
    tuoi = fields.Integer(string="Tuổi", compute='_compute_tuoi', store=True)
    thang_sinh = fields.Integer(string="Tháng sinh", compute='_compute_thang_sinh', store=True)

    def name_get(self):
        result = []
        for rec in self:
            name = f"[{rec.ma_nhan_vien}] {rec.ho_ten}"
            result.append((rec.id, name))
        return result

    @api.depends("ngay_sinh")
    def _compute_tuoi(self):
        today = datetime.date.today()
        for record in self:
            if record.ngay_sinh:
                record.tuoi = today.year - record.ngay_sinh.year
            else:
                record.tuoi = 0

    @api.depends("ngay_sinh") # Sửa từ onchange thành depends để lưu database
    def _compute_thang_sinh(self):
        for record in self:
            if record.ngay_sinh:
                record.thang_sinh = record.ngay_sinh.month
            else:
                record.thang_sinh = 0

    @api.constrains('tuoi')
    def _check_tuoi(self):
        for record in self:
            # Chỉ check nếu có nhập ngày sinh (tuổi > 0)
            if record.ngay_sinh and record.tuoi < 18:
                raise ValidationError("Nhân viên phải từ 18 tuổi trở lên.")

    @api.constrains('email')
    def _check_email(self):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("Email không hợp lệ!")

    @api.constrains('so_dien_thoai')
    def _check_so_dien_thoai(self):
        phone_regex = r'^\d{10,11}$'
        for record in self:
            if record.so_dien_thoai and not re.match(phone_regex, record.so_dien_thoai):
                raise ValidationError("Số điện thoại không hợp lệ! Phải có 10 hoặc 11 chữ số.")