import os

from flask import json, jsonify, request

from .controller_v2 import ControllerV2


class PublicBuildingController(ControllerV2):

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(PublicBuildingController, self).__init__(
            "Danh sách nhà công sản",
            "public-building",
            "public-building",
            "public_building",
            app,
            handler,
        )
        self.register_routes()

    def register_routes(self):
        # get data by page
        self.app.add_url_rule(
            "/api/public-building/page",
            "get_data_by_page_public_building",
            self.get_data_by_page_public_building,
            methods=["POST"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/public-building/detail/<id>",
            "get_by_id_loai_public_building",
            self.get_by_id_public_building,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/public-building/create",
            "create_or_update_item_public_building",
            self.create_or_update_item_public_building,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/public-building/update/<id>",
            "create_or_update_item_public_building",
            self.create_or_update_item_public_building,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/public-building/delete/<id>",
            "remove_item_public_building",
            self.remove_item_public_building,
            methods=["DELETE"],
        )

    # Hàm cho danh sách tham số
    def get_data_by_page_public_building(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        query = session.query(self.PBDMQuanLyNhaCongSan).filter(
            self.PBDMQuanLyNhaCongSan.trang_thai_xoa == False
        )
        # Nếu có giá trị search
        if req_search["value"]:
            query = query.filter(
                self.PBDMQuanLyNhaCongSan.ma_tai_san.ilike(
                    "%%%s%%" % req_search["value"]
                )
                | self.PBDMQuanLyNhaCongSan.ten_ngoi_nha.ilike(
                    "%%%s%%" % req_search["value"]
                )
                | self.PBDMQuanLyNhaCongSan.ten_tp.ilike("%%%s%%" % req_search["value"])
                | self.PBDMQuanLyNhaCongSan.ten_qh.ilike("%%%s%%" % req_search["value"])
                | self.PBDMQuanLyNhaCongSan.ten_px.ilike("%%%s%%" % req_search["value"])
                | self.PBDMQuanLyNhaCongSan.dia_chi.ilike(
                    "%%%s%%" % req_search["value"]
                )
            )

        # Sort
        if req_order:
            idx_col = req_order[0]["column"]
            val_col = req_columns[idx_col]["data"]
            val_dir = req_order[0]["dir"]
            if val_dir == "asc":
                query = query.order_by(
                    getattr(self.PBDMQuanLyNhaCongSan, val_col).asc()
                )
            elif val_dir == "desc":
                query = query.order_by(
                    getattr(self.PBDMQuanLyNhaCongSan, val_col).desc()
                )
        else:
            query = query.order_by(self.PBDMQuanLyNhaCongSan.ngay_tao)

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()

        jsonData = [
            {
                "id": t1.id,
                "he_thong_id": t1.he_thong_id,
                "tai_san_id": t1.tai_san_id,
                "tai_san_theo_chu_so_huu_id": t1.tai_san_theo_chu_so_huu_id,
                "ma_tai_san": t1.ma_tai_san,
                "ten_ngoi_nha": t1.ten_ngoi_nha,
                "phan_loai_tai_san_id": t1.phan_loai_tai_san_id,
                "dia_chi": t1.dia_chi,
                "ma_px": t1.ma_px,
                "ten_px": t1.ten_px,
                "ma_qh": t1.ma_qh,
                "ten_qh": t1.ten_qh,
                "ma_tp": t1.ma_tp,
                "ten_tp": t1.ten_tp,
                "ds_file_dinh_kem": t1.ds_file_dinh_kem,
                "full_dia_chi": f"{t1.dia_chi}, {t1.ten_px}, {t1.ten_qh}, {t1.ten_tp}",
                "ngay_tao": self.convertUTCDateToVNTime(t1.ngay_tao),
            }
            for t1 in data
        ]
        pagination = {
            "draw": int(body_request["draw"]),
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": jsonData,
        }
        session.close()
        return jsonify({"result": pagination})

    def get_by_id_public_building(self):
        pass

    def create_or_update_item_public_building(self):
        pass

    def remove_item_public_building(self):
        pass
