from odoo import models, fields, api


class VanBanNoiBo(models.Model):
    _name = 'van_ban_noi_bo'
    _description = 'Văn bản nội bộ'

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

    nguoi_gui = fields.Many2one(
        'nhan_vien',
        string='Người gửi'
    )

    nguoi_nhan = fields.Many2one(
        'nhan_vien',
        string='Người nhận'
    )

    mo_ta = fields.Text('Mô tả')

    file_dinh_kem = fields.Binary('File đính kèm')

    danh_sach_van_ban_id = fields.Many2one(
        'danh_sach_van_ban'
    )

    trang_thai = fields.Selection([
        ('moi', 'Mới tạo'),
        ('dang_xu_ly', 'Đang xử lý'),
        ('hoan_thanh', 'Hoàn thành'),
    ], string='Trạng thái', default='moi')

    # ================= MAP =================

    def _map_trang_thai(self, state):
        return {
            'moi': 'draft',
            'dang_xu_ly': 'active',
            'hoan_thanh': 'done',
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

            'loai_xu_ly': 'noi_bo',
            'loai_model': 'noi_bo',

            'loai_van_ban_id': record.loai_van_ban_id.id,

            # Văn bản nội bộ không có khách hàng
            'khach_hang_id': False,

            # Người phụ trách là người gửi
            'nhan_vien_phu_trach_id': record.nguoi_gui.id,

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

                    'khach_hang_id': False,

                    'nhan_vien_phu_trach_id': rec.nguoi_gui.id,

                    'trang_thai': rec._map_trang_thai(rec.trang_thai),
                })

        return res

    # ================= DELETE =================

    def unlink(self):

        ds = self.mapped('danh_sach_van_ban_id')

        res = super().unlink()

        ds.unlink()

        return res