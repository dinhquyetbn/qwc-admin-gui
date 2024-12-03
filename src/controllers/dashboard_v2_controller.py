import os

from flask import json, jsonify

from .controller_v2 import ControllerV2


class DashboardV2Controller(ControllerV2):

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(DashboardV2Controller, self).__init__(
            "Trang chủ", "dashboard-v2", "dashboard-v2", "dashboard-v2", app, handler
        )
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule(
            "/api/dashboard-v2/thong-ke-so-luong",
            "get_thong_ke_so_luong",
            self.get_thong_ke_so_luong,
            methods=["GET"],
        )

    def get_thong_ke_so_luong(self):
        self.setup_models()
        session = self.session()
        resDonVi = (
            session.query(self.PBMSQuanLyDonVi)
            .filter(self.PBMSQuanLyDonVi.trang_thai_xoa == False)
            .count()
        )
        resNhaCS = (
            session.query(self.PBDMQuanLyNhaCongSan)
            .filter(self.PBDMQuanLyNhaCongSan.trang_thai_xoa == False)
            .count()
        )
        resDatCS = (
            session.query(self.PBDMQuanLyDatCong)
            .filter(self.PBDMQuanLyDatCong.trang_thai_xoa == False)
            .count()
        )
        data = {
            "so_luong_don_vi": resDonVi,
            "so_luong_nha_cs": resNhaCS,
            "so_luong_dat_cs": resDatCS,
            "so_luong_nha_bao_tri": 0,
        }
        session.close()
        return jsonify({"result": data})
