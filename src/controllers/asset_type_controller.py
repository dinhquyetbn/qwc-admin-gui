import os
import uuid

from datetime import datetime, timezone
from flask import json, jsonify, request
from .controller_v2 import ControllerV2


class AssetTypeController(ControllerV2):

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(AssetTypeController, self).__init__(
            "Danh sách danh mục phân loại tài sản",
            "asset-type",
            "asset-type",
            "asset_type",
            app,
            handler,
        )
        self.register_routes()

    def register_routes(self):
        # PHÂN LOẠI TÀI SẢN
        # get data by page
        self.app.add_url_rule(
            "/api/asset-type/type/page",
            "get_data_by_page_loai_ts",
            self.get_data_by_page_loai_ts,
            methods=["POST"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/asset-type/type/detail/<id>",
            "get_by_id_loai_ts",
            self.get_by_id_loai_ts,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/asset-type/type/create",
            "create_or_update_item_loai_ts",
            self.create_or_update_item_loai_ts,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/asset-type/type/update/<id>",
            "create_or_update_item_loai_ts",
            self.create_or_update_item_loai_ts,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/asset-type/type/delete/<id>",
            "remove_item_loai_ts",
            self.remove_item_loai_ts,
            methods=["DELETE"],
        )

        # delete
        self.app.add_url_rule(
            "/api/asset-type/type/categories/all",
            "get_categories_all_loai_ts",
            self.get_categories_all_loai_ts,
            methods=["GET"],
        )

        # danh sách tham số theo loai tài sản
        self.app.add_url_rule(
            "/api/asset-type/type/<id>/param",
            "get_all_param_by_loai_ts_id",
            self.get_all_param_by_loai_ts_id,
            methods=["GET"],
        )

    # Hàm cho danh sách tham số
    def get_data_by_page_loai_ts(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        # query = session.query(self.PBMSQuanLyThamSo).filter_by(trang_thai_xoa=False)
        query = session.query(self.PBMSQuanLyPhanLoaiTaiSan).filter(
            self.PBMSQuanLyPhanLoaiTaiSan.trang_thai_xoa == False
        )
        # Nếu có giá trị search
        if req_search["value"]:
            query = query.filter(
                self.PBMSQuanLyPhanLoaiTaiSan.ten_loai_ts.ilike(
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
                    getattr(self.PBMSQuanLyPhanLoaiTaiSan, val_col).asc()
                )
            elif val_dir == "desc":
                query = query.order_by(
                    getattr(self.PBMSQuanLyPhanLoaiTaiSan, val_col).desc()
                )
        else:
            query = query.order_by(self.PBMSQuanLyPhanLoaiTaiSan.ngay_tao)

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        jsonData = [
            {
                "id": tblLoaiTS.id,
                "ten_loai_ts": tblLoaiTS.ten_loai_ts,
                "ds_tham_so": tblLoaiTS.ds_tham_so,
                "mo_ta": tblLoaiTS.mo_ta,
                "ngay_tao": self.convertUTCDateToVNTime(tblLoaiTS.ngay_tao),
            }
            for tblLoaiTS in data
        ]
        pagination = {
            "draw": int(body_request["draw"]),
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": jsonData,
        }
        session.close()
        return jsonify({"result": pagination})

    def create_or_update_item_loai_ts(self, id=None):
        try:
            # Parse JSON data from the request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            if id is None:
                # create new
                obj = self.PBMSQuanLyPhanLoaiTaiSan()
                obj.id = str(uuid.uuid4())
                # obj.nguoi_tao = userLogin.gext('id') or None
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource_loai_ts(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.ngay_sua = datetime.now(timezone.utc)

            obj.ten_loai_ts = data["ten_loai_ts"]
            obj.ds_tham_so = data["ds_tham_so"]
            obj.mo_ta = data["mo_ta"]

            session.commit()
            # self.update_config_timestamp(session)
            session.close()
            # Return a success response
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            # Handle exceptions and return an error response
            return jsonify({"error": str(e)}), 500

    def remove_item_loai_ts(self, id):
        try:
            session = self.session()
            # Find the group parameter by id
            obj = self.find_resource_loai_ts(id, session)
            if obj is None:
                return jsonify({"error": "Không tìm thấy bản ghi."}), 404

            # Mark as deleted
            # obj.nguoi_xoa = ''
            obj.ngay_xoa = datetime.now(timezone.utc)
            obj.trang_thai_xoa = True
            session.commit()
            session.close()
            return jsonify({"message": "Xóa dữ liệu thành công."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_by_id_loai_ts(self, id):
        session = self.session()
        query = self.find_resource_loai_ts(id, session)
        jsonData = {
            "id": query.id,
            "ten_loai_ts": query.ten_loai_ts,
            "ds_tham_so": query.ds_tham_so,
            "mo_ta": query.mo_ta,
            "ngay_tao": self.convertUTCDateToVNTime(query.ngay_tao),
        }
        session.close()
        return jsonify({"result": jsonData})

    def find_resource_loai_ts(self, id, session):
        return (
            session.query(self.PBMSQuanLyPhanLoaiTaiSan)
            .filter_by(id=id, trang_thai_xoa=False)
            .first()
        )

    def get_categories_all_loai_ts(self):
        self.setup_models()
        param_value = request.args.get("q")
        session = self.session()
        query = session.query(self.PBMSQuanLyPhanLoaiTaiSan).filter_by(
            trang_thai_xoa=False
        )
        if param_value:
            query = query.filter(
                self.PBMSQuanLyPhanLoaiTaiSan.ten_loai_ts.ilike("%" + param_value + "%")
            )
        query = query.order_by(self.PBMSQuanLyPhanLoaiTaiSan.ngay_tao)
        jsonData = [
            {
                "id": item.id,
                "text": item.ten_loai_ts,
            }
            for item in query
        ]
        session.close()
        return jsonify({"result": jsonData})

    def get_all_param_by_loai_ts_id(self, id):
        self.setup_models()
        session = self.session()
        query = self.find_resource_loai_ts(id, session)
        jsonData = []
        if query.ds_tham_so:
            lstThamSoId = query.ds_tham_so.split(",")
            dbThamSos = (
                session.query(self.PBMSQuanLyThamSo, self.PBMSQuanLyNhomThamSo)
                .join(
                    self.PBMSQuanLyNhomThamSo,
                    self.PBMSQuanLyThamSo.nhom_tham_so_id
                    == self.PBMSQuanLyNhomThamSo.id,
                )
                .filter(
                    self.PBMSQuanLyThamSo.trang_thai_xoa == False,
                    self.PBMSQuanLyThamSo.id.in_(lstThamSoId),
                )
                .all()
            )

            jsonData = sorted(
                [
                    {
                        "id": tblThamSo.id,
                        "ma_truong": tblThamSo.ma_truong,
                        "ten_truong": tblThamSo.ten_truong,
                        "kieu_du_lieu": tblThamSo.kieu_du_lieu,
                        "mo_ta": tblThamSo.mo_ta,
                        "thu_tu_hien_thi": tblThamSo.thu_tu_hien_thi,
                        "nhom_tham_so_id": tblThamSo.nhom_tham_so_id,
                        "ten_nhom_tham_so": f"{tblNhomTS.thu_tu_hien_thi}.{tblNhomTS.ten_nhom}",
                        # Add other fields as necessary
                    }
                    for tblThamSo, tblNhomTS in dbThamSos
                ],
                key=lambda x: x["ten_nhom_tham_so"],
            )
        session.close()
        return jsonify(
            {
                "result": {
                    "id": query.id,
                    "ten_loai_ts": query.ten_loai_ts,
                    "params": jsonData,
                }
            }
        )

    def resources_for_index_query(self, search_text, session):
        pass
