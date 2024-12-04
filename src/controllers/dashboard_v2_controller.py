import os

from flask import json, jsonify
from sqlalchemy import text
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

        self.app.add_url_rule(
            "/api/dashboard-v2/thong-ke-nha-dat-theo-qh",
            "get_thong_ke_nha_dat_theo_qh",
            self.get_thong_ke_nha_dat_theo_qh,
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

    def get_thong_ke_nha_dat_theo_qh(self):
        self.setup_models()
        session = self.session()
        # Lấy danh sách quận huyện của Đà Nẵng
        dataQuanHuyen = (
            session.query(self.PBDMDanhMucQuanHuyen.ma, self.PBDMDanhMucQuanHuyen.ten)
            .filter(
                self.PBDMDanhMucQuanHuyen.trang_thai_xoa == False,
                self.PBDMDanhMucQuanHuyen.ma_tp == "48",
            )
            .all()
        )

        # Lấy danh sách nhà công sản
        sql_queryNha = text(
            """
                SELECT ma_qh, COUNT(ma_qh)
                FROM qwc_config.pbms_quan_ly_nha_cong_san
                WHERE trang_thai_xoa = FALSE
                GROUP BY ma_qh;
            """
        )
        resNha = session.execute(sql_queryNha)
        dataNhas = resNha.fetchall()
        # Lấy danh sách đất công sản
        sql_queryDat = text(
            """
                SELECT ma_qh, COUNT(ma_qh)
                FROM qwc_config.pbms_quan_ly_dat_cong
                WHERE trang_thai_xoa = FALSE
                GROUP BY ma_qh;
            """
        )
        resDat = session.execute(sql_queryDat)
        dataDats = resNha.fetchall()

        valLabel = []
        valNha = []
        valDat = []

        for item in dataQuanHuyen:
            valLabel.append(item.ten)
            valNha.append(next((x[1] for x in dataNhas if x[0] == item.ma), 0))
            valDat.append(next((x[1] for x in dataDats if x[0] == item.ma), 0))

        data = {"labels": valLabel, "valueDat": valDat, "valueNha": valNha}
        session.close()
        return jsonify({"result": data})
