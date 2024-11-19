import os
import uuid

from datetime import datetime, timezone
from flask import json, jsonify, request
from .controller_v2 import ControllerV2


class UnitsController(ControllerV2):

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(UnitsController, self).__init__(
            "Danh sách đơn vị",
            "units",
            "units",
            "units",
            app,
            handler,
        )
        self.register_routes()

    def register_routes(self):
        # get data by page
        self.app.add_url_rule(
            "/api/units/page",
            "get_data_by_page_unit",
            self.get_data_by_page_unit,
            methods=["POST"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/units/detail/<id>",
            "get_by_id_loai_unit",
            self.get_by_id_unit,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/units/create",
            "create_or_update_item_unit",
            self.create_or_update_item_unit,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/units/update/<id>",
            "create_or_update_item_unit",
            self.create_or_update_item_unit,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/units/delete/<id>",
            "remove_item_unit",
            self.remove_item_unit,
            methods=["DELETE"],
        )
        # get all
        self.app.add_url_rule(
            "/api/units/all",
            "get_all_unit",
            self.get_all_unit,
            methods=["GET"],
        )

    # Hàm cho danh sách tham số
    def get_data_by_page_unit(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        query = session.query(self.PBMSQuanLyDonVi).filter(
            self.PBMSQuanLyDonVi.trang_thai_xoa == False
        )
        # Nếu có giá trị search
        if req_search["value"]:
            query = query.filter(
                self.PBMSQuanLyDonVi.ten_dv.ilike("%%%s%%" % req_search["value"])
            )

        # Sort
        if req_order:
            idx_col = req_order[0]["column"]
            val_col = req_columns[idx_col]["data"]
            val_dir = req_order[0]["dir"]
            if val_dir == "asc":
                query = query.order_by(getattr(self.PBMSQuanLyDonVi, val_col).asc())
            elif val_dir == "desc":
                query = query.order_by(getattr(self.PBMSQuanLyDonVi, val_col).desc())
        else:
            query = query.order_by(self.PBMSQuanLyDonVi.ngay_tao)

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        jsonData = [
            {
                "id": tblUnit.id,
                "ma_dv": tblUnit.ma_dv,
                "ten_dv": tblUnit.ten_dv,
                "dia_chi": tblUnit.dia_chi,
                "ma_px": tblUnit.ma_px,
                "ten_px": tblUnit.ten_px,
                "ma_qh": tblUnit.ma_qh,
                "ten_qh": tblUnit.ten_qh,
                "ma_tp": tblUnit.ma_tp,
                "ten_tp": tblUnit.ten_tp,
                "don_vi_cap_cha_id": tblUnit.don_vi_cap_cha_id,
                "ten_don_vi_cap_cha": "",
                "sdt": tblUnit.sdt,
                "ngay_tao": self.convertUTCDateToVNTime(tblUnit.ngay_tao),
            }
            for tblUnit in data
        ]
        pagination = {
            "draw": int(body_request["draw"]),
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": jsonData,
        }
        session.close()
        return jsonify({"result": pagination})

    def create_or_update_item_unit(self, id=None):
        try:
            # Parse JSON data from the request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            if id is None:
                # create new
                obj = self.PBMSQuanLyDonVi()
                obj.id = str(uuid.uuid4())
                # obj.nguoi_tao = userLogin.gext('id') or None
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource_unit(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.ngay_sua = datetime.now(timezone.utc)

            obj.ma_dv = data["ma_dv"]
            obj.ten_dv = data["ten_dv"]
            obj.dia_chi = data["dia_chi"]
            obj.ma_px = data["ma_px"]
            obj.ten_px = data["ten_px"]
            obj.ma_qh = data["ma_qh"]
            obj.ten_qh = data["ten_qh"]
            obj.ma_tp = data["ma_tp"]
            obj.ten_tp = data["ten_tp"]
            obj.don_vi_cap_cha_id = data["don_vi_cap_cha_id"]
            obj.sdt = data["sdt"]

            session.commit()
            # self.update_config_timestamp(session)
            session.close()
            # Return a success response
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            # Handle exceptions and return an error response
            return jsonify({"error": str(e)}), 500

    def remove_item_unit(self, id):
        try:
            session = self.session()
            # Find the group parameter by id
            obj = self.find_resource_unit(id, session)
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

    def get_by_id_unit(self, id):
        session = self.session()
        query = self.find_resource_unit(id, session)
        jsonData = {
            "id": query.id,
            "ma_dv": query.ma_dv,
            "ten_dv": query.ten_dv,
            "dia_chi": query.dia_chi,
            "ma_px": query.ma_px,
            "ten_px": query.ten_px,
            "ma_qh": query.ma_qh,
            "ten_qh": query.ten_qh,
            "ma_tp": query.ma_tp,
            "ten_tp": query.ten_tp,
            "don_vi_cap_cha_id": query.don_vi_cap_cha_id,
            "ten_don_vi_cap_cha": "",
            "sdt": query.sdt,
            "ngay_tao": self.convertUTCDateToVNTime(query.ngay_tao),
        }
        session.close()
        return jsonify({"result": jsonData})

    def find_resource_unit(self, id, session):
        return (
            session.query(self.PBMSQuanLyDonVi)
            .filter_by(id=id, trang_thai_xoa=False)
            .first()
        )

    def get_all_unit(self):
        param_value = request.args.get("q")
        session = self.session()
        query = session.query(self.PBMSQuanLyDonVi).filter_by(trang_thai_xoa=False)
        if param_value:
            query = query.filter(
                self.PBMSQuanLyDonVi.ten_dv.ilike("%" + param_value + "%")
            )
        query = query.order_by(self.PBMSQuanLyDonVi.ten_dv)
        jsonData = [
            {
                "id": item.id,
                "text": item.ten_dv,
            }
            for item in query
        ]
        session.close()
        return jsonify({"result": jsonData})

    def resources_for_index_query(self, search_text, session):
        pass
