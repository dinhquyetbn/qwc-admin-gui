import math
import os
import uuid
from datetime import datetime, timezone
from flask import render_template, jsonify, request
from .controller import Controller
from utils import i18n
from qwc_services_core.auth import get_identity


class AssetParametersController(Controller):

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(AssetParametersController, self).__init__(
            "Danh sách tham số tài sản",
            "asset-parameters",
            "asset-parameters",
            "asset_parameters",
            app,
            handler,
        )
        self.register_routes()

    def register_routes(self):
        # route tham số
        # get data by page
        self.app.add_url_rule(
            "/api/asset-parameter/param/page",
            "get_data_by_page_param",
            self.get_data_by_page_param,
            methods=["POST"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/asset-parameter/param/detail/<id>",
            "get_by_id_param",
            self.get_by_id_param,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/asset-parameter/param/create",
            "create_or_update_item_param",
            self.create_or_update_item_param,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/asset-parameter/param/update/<id>",
            "create_or_update_item_param",
            self.create_or_update_item_param,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/asset-parameter/param/delete/<id>",
            "remove_item_param",
            self.remove_item_param,
            methods=["DELETE"],
        )

        # route nhóm tham số
        # get data by page
        self.app.add_url_rule(
            "/api/asset-parameter/group/page",
            "get_data_by_page_group",
            self.get_data_by_page_group,
            methods=["POST"],
        )
        # get data for category
        self.app.add_url_rule(
            "/api/asset-parameter/group/all",
            "get_data_all_group",
            self.get_data_all_group,
            methods=["GET"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/asset-parameter/group/detail/<id>",
            "get_by_id_group",
            self.get_by_id_group,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/asset-parameter/group/create",
            "create_or_update_item_group",
            self.create_or_update_item_group,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/asset-parameter/group/update/<id>",
            "create_or_update_item_group",
            self.create_or_update_item_group,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/asset-parameter/group/delete/<id>",
            "remove_item_group",
            self.remove_item_group,
            methods=["DELETE"],
        )

    # Hàm cho danh sách tham số
    def get_data_by_page_param(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        query = session.query(self.PBMSQuanLyThamSo).filter_by(trang_thai_xoa=False)

        # Nếu có giá trị search
        if req_search["value"]:
            query = query.filter(
                self.PBMSQuanLyThamSo.ten_truong.ilike("%%%s%%" % req_search["value"])
            )

        # Sort
        if req_order:
            idx_col = req_order[0]["column"]
            val_col = req_columns[idx_col]["data"]
            val_dir = req_order[0]["dir"]
            if val_dir == "asc":
                query = query.order_by(getattr(self.PBMSQuanLyThamSo, val_col).asc())
            elif val_dir == "desc":
                query = query.order_by(getattr(self.PBMSQuanLyThamSo, val_col).desc())
        else:
            query = query.order_by(self.PBMSQuanLyThamSo.thu_tu_hien_thi)
        print(str(query.statement))
        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        jsonData = [
            {
                "id": item.id,
                "ten_nhom": item.ten_nhom,
                "thu_tu_hien_thi": item.thu_tu_hien_thi,
                "ngay_tao": self.convertUTCDateToVNTime(item.ngay_tao),
                # Add other fields as necessary
            }
            for item in data
        ]
        pagination = {
            "draw": int(body_request["draw"]),
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": jsonData,
        }
        session.close()

        return jsonify({"result": pagination})

    def create_or_update_item_param(self, id=None):
        try:
            # Parse JSON data from the request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            if id is None:
                # create new
                obj = self.PBMSQuanLyThamSo()
                obj.id = str(uuid.uuid4())
                # obj.nguoi_tao = userLogin.gext('id') or None
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401

            obj.ten_nhom = data["ten_nhom"]
            obj.thu_tu_hien_thi = data["thu_tu_hien_thi"]

            session.commit()
            # self.update_config_timestamp(session)
            session.close()
            # Return a success response
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            # Handle exceptions and return an error response
            return jsonify({"error": str(e)}), 500

    def remove_item_param(self, id):
        try:
            session = self.session()
            # Find the group parameter by id
            obj = self.find_resource_param(id, session)
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

    def get_by_id_param(self, id):
        session = self.session()
        query = self.find_resource_group(id, session)
        jsonData = {
            "id": query.id,
            "ten_nhom": query.ten_nhom,
            "thu_tu_hien_thi": query.thu_tu_hien_thi,
            "ngay_tao": self.convertUTCDateToVNTime(query.ngay_tao),
        }
        session.close()
        return jsonify({"result": jsonData})

    def find_resource_param(self, id, session):
        return (
            session.query(self.PBMSQuanLyThamSo)
            .filter_by(id=id, trang_thai_xoa=False)
            .first()
        )

    ###################################################################

    # Hàm cho danh sách nhóm tham số
    def get_data_by_page_group(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        query = session.query(self.PBMSQuanLyNhomThamSo).filter_by(trang_thai_xoa=False)

        # Nếu có giá trị search
        if req_search["value"]:
            query = query.filter(
                self.PBMSQuanLyNhomThamSo.ten_nhom.ilike("%%%s%%" % req_search["value"])
            )

        # Sort
        if req_order:
            idx_col = req_order[0]["column"]
            val_col = req_columns[idx_col]["data"]
            val_dir = req_order[0]["dir"]
            if val_dir == "asc":
                query = query.order_by(
                    getattr(self.PBMSQuanLyNhomThamSo, val_col).asc()
                )
            elif val_dir == "desc":
                query = query.order_by(
                    getattr(self.PBMSQuanLyNhomThamSo, val_col).desc()
                )
        else:
            query = query.order_by(self.PBMSQuanLyNhomThamSo.thu_tu_hien_thi)
        print(str(query.statement))
        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        jsonData = [
            {
                "id": item.id,
                "ten_nhom": item.ten_nhom,
                "thu_tu_hien_thi": item.thu_tu_hien_thi,
                "ngay_tao": self.convertUTCDateToVNTime(item.ngay_tao),
                # Add other fields as necessary
            }
            for item in data
        ]
        pagination = {
            "draw": int(body_request["draw"]),
            "recordsTotal": count,
            "recordsFiltered": count,
            "data": jsonData,
        }
        session.close()

        return jsonify({"result": pagination})

    def get_data_all_group(self):
        session = self.session()
        query = (
            session.query(self.PBMSQuanLyNhomThamSo)
            .filter_by(trang_thai_xoa=False)
            .order_by(self.PBMSQuanLyNhomThamSo.thu_tu_hien_thi)
        )
        jsonData = [
            {
                "id": item.id,
                "text": item.ten_nhom,
            }
            for item in query
        ]
        session.close()
        return jsonify({"result": jsonData})

    def create_or_update_item_group(self, id=None):
        try:
            # Parse JSON data from the request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            if id is None:
                # create new
                obj = self.PBMSQuanLyNhomThamSo()
                obj.id = str(uuid.uuid4())
                # obj.nguoi_tao = userLogin.gext('id') or None
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401

            obj.ten_nhom = data["ten_nhom"]
            obj.thu_tu_hien_thi = data["thu_tu_hien_thi"]

            session.commit()
            # self.update_config_timestamp(session)
            session.close()
            # Return a success response
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            # Handle exceptions and return an error response
            return jsonify({"error": str(e)}), 500

    def remove_item_group(self, id):
        try:
            session = self.session()
            # Find the group parameter by id
            obj = self.find_resource_group(id, session)
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

    def get_by_id_group(self, id):
        session = self.session()
        query = self.find_resource_group(id, session)
        jsonData = {
            "id": query.id,
            "ten_nhom": query.ten_nhom,
            "thu_tu_hien_thi": query.thu_tu_hien_thi,
            "ngay_tao": self.convertUTCDateToVNTime(query.ngay_tao),
        }
        session.close()
        return jsonify({"result": jsonData})

    def find_resource_group(self, id, session):
        return (
            session.query(self.PBMSQuanLyNhomThamSo)
            .filter_by(id=id, trang_thai_xoa=False)
            .first()
        )

    def resources_for_index_query(self, search_text, session):
        """Return query for roles list.

        :param str search_text: Search string for filtering
        :param Session session: DB session
        """
        query = (
            session.query(self.PBMSQuanLyNhomThamSo)
            .filter_by(trang_thai_xoa=False)
            .order_by(self.PBMSQuanLyNhomThamSo.thu_tu_hien_thi)
        )

        if search_text:
            query = query.filter(
                self.PBMSQuanLyNhomThamSo.ten_nhom.ilike("%%%s%%" % search_text)
            )

        return query
