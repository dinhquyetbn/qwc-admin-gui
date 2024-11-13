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
        # get data by page
        self.app.add_url_rule(
            "/api/asset-parameter/group/page",
            "get_data_by_page",
            self.get_data_by_page,
            methods=["POST"],
        )
        # create
        self.app.add_url_rule(
            "/api/asset-parameter/group/create",
            "create_or_update_group_params",
            self.create_or_update_group_params,
            methods=["POST"],
        )
        # delete
        self.app.add_url_rule(
            "/api/asset-parameter/group/delete/<id>",
            "delete_group_params",
            self.delete_group_params,
            methods=["DELETE"],
        )

    def get_data_by_page(self):
        session = self.session()
        query = (
            session.query(self.PBMSQuanLyNhomThamSo)
            .filter(self.PBMSQuanLyNhomThamSo.trang_thai_xoa == False)
            .order_by(self.PBMSQuanLyNhomThamSo.thu_tu_hien_thi)
        )
        data = query.all()
        jsonData = [
            {
                "id": item.id,
                "ten_nhom": item.ten_nhom,
                "thu_tu_hien_thi": item.thu_tu_hien_thi,
                "ngay_tao": self.convertUTCDateToVNTime(item.ngay_tao)
                # Add other fields as necessary
            }
            for item in data
        ]
        pagination = {
            "draw": 1,
            "recordsTotal": 4,
            "recordsFiltered": 4,
            "data": jsonData,
        }
        session.close()

        return jsonify({"result": pagination})

    def create_or_update_group_params(self):
        try:
            # Parse JSON data from the request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            if "id" not in data:
                # create new
                obj = self.PBMSQuanLyNhomThamSo()
                obj.id = str(uuid.uuid4())
                # obj.nguoi_tao = userLogin.gext('id') or None
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                pass

            obj.ten_nhom = data["ten_nhom"]
            obj.thu_tu_hien_thi = data["thu_tu_hien_thi"]

            session.commit()
            # self.update_config_timestamp(session)
            session.close()
            # Return a success response
            return jsonify({"message": "Thêm mới dữ liệu thành công."}), 201
        except Exception as e:
            # Handle exceptions and return an error response
            return jsonify({"error": str(e)}), 500
        
    def delete_group_params(self, id):
        try:
            session = self.session()
            # Find the group parameter by id
            obj = session.query(self.PBMSQuanLyNhomThamSo).get(id)
            if not obj:
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

    def resources_for_index_query(self, search_text, session):
        """Return query for roles list.

        :param str search_text: Search string for filtering
        :param Session session: DB session
        """
        query = (
            session.query(self.PBMSQuanLyNhomThamSo)
            .filter(self.PBMSQuanLyNhomThamSo.trang_thai_xoa == False)
            .order_by(self.PBMSQuanLyNhomThamSo.thu_tu_hien_thi)
        )

        if search_text:
            query = query.filter(
                self.PBMSQuanLyNhomThamSo.ten_nhom.ilike("%%%s%%" % search_text)
            )

        return query
