from odoo import models, fields

class LoaiVanBan(models.Model):
    _name = 'loai_van_ban'
    _description = 'Loại văn bản'
    _rec_name = 'ten'
    ma = fields.Char('Mã', required=True)
    ten = fields.Char('Tên loại', required=True)
    mo_ta = fields.Text('Mô tả')
    hieu_luc = fields.Boolean('Hiệu lực', default=True)
