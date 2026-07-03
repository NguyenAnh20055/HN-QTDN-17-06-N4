from odoo import models, fields, api


class DashboardKhachHang(models.Model):
    _name = 'dashboard.khach.hang'
    _description = 'Dashboard CRM'

    name = fields.Char(default='Dashboard CRM')

    tong_khach_hang = fields.Integer(compute='_compute_dashboard')
    khach_hang_tiem_nang = fields.Integer(compute='_compute_dashboard')

    tong_hop_dong = fields.Integer(compute='_compute_dashboard')
    hop_dong_hieu_luc = fields.Integer(compute='_compute_dashboard')

    ho_tro_mo = fields.Integer(compute='_compute_dashboard')
    ho_tro_dong = fields.Integer(compute='_compute_dashboard')

    cong_viec_cho = fields.Integer(compute='_compute_dashboard')

    def _compute_dashboard(self):
        for rec in self:

            rec.tong_khach_hang = self.env['khach_hang'].search_count([])

            rec.khach_hang_tiem_nang = self.env['khach_hang'].search_count([
                ('loai_khach_hang', '=', 'tiem_nang')
            ]) if 'loai_khach_hang' in self.env['khach_hang']._fields else 0

            rec.tong_hop_dong = self.env['hop_dong'].search_count([])

            rec.hop_dong_hieu_luc = self.env['hop_dong'].search_count([
                ('trang_thai', '=', 'hieu_luc')
            ])

            rec.ho_tro_mo = self.env['ho_tro_khach_hang'].search_count([
                ('trang_thai', '=', 'mo')
            ])

            rec.ho_tro_dong = self.env['ho_tro_khach_hang'].search_count([
                ('trang_thai', '=', 'dong')
            ])

            rec.cong_viec_cho = self.env['phan_cong_cong_viec'].search_count([
                ('trang_thai', '=', 'cho')
            ])