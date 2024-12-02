from datetime import datetime, timezone
import os
import uuid

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

        self.app.add_url_rule(
            "/api/public-building/categories/all",
            "get_categories_public_building",
            self.get_categories_public_building,
            methods=["GET"],
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

    def create_or_update_item_public_building(self, id=None):
        try:
            # Parse JSON data from the request
            data = request.form
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            if id is None:
                # create new
                obj = self.PBDMQuanLyNhaCongSan()
                obj.id = str(uuid.uuid4())
                # Từ số tờ, số thửa => tai_san_id
                checkSoTo = data.get('so_to')
                checkSoThua = data.get('so_thua')
                if checkSoTo and checkSoThua:
                    obj.tai_san_id = str(uuid.uuid4())
                # obj.nguoi_tao = userLogin.gext('id') or None
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.ngay_sua = datetime.now(timezone.utc)

            # update value tai_san_id
            obj.tai_san_id = self.getTaiSanIdBySoToAndSoThua(session, data.get('so_to'), data.get('so_thua'))
            print(f"TS: {obj.tai_san_id}")
            # Lấy dữ liệu tham số
            dsParamInDB = json.loads(data["body_params"])
            # Gán lại các giá trị vào bảng dữ liệu
            for item in dsParamInDB:
                if item['kieu_du_lieu'] == "string" or item['kieu_du_lieu'] == "textarea":
                    setattr(obj, item['ma_truong'], data.get(item['ma_truong']))

                elif item['kieu_du_lieu'] == "integer":
                    setattr(obj, item['ma_truong'], int(data.get(item['ma_truong'])) if data.get(item['ma_truong']) and data.get(item['ma_truong']) != '' else None)

                elif item['kieu_du_lieu'] == "float":
                    setattr(obj, item['ma_truong'], float(data.get(item['ma_truong'])) if data.get(item['ma_truong']) and data.get(item['ma_truong']) != '' else None)

                elif item['kieu_du_lieu'] == "date":
                    pass

                elif item['kieu_du_lieu'] == "file":
                    pass

            # for key, value in data.items():
            #     objField = dsParamInDB
            #     setattr(obj, key, value)

            session.commit()
            session.close()
            # Return a success response
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            # Handle exceptions and return an error response
            return jsonify({"error": str(e)}), 500

    def remove_item_public_building(self):
        pass

    def get_categories_public_building(self):
        # self.setup_models()
        # param_value = request.args.get("q")
        # session = self.session()
        # query = session.query(self.PBMSQuanLyPhanLoaiTaiSan).filter_by(
        #     trang_thai_xoa=False
        # )
        # if param_value:
        #     query = query.filter(
        #         self.PBMSQuanLyPhanLoaiTaiSan.ten_loai_ts.ilike("%" + param_value + "%")
        #     )
        # query = query.order_by(self.PBMSQuanLyPhanLoaiTaiSan.ngay_tao)
        # jsonData = [
        #     {
        #         "id": item.id,
        #         "text": item.ten_loai_ts,
        #     }
        #     for item in query
        # ]
        # session.close()
        # return jsonify({"result": jsonData})

        jsonData = [
            {
                "id": "NDCS-20224303233",
                "text": "NDCS-20224303233",
                "ten_ts": "Trường tiểu học An Khê",
                "dia_chi": "K245 Trường Chinh, phường An Khê, Thanh Khê, Đà Nẵng",
                "ma_to_thua": "30",
                "ma_to_dat": "32",
                "ds_file_dinh_kem": "",
                "ngay_tao": "25/11/2024 10:12",
            },
            {
                "id": "NDCS-20257336410",
                "text": "NDCS-20257336410",
                "ten_ts": "BQL chợ Nguyễn Tri Phương",
                "dia_chi": "KDC số 01 Nguyễn Tri Phương, phường Hòa Cường Bắc, Hải Châu, Đà Nẵng",
                "ma_to_thua": "33",
                "ma_to_dat": "64",
                "ds_file_dinh_kem": "",
                "ngay_tao": "12/10/2024 8:12",
            },
            {
                "id": "NDCS-202573256124",
                "text": "NDCS-202573256124",
                "ten_ts": "Trường tiểu học Núi Thành",
                "dia_chi": "Số 158 Ỷ Lan Nguyên Phi, phường Hòa Cường Bắc, Hải Châu, Đà Nẵng",
                "ma_to_thua": "32",
                "ma_to_dat": "561",
                "ds_file_dinh_kem": "",
                "ngay_tao": "02/11/2024 11:12",
            },
            {
                "id": "NDCS-20258687",
                "text": "NDCS-20258687",
                "ten_ts": "Trường THPT Nguyễn Hiền",
                "dia_chi": "Số 61 Phan Đăng Lưu, phường Hòa Cường Nam, Hải Châu, Đà Nẵng",
                "ma_to_thua": "6",
                "ma_to_dat": "7",
                "ds_file_dinh_kem": "",
                "ngay_tao": "25/11/2024 10:12",
            },
        ]

        return jsonify({"result": jsonData})

    def getTaiSanIdBySoToAndSoThua(self, session, soTo, soThua):
        if soTo and soThua:
            return (
                session.query(self.PBDMQuanLyNhaCongSan.tai_san_id)
                .filter_by(so_to=soTo, so_thua=soThua, trang_thai_xoa=False)
                .first()
            )
        else:
            return str(uuid.uuid4())