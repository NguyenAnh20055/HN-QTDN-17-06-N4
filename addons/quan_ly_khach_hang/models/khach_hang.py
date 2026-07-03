from odoo import fields, models, api

class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Khách Hàng'
    _rec_name = 'full_name'

    # 1. Chuyển thành trường Char bình thường để người dùng tự nhập
    full_name = fields.Char(string='Họ và tên', required=True)
    
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Số điện thoại', required=True)
    address = fields.Char(string='Địa chỉ')
    birthday = fields.Date(string='Ngày sinh')
    
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên phụ trách'
    )
    ho_tro_ids = fields.One2many('ho_tro_khach_hang', 'khach_hang_id', string='Hỗ trợ khách hàng')
    khach_hang_tiem_nang_ids = fields.One2many('khach_hang_tiem_nang', 'khach_hang_id', string='Khách hàng tiềm năng')
    phan_cong_ids = fields.One2many(
        'phan_cong_cong_viec',
        'khach_hang_id',
        string='Phân công'
    )
    loai_khach_hang = fields.Selection([
        ('tiem_nang', 'Tiềm năng'),
        ('chinh_thuc', 'Chính thức')
    ], string="Loại khách hàng", default='tiem_nang')