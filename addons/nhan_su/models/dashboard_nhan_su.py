from odoo import models, fields, api

class DashboardNhanSu(models.Model):
    _name = 'dashboard.nhan.su'
    _description = 'Dashboard Nhân Sự'

    tong_nhan_vien = fields.Integer(string="Tổng nhân viên", compute="_compute_data")
    dang_lam_viec = fields.Integer(string="Đang làm việc", compute="_compute_data")
    da_nghi_viec = fields.Integer(string="Đã nghỉ việc", compute="_compute_data")

    @api.depends()
    def _compute_data(self):
        for r in self:
            r.tong_nhan_vien = self.env['nhan_vien'].search_count([])
            r.dang_lam_viec = self.env['nhan_vien'].search_count([
                ('trang_thai', '=', 'dang_lam_viec')
            ])
            r.da_nghi_viec = self.env['nhan_vien'].search_count([
                ('trang_thai', '=', 'da_nghi_viec')
            ])