from odoo import models, fields


class DanhSachVanBan(models.Model):
    _name = 'danh_sach_van_ban'
    _description = 'Danh sách văn bản'
    _rec_name = 'ten'

    ten = fields.Char(
        string='Tên văn bản',
        required=True
    )

    ma = fields.Char(
        string='Mã',
        required=True
    )

    file_dinh_kem = fields.Binary(
        string='File đính kèm'
    )

    file_name = fields.Char(
        string='Tên file'
    )

    khach_hang_id = fields.Many2one(
        'khach_hang',
        string='Khách hàng'
    )

    loai_van_ban_id = fields.Many2one(
        'loai_van_ban',
        string='Loại văn bản'
    )

    nhan_vien_phu_trach_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên phụ trách'
    )

    thoi_gian = fields.Datetime(
        string='Thời gian',
        default=fields.Datetime.now
    )

    trang_thai = fields.Selection([
        ('draft', 'Chờ gửi'),
        ('new', 'Mới'), 
        ('active', 'Đang xử lý'),
        ('processed', 'Đã xử lý'),
        ('done', 'Hoàn thành'),
        ('sent', 'Đã gửi'),
        ('archived', 'Hoàn thành'),
    ], string='Trạng thái', default='draft')

    loai_xu_ly = fields.Selection([
        ('den', 'Văn bản đến'),
        ('di', 'Văn bản đi'),
        ('noi_bo', 'Văn bản nội bộ')
    ],
        string='Loại xử lý'
    )

    loai_model = fields.Selection([
        ('den', 'Văn bản đến'),
        ('di', 'Văn bản đi'),
        ('noi_bo', 'Văn bản nội bộ')
    ], string="Loại model")

 