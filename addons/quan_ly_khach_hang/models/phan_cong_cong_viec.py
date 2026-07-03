from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import date

class PhanCongCongViec(models.Model):
    _name = 'phan_cong_cong_viec'
    _description = 'Phân công công việc'

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Mã nhân viên',
        required=True
    )
    khach_hang_id = fields.Many2one(
        'khach_hang',
        string='Khách hàng',
        required=True
    )
    hoat_dong_id = fields.Many2one(
        'hoat_dong',
        string='Hoạt động'
    )

    ho_tro_khach_hang_id = fields.Many2one(
        'ho_tro_khach_hang',
        string='Hỗ trợ khách hàng'
    )

    ngay_phan_cong = fields.Date(string='Ngày phân công', required=True)
    han_hoan_thanh = fields.Date(
        string="Hạn hoàn thành"
    )
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('dang_thuc_hien', 'Đang thực hiện'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy')
    ], string='Trạng thái', default='moi', required=True)

    @api.constrains('ngay_phan_cong')
    def _check_ngay_phan_cong(self):
        for record in self:
            if record.ngay_phan_cong and record.ngay_phan_cong > date.today():
                raise ValidationError(_("Ngày phân công không thể lớn hơn ngày hiện tại!"))

    @api.constrains('hoat_dong_id', 'ho_tro_khach_hang_id')
    def _check_hoat_dong_or_ho_tro(self):
        for record in self:
            if record.hoat_dong_id and record.ho_tro_khach_hang_id:
                raise ValidationError(_("Chỉ chọn Hoạt động hoặc Hỗ trợ khách hàng, không chọn cả hai!"))

            if not record.hoat_dong_id and not record.ho_tro_khach_hang_id:
                raise ValidationError(_("Phải chọn Hoạt động hoặc Hỗ trợ khách hàng!"))