import math
import os
import uuid
from datetime import datetime, timezone
from flask import render_template, jsonify, request
from .controller_v2 import ControllerV2
from utils import i18n
from sqlalchemy import func, text
from qwc_services_core.auth import get_identity


class AssetParametersController(ControllerV2):

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
        # get category param by group
        self.app.add_url_rule(
            "/api/asset-parameter/group/category",
            "get_category_group_param",
            self.get_category_group_param,
            methods=["GET"],
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

        # query = session.query(self.PBMSQuanLyThamSo).filter_by(trang_thai_xoa=False)
        query = (
            session.query(self.PBMSQuanLyThamSo, self.PBMSQuanLyNhomThamSo)
            .join(
                self.PBMSQuanLyNhomThamSo,
                self.PBMSQuanLyThamSo.nhom_tham_so_id == self.PBMSQuanLyNhomThamSo.id,
            )
            .filter(self.PBMSQuanLyThamSo.trang_thai_xoa == False)
        )
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
            query = query.order_by(self.PBMSQuanLyThamSo.nhom_tham_so_id)

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        jsonData = [
            {
                "id": tblThamSo.id,
                "ma_truong": tblThamSo.ma_truong,
                "ten_truong": tblThamSo.ten_truong,
                "kieu_du_lieu": tblThamSo.kieu_du_lieu,
                "mo_ta": tblThamSo.mo_ta,
                "thu_tu_hien_thi": tblThamSo.thu_tu_hien_thi,
                "nhom_tham_so_id": tblThamSo.nhom_tham_so_id,
                "ten_nhom_tham_so": f"Nhóm: {tblNhomTS.ten_nhom} (TS: {self.getLoaiTS(tblNhomTS.loai_ts)})",
                "ngay_tao": self.convertUTCDateToVNTime(tblThamSo.ngay_tao),
                # Add other fields as necessary
            }
            for tblThamSo, tblNhomTS in data
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
                obj = self.find_resource_param(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.ngay_sua = datetime.now(timezone.utc)

            obj.ma_truong = data["ma_truong"]
            obj.ten_truong = data["ten_truong"]
            obj.kieu_du_lieu = data["kieu_du_lieu"]
            obj.nhom_tham_so_id = data["nhom_tham_so_id"]
            obj.mo_ta = data["mo_ta"]
            obj.thu_tu_hien_thi = data["thu_tu_hien_thi"]

            # Cập nhật cột dữ liệu vào bảng dữ liệu chính
            objNhomTS = self.find_resource_group(obj.nhom_tham_so_id, session)
            if objNhomTS:
                valLoaiTS = objNhomTS.loai_ts
                self.alterColumnForTable(valLoaiTS, obj.ma_truong, obj.kieu_du_lieu)
            else:
                return jsonify({"error": "Không tìm thấy bản ghi."}), 401

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
        query = self.find_resource_param(id, session)
        objGroupParam = self.find_resource_group(query.nhom_tham_so_id, session)
        ten_nhom_ts = objGroupParam.ten_nhom if objGroupParam else ""
        jsonData = {
            "id": query.id,
            "ma_truong": query.ma_truong,
            "ten_truong": query.ten_truong,
            "kieu_du_lieu": query.kieu_du_lieu,
            "mo_ta": query.mo_ta,
            "thu_tu_hien_thi": query.thu_tu_hien_thi,
            "nhom_tham_so_id": query.nhom_tham_so_id,
            "ten_nhom_tham_so": ten_nhom_ts,
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
        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        jsonData = [
            {
                "id": item.id,
                "loai_ts": f"TS: {self.getLoaiTS(item.loai_ts)}",
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
        param_value = request.args.get("q")
        session = self.session()
        query = session.query(self.PBMSQuanLyNhomThamSo).filter_by(trang_thai_xoa=False)
        if param_value:
            query = query.filter(
                self.PBMSQuanLyNhomThamSo.ten_nhom.ilike("%" + param_value + "%")
            )
        query = query.order_by(self.PBMSQuanLyNhomThamSo.thu_tu_hien_thi)
        jsonData = [
            {
                "id": item.id,
                "text": f"Nhóm: {item.ten_nhom} (TS: {self.getLoaiTS(item.loai_ts)})",
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
                obj = self.find_resource_group(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.ngay_sua = datetime.now(timezone.utc)

            obj.ten_nhom = data["ten_nhom"]
            obj.loai_ts = data["loai_ts"]
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
            "loai_ts": query.loai_ts,
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

    def get_category_group_param(self):
        self.setup_models()
        session = self.session()
        queryData = (
            session.query(
                self.PBMSQuanLyThamSo.nhom_tham_so_id,
                func.json_agg(
                    func.json_build_object(
                        "id",
                        self.PBMSQuanLyThamSo.id,
                        "text",
                        self.PBMSQuanLyThamSo.ten_truong,
                    )
                ).label(
                    "datas"
                ),  # Label the aggregated JSON array
            )
            .filter(self.PBMSQuanLyThamSo.trang_thai_xoa == False)
            .group_by(self.PBMSQuanLyThamSo.nhom_tham_so_id)
        )
        dataParam = queryData.all()

        queryGroup = (
            session.query(self.PBMSQuanLyNhomThamSo)
            .filter(self.PBMSQuanLyNhomThamSo.trang_thai_xoa == False)
            .order_by(self.PBMSQuanLyNhomThamSo.thu_tu_hien_thi)
        )
        dataGroup = queryGroup.all()

        jsonData = []
        for itemGroup in dataGroup:
            dsParam = [item[1] for item in dataParam if item[0] == itemGroup.id]
            dsParam = dsParam[0] if dsParam else []
            obj = {
                "id": itemGroup.id,
                "state": {"disabled": len(dsParam) == 0},
                "text": f"{itemGroup.ten_nhom} ({self.getLoaiTS(itemGroup.loai_ts)}) ({len(dsParam)})",
                "children": dsParam,
            }
            jsonData.append(obj)

        session.close()
        return jsonify({"result": jsonData})

    def resources_for_index_query(self, search_text, session):
        """Return query for roles list.

        :param str search_text: Search string for filtering
        :param Session session: DB session
        """
        # query = (
        #     session.query(self.PBMSQuanLyNhomThamSo)
        #     .filter_by(trang_thai_xoa=False)
        #     .order_by(self.PBMSQuanLyNhomThamSo.thu_tu_hien_thi)
        # )

        # if search_text:
        #     query = query.filter(
        #         self.PBMSQuanLyNhomThamSo.ten_nhom.ilike("%%%s%%" % search_text)
        #     )

        # return query
        pass

    def getLoaiTS(self, valLoaiTS=None):
        if valLoaiTS == "DAT_CS":
            return "Đất Công Sản"
        elif valLoaiTS == "NHA_CS":
            return "Nhà Công Sản"
        else:
            return None

    def getTypeColumnForTable(self, type):
        if type == "string" or type == "file" or type == "textarea":
            return "TEXT"
        elif type == "integer":
            return "INT8"
        elif type == "float":
            return "FLOAT"
        elif type == "date":
            return "DATE"

    def alterColumnForTable(self, loaiTS, fieldName, type):
        if type:
            session = self.session()
            try:
                convertType = self.getTypeColumnForTable(type)
                sql_query = ""
                if loaiTS == "NHA_CS":
                    sql_query = text(
                        f"ALTER TABLE qwc_config.pbms_quan_ly_nha_cong_san ADD COLUMN IF NOT EXISTS {fieldName} {convertType}"
                    )
                elif loaiTS == "DAT_CS":
                    sql_query = text(
                        f"ALTER TABLE qwc_config.pbms_quan_ly_dat_cong ADD COLUMN IF NOT EXISTS {fieldName} {convertType}"
                    )

                if sql_query is not None:
                    session.execute(sql_query)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
