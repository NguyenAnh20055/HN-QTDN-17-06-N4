from odoo import models, fields, api


class DashboardVanBan(models.Model):
    _name = 'dashboard.van.ban'
    _description = 'Dashboard Văn Bản'

    name = fields.Char(default='Dashboard')

    tong_van_ban = fields.Integer(
        compute='_compute_dashboard'
    )

    tong_van_ban_den = fields.Integer(
        compute='_compute_dashboard'
    )

    tong_van_ban_di = fields.Integer(
        compute='_compute_dashboard'
    )

    tong_van_ban_noi_bo = fields.Integer(
        compute='_compute_dashboard'
    )

    def _compute_dashboard(self):
        for rec in self:

            rec.tong_van_ban = self.env[
                'danh_sach_van_ban'
            ].search_count([])

            rec.tong_van_ban_den = self.env[
                'danh_sach_van_ban'
            ].search_count([
                ('loai_xu_ly', '=', 'den')
            ])

            rec.tong_van_ban_di = self.env[
                'danh_sach_van_ban'
            ].search_count([
                ('loai_xu_ly', '=', 'di')
            ])

            rec.tong_van_ban_noi_bo = self.env[
                'danh_sach_van_ban'
            ].search_count([
                ('loai_xu_ly', '=', 'noi_bo')
            ])