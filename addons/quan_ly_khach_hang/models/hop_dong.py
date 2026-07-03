from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class HopDong(models.Model):
    _name = "hop_dong"
    _description = "Hợp đồng"
    _rec_name = "ten"

    ten = fields.Char(string="Tên hợp đồng", required=True)
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc", required=True)
    
    # Cần thêm currency_id để dùng widget monetary trong XML
    currency_id = fields.Many2one('res.currency', string='Tiền tệ', 
                                 default=lambda self: self.env.company.currency_id)
    gia_tri_hop_dong = fields.Monetary(string="Giá trị hợp đồng", currency_field='currency_id', required=True)
    
    trang_thai = fields.Selection([
        ('moi', 'Mới'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy')
    ], string="Trạng thái", default='moi')

    # KHỚP VỚI KHÁCH HÀNG
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng")
    

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay_hop_dong(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau and record.ngay_ket_thuc <= record.ngay_bat_dau:
                raise ValidationError(_("Ngày kết thúc không thể trước ngày bắt đầu."))