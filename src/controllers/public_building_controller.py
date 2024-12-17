from datetime import datetime, timezone
import os
import uuid
from sqlalchemy import desc
from flask import json, jsonify, request
from services.upload_file_service import UploadFileService
from .controller_v2 import ControllerV2
from services.auth_service import AuthService


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

        # get history
        self.app.add_url_rule(
            "/api/public-building/history-edit/<id>",
            "get_history_edit_building",
            self.get_history_edit_building,
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
                | self.PBDMQuanLyNhaCongSan.ten_tai_san.ilike(
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
            query = query.order_by(desc(self.PBDMQuanLyNhaCongSan.ngay_tao))

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()

        jsonData = [
            {
                "id": t1.id,
                "tai_san_id": t1.tai_san_id,
                "tai_san_theo_chu_so_huu_id": t1.tai_san_theo_chu_so_huu_id,
                "ma_tai_san": t1.ma_tai_san,
                "ten_tai_san": t1.ten_tai_san,
                "phan_loai_tai_san_id": t1.phan_loai_tai_san_id,
                "so_to": t1.so_to,
                "so_thua": t1.so_thua,
                "full_dia_chi": (
                    f"{t1.dia_chi}, {t1.ten_px}, {t1.ten_qh}, {t1.ten_tp}"
                    if t1.dia_chi
                    else ""
                ),
                "ds_file_dinh_kem_info": t1.ds_file_dinh_kem,
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

    def get_by_id_public_building(self, id):
        self.setup_models()
        session = self.session()
        query = self.find_resource_public_building(id, session)

        jsonData = {
            "id": query.id,
            "ten_tp": query.ten_tp,
            "ten_qh": query.ten_qh,
            "ten_px": query.ten_px,
            # "phan_loai_tai_san_id": query.phan_loai_tai_san_id
        }

        # Get object phân loại sản phẩm
        objPhanLoaiTS = (
            session.query(self.PBMSQuanLyPhanLoaiTaiSan)
            .filter_by(id=query.phan_loai_tai_san_id, trang_thai_xoa=False)
            .first()
        )
        if objPhanLoaiTS.ds_tham_so:
            lstThamSoId = objPhanLoaiTS.ds_tham_so.split(",")
            dbThamSos = (
                session.query(self.PBMSQuanLyThamSo)
                .filter(
                    self.PBMSQuanLyThamSo.trang_thai_xoa == False,
                    self.PBMSQuanLyThamSo.id.in_(lstThamSoId),
                )
                .all()
            )
            for item in dbThamSos:
                if item.kieu_du_lieu == "date":
                    jsonData[item.ma_truong] = (
                        getattr(query, item.ma_truong).strftime("%d/%m/%Y")
                        if getattr(query, item.ma_truong)
                        else None
                    )
                if item.kieu_du_lieu == "file":
                    jsonData[f"{item.ma_truong}_info"] = getattr(query, item.ma_truong)
                else:
                    jsonData[item.ma_truong] = getattr(query, item.ma_truong)

        session.close()
        return jsonify({"result": jsonData})

    def create_or_update_item_public_building(self, id=None):
        try:
            _authService = AuthService()
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

                obj.nguoi_tao = _authService.get_user_uuid(request)
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource_public_building(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                # Convert object to dictionary before JSON serialization
                oldData = obj.__dict__.copy()
                obj.nguoi_sua = _authService.get_user_uuid(request)
                obj.ngay_sua = datetime.now(timezone.utc)

            # update value tai_san_id
            obj.tai_san_id = str(
                self.getTaiSanIdBySoToAndSoThua(data.get("so_to"), data.get("so_thua"))
            )
            obj.ten_tp = data.get("ten_tp")
            obj.ten_qh = data.get("ten_qh")
            obj.ten_px = data.get("ten_px")
            # Lấy dữ liệu tham số
            dsParamInDB = json.loads(data["body_params"])
            # Gán lại các giá trị vào bảng dữ liệu
            for item in dsParamInDB:
                if (
                    item["kieu_du_lieu"] == "string"
                    or item["kieu_du_lieu"] == "textarea"
                ):
                    setattr(obj, item["ma_truong"], data.get(item["ma_truong"]))

                elif item["kieu_du_lieu"] == "integer":
                    setattr(
                        obj,
                        item["ma_truong"],
                        (
                            int(data.get(item["ma_truong"]))
                            if data.get(item["ma_truong"])
                            and data.get(item["ma_truong"]) != ""
                            else None
                        ),
                    )

                elif item["kieu_du_lieu"] == "float":
                    setattr(
                        obj,
                        item["ma_truong"],
                        (
                            float(data.get(item["ma_truong"]))
                            if data.get(item["ma_truong"])
                            and data.get(item["ma_truong"]) != ""
                            else None
                        ),
                    )

                elif item["kieu_du_lieu"] == "date":
                    setattr(
                        obj,
                        item["ma_truong"],
                        (
                            datetime.strptime(data.get(item["ma_truong"]), "%d/%m/%Y")
                            if data.get(item["ma_truong"])
                            and data.get(item["ma_truong"]) != ""
                            else None
                        ),
                    )

                elif item["kieu_du_lieu"] == "file":
                    # Upload files
                    file_ma_truong = str(item["ma_truong"])
                    # Kiểm tra tồn tại file upload không
                    file_uploads = request.files.getlist(file_ma_truong)
                    # File dữ liệu cũ
                    file_news = []
                    file_olds = (
                        json.loads(data.get(f"{file_ma_truong}_info"))
                        if data.get(f"{file_ma_truong}_info") != ""
                        else []
                    )
                    if file_uploads and file_uploads.__len__() > 0:
                        uploadFileService = UploadFileService()
                        (saved_files, error_files) = (
                            uploadFileService.saveToMultipleFile(file_uploads)
                        )
                        if error_files and error_files.__len__() > 0:
                            return (
                                jsonify({"error": "File upload không thành công."}),
                                400,
                            )
                        if saved_files and saved_files.__len__() > 0:
                            # Gán danh sách file vào db
                            file_news = saved_files
                            for item in saved_files:
                                addFile = self.PBDMQuanLyFileDinhKem()
                                addFile.id = item["id"]
                                addFile.file_name = item["file_name"]
                                addFile.file_url = item["file_url"]
                                addFile.file_type = item["file_type"]
                                addFile.file_size = item["file_size"]
                                addFile.ngay_tao = datetime.now(timezone.utc)
                                session.add(addFile)
                    if id:
                        if file_news.__len__() > 0:
                            resultFile = json.dumps([*file_olds, *file_news])
                        else:
                            resultFile = json.dumps(file_olds)
                    else:
                        if file_news.__len__() > 0:
                            resultFile = json.dumps(file_news)
                        else:
                            resultFile = json.dumps([])
                    setattr(
                        obj,
                        file_ma_truong,
                        resultFile,
                    )

            # Nếu là update thì mới ghi vào bảng lịch sử
            if id:
                # TODO: Cập nhật lịch sử chỉnh sửa dữ liệu
                objLSChinhSua = self.PBDMLichSuChinhSuaNhaCS()
                objLSChinhSua.id = str(uuid.uuid4())
                objLSChinhSua.nha_cs_id = obj.id
                objLSChinhSua.ly_do_id = data.get("lyDoChinhSuaID")
                objLSChinhSua.ly_do_chinh_sua = data.get("lyDoChinhSuaTEXT")
                # TODO: Lấy ID tài khoản đăng nhập
                objLSChinhSua.nguoi_chinh_sua_id = _authService.get_user_uuid(request)
                objLSChinhSua.ngay_tao = datetime.now(timezone.utc)
                formatData = request.form.to_dict()
                formatData.pop("body_params")
                formatData.pop("lyDoChinhSuaID")
                formatData.pop("lyDoChinhSuaTEXT")
                oldData.pop("_sa_instance_state", None)
                newData = obj.__dict__.copy()
                newData.pop("_sa_instance_state", None)
                objLSChinhSua.du_lieu_cu = str(json.dumps(oldData))
                objLSChinhSua.du_lieu_moi = str(json.dumps(newData))
                session.add(objLSChinhSua)

            session.commit()
            session.close()
            # Return a success response
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            # Handle exceptions and return an error response
            return jsonify({"error": str(e)}), 500

    def remove_item_public_building(self, id):
        try:
            _authService = AuthService()
            session = self.session()
            # Find the group parameter by id
            obj = self.find_resource_public_building(id, session)
            if obj is None:
                return jsonify({"error": "Không tìm thấy bản ghi."}), 404

            # Mark as deleted
            obj.nguoi_xoa = _authService.get_user_uuid(request)
            obj.ngay_xoa = datetime.now(timezone.utc)
            obj.trang_thai_xoa = True
            session.commit()
            session.close()
            return jsonify({"message": "Xóa dữ liệu thành công."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def find_resource_public_building(self, id, session):
        return (
            session.query(self.PBDMQuanLyNhaCongSan)
            .filter_by(id=id, trang_thai_xoa=False)
            .first()
        )

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

    def getTaiSanIdBySoToAndSoThua(self, soTo, soThua):
        if soTo and soThua:
            session = self.session()
            valTaiSanID = (
                session.query(self.PBDMQuanLyNhaCongSan.tai_san_id)
                .filter(
                    self.PBDMQuanLyNhaCongSan.so_to == soTo,
                    self.PBDMQuanLyNhaCongSan.so_thua == soThua,
                    self.PBDMQuanLyNhaCongSan.trang_thai_xoa == False,
                )
                .first()
            )
            session.close()
            return valTaiSanID[0] if valTaiSanID else str(uuid.uuid4())
        else:
            return str(uuid.uuid4())

    def get_history_edit_building(self, id):
        session = self.session()
        query = (
            session.query(self.PBDMLichSuChinhSuaNhaCS)
            .filter_by(nha_cs_id=id, trang_thai_xoa=False)
            .order_by(desc(self.PBDMLichSuChinhSuaNhaCS.ngay_tao))
            .all()
        )
        arrNguoiChinhSuaId = [item.nguoi_chinh_sua_id for item in query]
        dbUsers = (
            session.query(self.User)
            .filter(self.User.uuid.in_(arrNguoiChinhSuaId))
            .all()
        )
        resJson = [
            {
                "nha_cs_id": item.nha_cs_id,
                "ly_do_chinh_sua": item.ly_do_chinh_sua,
                "nguoi_chinh_sua": [user.name for user in dbUsers if user.uuid == item.nguoi_chinh_sua_id],
                "du_lieu_cu": item.du_lieu_cu,
                "du_lieu_moi": item.du_lieu_moi,
                "ngay_tao": self.convertUTCDateToVNTime(item.ngay_tao),
            }
            for item in query
        ]
        session.close()
        return jsonify({"result": resJson})
