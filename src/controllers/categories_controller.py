import os
import uuid

from datetime import datetime, timezone
from flask import json, jsonify, request
from .controller_v2 import ControllerV2


class CategoriesController(ControllerV2):
    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(CategoriesController, self).__init__(
            "Danh mục",
            "categories",
            "categories",
            "categories",
            app,
            handler,
        )
        self.register_routes()

    def register_routes(self):
        # Lấy danh sách tỉnh thành
        self.app.add_url_rule(
            "/api/categories/province",
            "get_category_province",
            self.get_category_province,
            methods=["GET"],
        )
        # Lấy danh sách quận huyện
        self.app.add_url_rule(
            "/api/categories/<provinceId>/district",
            "get_category_district",
            self.get_category_district,
            methods=["GET"],
        )
        # Lấy danh sách phường xã
        self.app.add_url_rule(
            "/api/categories/<provinceId>/<districtId>/ward",
            "get_category_ward",
            self.get_category_ward,
            methods=["GET"],
        )
        # Lấy danh sách danh mục theo mã nhóm
        self.app.add_url_rule(
            "/api/categories/<ma_nhom>/all",
            "get_category_by_ma_nhom",
            self.get_category_by_ma_nhom,
            methods=["GET"],
        )

    def get_category_province(self):
        self.setup_models()
        param_value = request.args.get("q")
        session = self.session()
        # Get dữ liệu đà nẵng
        query = session.query(self.PBDMDanhMucTinhThanh).filter_by(
            trang_thai_xoa=False, ma="48"
        )
        if param_value:
            query = query.filter(
                self.PBDMDanhMucTinhThanh.ten.ilike("%" + param_value + "%")
            )
        query = query.order_by(self.PBDMDanhMucTinhThanh.ten)
        jsonData = [
            {
                "id": item.ma,
                "text": item.ten,
            }
            for item in query
        ]
        session.close()
        return jsonify({"result": jsonData})

    def get_category_district(self, provinceId):
        self.setup_models()
        param_value = request.args.get("q")
        session = self.session()
        # Get dữ liệu đà nẵng
        query = session.query(self.PBDMDanhMucQuanHuyen).filter_by(
            trang_thai_xoa=False, ma_tp="48"
        )
        if param_value:
            query = query.filter(
                self.PBDMDanhMucQuanHuyen.ten.ilike("%" + param_value + "%")
            )
        query = query.order_by(self.PBDMDanhMucQuanHuyen.ten)
        jsonData = [
            {
                "id": item.ma,
                "text": item.ten,
            }
            for item in query
        ]
        session.close()
        return jsonify({"result": jsonData})

    def get_category_ward(self, provinceId, districtId):
        self.setup_models()
        param_value = request.args.get("q")
        session = self.session()
        # Get dữ liệu đà nẵng
        query = session.query(self.PBDMDanhMucPhuongXa).filter_by(
            trang_thai_xoa=False, ma_tp=provinceId, ma_qh=districtId
        )
        if param_value:
            query = query.filter(
                self.PBDMDanhMucPhuongXa.ten.ilike("%" + param_value + "%")
            )
        query = query.order_by(self.PBDMDanhMucPhuongXa.ten)
        jsonData = [
            {
                "id": item.ma,
                "text": item.ten,
            }
            for item in query
        ]
        session.close()
        return jsonify({"result": jsonData})

    def get_category_by_ma_nhom(self, ma_nhom):
        self.setup_models()
        param_value = request.args.get("q")
        session = self.session()
        # Get dữ liệu đà nẵng
        query = session.query(self.PBDMQuanLyDanhMuc).filter_by(
            trang_thai_xoa=False, ma_nhom=ma_nhom
        )
        if param_value:
            query = query.filter(
                self.PBDMQuanLyDanhMuc.ten_danh_muc.ilike("%" + param_value + "%")
            )
        query = query.order_by(self.PBDMQuanLyDanhMuc.ten_danh_muc)
        jsonData = [
            {
                "id": item.id,
                "text": item.ten_danh_muc,
            }
            for item in query
        ]
        session.close()
        return jsonify({"result": jsonData})
