from datetime import datetime, timezone
import os
import uuid

from flask import json, jsonify, request

from .controller_v2 import ControllerV2


class PublicLandController(ControllerV2):

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(PublicLandController, self).__init__(
            "Danh sách thửa đất",
            "public-land",
            "public-land",
            "public_land",
            app,
            handler,
        )

        self.register_routes()

    def register_routes(self):
        # get data by page
        self.app.add_url_rule(
            "/api/public-land/page",
            "get_data_by_page_public_land",
            self.get_data_by_page_public_land,
            methods=["POST"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/public-land/detail/<id>",
            "get_by_id_loai_public_land",
            self.get_by_id_public_land,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/public-land/create",
            "create_or_update_item_public_land",
            self.create_or_update_item_public_land,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/public-land/update/<id>",
            "create_or_update_item_public_land",
            self.create_or_update_item_public_land,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/public-land/delete/<id>",
            "remove_item_public_land",
            self.remove_item_public_land,
            methods=["DELETE"],
        )

    # Hàm cho danh sách tham số
    def get_data_by_page_public_land(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        query = session.query(self.PBDMQuanLyDatCong).filter(
            self.PBDMQuanLyDatCong.trang_thai_xoa == False
        )
        # Nếu có giá trị search
        if req_search["value"]:
            query = query.filter(
                self.PBDMQuanLyDatCong.ma_dat.ilike("%%%s%%" % req_search["value"])
                | self.PBDMQuanLyDatCong.ten_dat.ilike("%%%s%%" % req_search["value"])
                | self.PBDMQuanLyDatCong.ten_tp.ilike("%%%s%%" % req_search["value"])
                | self.PBDMQuanLyDatCong.ten_qh.ilike("%%%s%%" % req_search["value"])
                | self.PBDMQuanLyDatCong.ten_px.ilike("%%%s%%" % req_search["value"])
                | self.PBDMQuanLyDatCong.dia_chi.ilike("%%%s%%" % req_search["value"])
            )

        # Sort
        if req_order:
            idx_col = req_order[0]["column"]
            val_col = req_columns[idx_col]["data"]
            val_dir = req_order[0]["dir"]
            if val_dir == "asc":
                query = query.order_by(getattr(self.PBDMQuanLyDatCong, val_col).asc())
            elif val_dir == "desc":
                query = query.order_by(getattr(self.PBDMQuanLyDatCong, val_col).desc())
        else:
            query = query.order_by(self.PBDMQuanLyDatCong.ngay_tao)

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        idDonViQuanLys = [item.don_vi_quan_ly_id for item in data]
        idHienTrangSDs = [item.hien_trang_sd_id for item in data]
        dataDonVi = (
            session.query(self.PBMSQuanLyDonVi)
            .filter(
                self.PBMSQuanLyDonVi.id.in_(idDonViQuanLys),
                self.PBMSQuanLyDonVi.trang_thai_xoa == False,
            )
            .all()
        )
        dataHTSD = (
            session.query(self.PBDMQuanLyDanhMuc)
            .filter(
                self.PBDMQuanLyDanhMuc.id.in_(idHienTrangSDs),
                self.PBDMQuanLyDanhMuc.trang_thai_xoa == False,
            )
            .all()
        )
        jsonData = [
            {
                "id": t1.id,
                "ma_dat": t1.ma_dat,
                "ten_dat": t1.ten_dat,
                "don_vi_quan_ly_id": t1.don_vi_quan_ly_id,
                "ten_don_vi_quan_ly": next((item.ten_dv for item in dataDonVi if item.id == t1.don_vi_quan_ly_id), ""),
                "hien_trang_sd_id": t1.hien_trang_sd_id,
                "ten_hien_trang_sd": next((item.ten_danh_muc for item in dataHTSD if item.id == t1.hien_trang_sd_id), ""),
                "so_to": t1.so_to,
                "so_thua": t1.so_thua,
                "dien_tich": t1.dien_tich,
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

    def create_or_update_item_public_land(self, id=None):
        try:
            # Parse JSON data from the request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            if id is None:
                # create new
                obj = self.PBDMQuanLyDatCong()
                obj.id = str(uuid.uuid4())
                # obj.nguoi_tao = userLogin.gext('id') or None
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource_public_land(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.ngay_sua = datetime.now(timezone.utc)

            obj.ma_dat = data["ma_dat"]
            obj.ten_dat = data["ten_dat"]
            obj.don_vi_quan_ly_id = data["don_vi_quan_ly_id"]
            obj.hien_trang_sd_id = data["hien_trang_sd_id"]
            obj.so_to = data["so_to"]
            obj.so_thua = data["so_thua"]
            obj.dien_tich = data["dien_tich"]
            obj.dia_chi = data["dia_chi"]
            obj.ma_px = data["ma_px"]
            obj.ten_px = data["ten_px"]
            obj.ma_qh = data["ma_qh"]
            obj.ten_qh = data["ten_qh"]
            obj.ma_tp = data["ma_tp"]
            obj.ten_tp = data["ten_tp"]
            obj.ds_file_dinh_kem = data["ds_file_dinh_kem"]

            session.commit()
            # self.update_config_timestamp(session)
            session.close()
            # Return a success response
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            # Handle exceptions and return an error response
            return jsonify({"error": str(e)}), 500

    def remove_item_public_land(self, id):
        try:
            session = self.session()
            # Find the group parameter by id
            obj = self.find_resource_public_land(id, session)
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

    def get_by_id_public_land(self, id):
        session = self.session()
        query = self.find_resource_public_land(id, session)
        jsonData = {
            "id": query.id,
            "ma_dat": query.ma_dat,
            "ten_dat": query.ten_dat,
            "don_vi_quan_ly_id": query.don_vi_quan_ly_id,
            "ten_don_vi_quan_ly": "",
            "hien_trang_sd_id": query.hien_trang_sd_id,
            "ten_hien_trang_sd": "",
            "so_to": query.so_to,
            "so_thua": query.so_thua,
            "dien_tich": query.dien_tich,
            "dia_chi": query.dia_chi,
            "ma_px": query.ma_px,
            "ten_px": query.ten_px,
            "ma_qh": query.ma_qh,
            "ten_qh": query.ten_qh,
            "ma_tp": query.ma_tp,
            "ten_tp": query.ten_tp,
            "ds_file_dinh_kem": query.ds_file_dinh_kem,
            "ngay_tao": self.convertUTCDateToVNTime(query.ngay_tao),
        }
        session.close()
        return jsonify({"result": jsonData})

    def find_resource_public_land(self, id, session):
        return (
            session.query(self.PBDMQuanLyDatCong)
            .filter_by(id=id, trang_thai_xoa=False)
            .first()
        )
