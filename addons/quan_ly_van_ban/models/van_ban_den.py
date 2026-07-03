from odoo import models, fields, api


class VanBanDen(models.Model):
    _name = 'van_ban_den'
    _description = 'Văn bản đến'

    ma = fields.Char(
        'Mã',
        required=True,
        readonly=True,
        copy=False,
        default='New'
    )

    ten = fields.Char('Tên văn bản', required=True)

    thoi_gian = fields.Datetime(
        'Thời gian',
        default=fields.Datetime.now
    )

    loai_van_ban_id = fields.Many2one(
        'loai_van_ban',
        required=True,
        string='Loại văn bản'
    )

    khach_hang_id = fields.Many2one(
        'khach_hang',
        string='Khách hàng'
    )

    nhan_vien_phu_trach_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên phụ trách'
    )

    ky_xac_nhan = fields.Char('Ký xác nhận')

    han = fields.Date('Hạn')

    file_dinh_kem = fields.Binary('File đính kèm')

    danh_sach_van_ban_id = fields.Many2one(
        'danh_sach_van_ban'
    )

    trang_thai = fields.Selection([
        ('moi', 'Mới nhận'),
        ('dang_xu_ly', 'Đang xử lý'),
        ('da_xu_ly', 'Đã xử lý'),
    ], string='Trạng thái', default='moi')

    # ================= MAP =================

    def _map_trang_thai(self, state):
        return {
            'moi': 'new',
            'dang_xu_ly': 'active',
            'da_xu_ly': 'processed',
        }.get(state, 'draft')

    # ================= CREATE =================

    @api.model
    def create(self, vals):

        # Sinh mã tự động
        if vals.get('ma', 'New') == 'New':
            vals['ma'] = self.env['ir.sequence'].next_by_code(
                'quan_ly_van_ban.sequence'
            ) or 'New'

        record = super().create(vals)

        ds = self.env['danh_sach_van_ban'].create({
            'ten': record.ten,
            'ma': record.ma,
            'thoi_gian': record.thoi_gian,

            'loai_xu_ly': 'den',
            'loai_model': 'den',

            'loai_van_ban_id': record.loai_van_ban_id.id,

            'khach_hang_id': record.khach_hang_id.id,
            'nhan_vien_phu_trach_id': record.nhan_vien_phu_trach_id.id,

            'trang_thai': self._map_trang_thai(record.trang_thai),
        })

        record.danh_sach_van_ban_id = ds.id

        return record

    # ================= WRITE =================

    def write(self, vals):

        res = super().write(vals)

        for rec in self:

            if rec.danh_sach_van_ban_id:
                rec.danh_sach_van_ban_id.write({
                    'ten': rec.ten,
                    'ma': rec.ma,
                    'thoi_gian': rec.thoi_gian,

                    'loai_van_ban_id': rec.loai_van_ban_id.id,
                    'khach_hang_id': rec.khach_hang_id.id,
                    'nhan_vien_phu_trach_id': rec.nhan_vien_phu_trach_id.id,

                    'trang_thai': rec._map_trang_thai(rec.trang_thai),
                })

        return res

    # ================= DELETE =================

    def unlink(self):

        ds = self.mapped('danh_sach_van_ban_id')

        res = super().unlink()

        ds.unlink()

        return res