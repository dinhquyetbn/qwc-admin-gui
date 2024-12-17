import os
import uuid

from datetime import datetime, timezone
from flask import json, jsonify, request
from .controller_v2 import ControllerV2
from sqlalchemy import desc
from services.auth_service import AuthService


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

        # Nhóm danh mục
        self.app.add_url_rule(
            "/api/categories/nhom-danh-muc/all",
            "get_data_all_nhom_danh_muc",
            self.get_data_all_nhom_danh_muc,
            methods=["GET"],
        )
        self.app.add_url_rule(
            "/api/categories/nhom-danh-muc/page",
            "get_data_by_page_nhom_danh_muc",
            self.get_data_by_page_nhom_danh_muc,
            methods=["POST"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/categories/nhom-danh-muc/detail/<id>",
            "get_by_id_nhom_danh_muc",
            self.get_by_id_nhom_danh_muc,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/categories/nhom-danh-muc/create",
            "create_or_update_item_nhom_danh_muc",
            self.create_or_update_item_nhom_danh_muc,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/categories/nhom-danh-muc/update/<id>",
            "create_or_update_item_nhom_danh_muc",
            self.create_or_update_item_nhom_danh_muc,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/categories/nhom-danh-muc/delete/<id>",
            "remove_item_nhom_danh_muc",
            self.remove_item_nhom_danh_muc,
            methods=["DELETE"],
        )
        # Danh mục
        self.app.add_url_rule(
            "/api/categories/danh-muc/page",
            "get_data_by_page_danh_muc",
            self.get_data_by_page_danh_muc,
            methods=["POST"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/categories/danh-muc/detail/<id>",
            "get_by_id_danh_muc",
            self.get_by_id_danh_muc,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/categories/danh-muc/create",
            "create_or_update_item_danh_muc",
            self.create_or_update_item_danh_muc,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/categories/danh-muc/update/<id>",
            "create_or_update_item_danh_muc",
            self.create_or_update_item_danh_muc,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/categories/danh-muc/delete/<id>",
            "remove_item_danh_muc",
            self.remove_item_danh_muc,
            methods=["DELETE"],
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
        query = query.order_by(self.PBDMDanhMucTinhThanh.ten).all()
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
        query = query.order_by(self.PBDMDanhMucQuanHuyen.ten).all()
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
        query = query.order_by(self.PBDMDanhMucPhuongXa.ten).all()
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
        query = query.order_by(self.PBDMQuanLyDanhMuc.ten_danh_muc).all()
        jsonData = [
            {
                "id": item.id,
                "text": item.ten_danh_muc,
            }
            for item in query
        ]
        session.close()
        return jsonify({"result": jsonData})

    def get_data_by_page_danh_muc(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        query = session.query(self.PBDMQuanLyDanhMuc).filter(
            self.PBDMQuanLyDanhMuc.trang_thai_xoa == False
        )
        # Nếu có giá trị search
        if req_search["value"]:
            query = query.filter(
                self.PBDMQuanLyDanhMuc.ma_danh_muc.ilike("%%%s%%" % req_search["value"])
                | self.PBDMQuanLyDanhMuc.ten_danh_muc.ilike(
                    "%%%s%%" % req_search["value"]
                )
            )

        # Sort
        if req_order:
            idx_col = req_order[0]["column"]
            val_col = req_columns[idx_col]["data"]
            val_dir = req_order[0]["dir"]
            if val_dir == "asc":
                query = query.order_by(getattr(self.PBDMQuanLyDanhMuc, val_col).asc())
            elif val_dir == "desc":
                query = query.order_by(getattr(self.PBDMQuanLyDanhMuc, val_col).desc())
        else:
            query = query.order_by(desc(self.PBDMQuanLyDanhMuc.ngay_tao))

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        jsonData = [
            {
                "id": t1.id,
                "ma_danh_muc": t1.ma_danh_muc,
                "ten_danh_muc": t1.ten_danh_muc,
                "ma_nhom": t1.ma_nhom,
                "ten_nhom": t1.ten_nhom,
                "group_nhom": f"{t1.ma_nhom} - {t1.ten_nhom}",
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

    def get_by_id_danh_muc(self, id):
        session = self.session()
        query = self.find_resource_danh_muc(id, session)
        jsonData = {
            "id": query.id,
            "ma_danh_muc": query.ma_danh_muc,
            "ten_danh_muc": query.ten_danh_muc,
            "ma_nhom": query.ma_nhom,
            "ten_nhom": query.ten_nhom,            
            "ngay_tao": self.convertUTCDateToVNTime(query.ngay_tao),
        }
        session.close()
        return jsonify({"result": jsonData})

    def create_or_update_item_danh_muc(self, id=None):
        try:
            _authService = AuthService()
            # Parse JSON data from the request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            if id is None:
                # create new
                obj = self.PBDMQuanLyDanhMuc()
                obj.id = str(uuid.uuid4())
                obj.nguoi_tao = _authService.get_user_uuid(request)
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource_danh_muc(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.nguoi_sua = _authService.get_user_uuid(request)
                obj.ngay_sua = datetime.now(timezone.utc)

            obj.ma_danh_muc = data["ma_danh_muc"]
            obj.ten_danh_muc = data["ten_danh_muc"]
            obj.ma_nhom = data["ma_nhom"]
            obj.ten_nhom = data["ten_nhom"]

            session.commit()
            # self.update_config_timestamp(session)
            session.close()
            # Return a success response
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_item_danh_muc(self, id):
        try:
            _authServices = AuthService()
            session = self.session()
            # Find the group parameter by id
            obj = self.find_resource_danh_muc(id, session)
            if obj is None:
                return jsonify({"error": "Không tìm thấy bản ghi."}), 404

            # Mark as deleted
            obj.nguoi_xoa = _authServices.get_user_uuid(request)
            obj.ngay_xoa = datetime.now(timezone.utc)
            obj.trang_thai_xoa = True
            session.commit()
            return jsonify({"message": "Xóa dữ liệu thành công."}), 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def find_resource_danh_muc(self, id, session):
        return (
            session.query(self.PBDMQuanLyNhomDanhMuc)
            .filter_by(id=id, trang_thai_xoa=False)
            .first()
        )

    def get_data_by_page_nhom_danh_muc(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        query = session.query(self.PBDMQuanLyNhomDanhMuc).filter(
            self.PBDMQuanLyNhomDanhMuc.trang_thai_xoa == False
        )
        # Nếu có giá trị search
        if req_search["value"]:
            query = query.filter(
                self.PBDMQuanLyNhomDanhMuc.ten_nhom.ilike(
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
                    getattr(self.PBDMQuanLyNhomDanhMuc, val_col).asc()
                )
            elif val_dir == "desc":
                query = query.order_by(
                    getattr(self.PBDMQuanLyNhomDanhMuc, val_col).desc()
                )
        else:
            query = query.order_by(desc(self.PBDMQuanLyNhomDanhMuc.ngay_tao))

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        jsonData = [
            {
                "id": t1.id,
                "ma_nhom": t1.ma_nhom,
                "ten_nhom": t1.ten_nhom,
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

    def get_data_all_nhom_danh_muc(self): 
        self.setup_models()
        param_value = request.args.get("q")
        session = self.session()
        query = session.query(self.PBDMQuanLyNhomDanhMuc).filter(
            self.PBDMQuanLyNhomDanhMuc.trang_thai_xoa == False
        )
        
        if param_value:
            query = query.filter(
                self.PBDMQuanLyNhomDanhMuc.ten_nhom.ilike("%" + param_value + "%")
            )

        query = query.order_by(desc(self.PBDMQuanLyNhomDanhMuc.ngay_tao)).all()

        jsonData = [
            {
                "id": item.ma_nhom,
                "text": item.ten_nhom,
            }
            for item in query
        ]

        session.close()
        return jsonify({"result": jsonData})

    def get_by_id_nhom_danh_muc(self, id):
        session = self.session()
        query = self.find_resource_nhom_danh_muc(id, session)
        jsonData = {
            "id": query.id,
            "ten_nhom": query.ten_nhom,
            "ma_nhom": query.ma_nhom,
            "ngay_tao": self.convertUTCDateToVNTime(query.ngay_tao),
        }
        session.close()
        return jsonify({"result": jsonData})

    def create_or_update_item_nhom_danh_muc(self, id=None):
        try:
            _authService = AuthService()
            # Parse JSON data from the request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            if id is None:
                # create new
                obj = self.PBDMQuanLyNhomDanhMuc()
                obj.id = str(uuid.uuid4())
                obj.nguoi_tao = _authService.get_user_uuid(request)
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource_nhom_danh_muc(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.nguoi_sua = _authService.get_user_uuid(request)
                obj.ngay_sua = datetime.now(timezone.utc)

            obj.ma_nhom = data["ma_nhom"]
            obj.ten_nhom = data["ten_nhom"]

            session.commit()
            # self.update_config_timestamp(session)
            session.close()
            # Return a success response
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_item_nhom_danh_muc(self, id):
        try:
            _authServices = AuthService()
            session = self.session()
            # Find the group parameter by id
            obj = self.find_resource_nhom_danh_muc(id, session)
            if obj is None:
                return jsonify({"error": "Không tìm thấy bản ghi."}), 404

            # Mark as deleted
            obj.nguoi_xoa = _authServices.get_user_uuid(request)
            obj.ngay_xoa = datetime.now(timezone.utc)
            obj.trang_thai_xoa = True
            session.commit()
            return jsonify({"message": "Xóa dữ liệu thành công."}), 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def find_resource_nhom_danh_muc(self, id, session):
        return (
            session.query(self.PBDMQuanLyNhomDanhMuc)
            .filter_by(id=id, trang_thai_xoa=False)
            .first()
        )
