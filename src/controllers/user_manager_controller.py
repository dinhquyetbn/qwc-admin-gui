import uuid
from flask import json, jsonify, request
from datetime import datetime, timezone
from .controller_v2 import ControllerV2
from services.auth_service import AuthService
from services.encryption_service import EncryptionService

class UserManagerController(ControllerV2):

    def __init__(self, app, handler):
        """Constructor

        :param Flask app: Flask application
        :param handler: Tenant config handler
        """
        super(UserManagerController, self).__init__(
            "Danh sách người dùng",
            "user-manager",
            "user-manager",
            "user_manager",
            app,
            handler,
        )
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule(
            "/api/user-manager/page",
            "get_data_by_page_user_manager",
            self.get_data_by_page_user_manager,
            methods=["POST"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/user-manager/detail/<user_uuid>",
            "get_by_id_user_manager",
            self.get_by_id_user_manager,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/user-manager/create",
            "create_or_update_item_user_manager",
            self.create_or_update_item_user_manager,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/user-manager/update/<user_uuid>",
            "create_or_update_item_user_manager",
            self.create_or_update_item_user_manager,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/user-manager/delete/<user_uuid>",
            "remove_item_user_manager",
            self.remove_item_user_manager,
            methods=["DELETE"],
        )

    def check_exist_username(self, session, user_uuid, username): 
        obj = session.query(self.User).filter_by(name=username).first()
        status_exist = False
        if obj:
            print(obj.uuid)
            status_exist = obj.uuid != user_uuid
        return status_exist

    def get_data_by_page_user_manager(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        query = session.query(self.User).filter(self.User.name != 'admin')
        # Nếu có giá trị search
        if req_search["value"]:
            query = query.filter(
                self.User.name.ilike("%%%s%%" % req_search["value"])
                | self.User.full_name.ilike("%%%s%%" % req_search["value"])
                | self.User.email.ilike("%%%s%%" % req_search["value"])
            )

        # Sort
        if req_order:
            idx_col = req_order[0]["column"]
            val_col = req_columns[idx_col]["data"]
            val_dir = req_order[0]["dir"]
            if val_dir == "asc":
                query = query.order_by(getattr(self.User, val_col).asc())
            elif val_dir == "desc":
                query = query.order_by(getattr(self.User, val_col).desc())
        else:
            query = query.order_by(
                self.User.don_vi_id.desc(),
            )

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()

        dsChucVuId = [item.chuc_vu_id for item in data]
        dbChucVus = (
            session.query(self.PBDMQuanLyChucVu)
            .filter(
                self.PBDMQuanLyChucVu.id.in_(dsChucVuId),
                self.PBDMQuanLyChucVu.trang_thai_xoa == False,
            )
            .all()
        )

        dsDonViId = [item.don_vi_id for item in data]
        dbDonVis = (
            session.query(self.PBMSQuanLyDonVi)
            .filter(
                self.PBMSQuanLyDonVi.id.in_(dsDonViId),
                self.PBMSQuanLyDonVi.trang_thai_xoa == False,
            )
            .all()
        )

        jsonData = [
            {
                "id": t1.id,
                "uuid": t1.uuid,
                "username": t1.name,
                "full_name": t1.full_name,
                "email": t1.email,
                "chuc_vu_id": t1.chuc_vu_id,
                "ten_chuc_vu": next((item.ten_chuc_vu for item in dbChucVus if item.id == t1.chuc_vu_id), None),
                "don_vi_id": t1.don_vi_id,
                "ten_don_vi": next((item.ten_dv for item in dbDonVis if item.id == t1.don_vi_id), None),
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

    def get_by_id_user_manager(self, user_uuid):
        session = self.session()
        query = self.find_resource_user_manager(user_uuid, session)

        dbChucVu = (
            session.query(self.PBDMQuanLyChucVu)
            .filter(
                self.PBDMQuanLyChucVu.id == query.chuc_vu_id,
                self.PBDMQuanLyChucVu.trang_thai_xoa == False,
            )
            .first()
        )

        dbDonVi = (
            session.query(self.PBMSQuanLyDonVi)
            .filter(
                self.PBMSQuanLyDonVi.id == query.don_vi_id,
                self.PBMSQuanLyDonVi.trang_thai_xoa == False,
            )
            .first()
        )

        dbUserRoles = session.query(self.Role).join(self.Role.users_collection).filter(self.User.name == query.name).all()

        jsonData = {
            "id": query.id,
            "uuid": query.uuid,
            "username": query.name,
            "full_name": query.full_name,
            "email": query.email,
            "sdt": query.sdt,
            "tai_khoan_cap": query.tai_khoan_cap,
            "chuc_vu_id": query.chuc_vu_id,
            "ten_chuc_vu": dbChucVu.ten_chuc_vu if dbChucVu else None,
            "don_vi_id": query.don_vi_id,
            "ten_don_vi": dbDonVi.ten_dv if dbDonVi else None,
            "is_active": query.is_active,
            "acc_ke_khai": query.acc_ke_khai,
            "acc_phe_duyet": query.acc_phe_duyet,
            "roles": [{"id": item.id, "name": item.txt_name} for item in dbUserRoles],
            "ngay_tao": self.convertUTCDateToVNTime(query.ngay_tao),
        }
        session.close()
        return jsonify({"result": jsonData})

    def create_or_update_item_user_manager(self, user_uuid=None):
        try:
            _authService = AuthService()
            _encryptionService = EncryptionService()
            # Parse JSON data from the request
            data = request.get_json()
            if not data:
                return jsonify({"error": "Dữ liệu không hợp lệ."}), 400

            # create and commit
            session = self.session()

            # check exist username
            is_username = self.check_exist_username(session, user_uuid, data['username'])
            if is_username:
                return jsonify({"error": "Tên đăng nhập đã tồn tại."}), 400

            if user_uuid is None:
                # create new
                obj = self.User()
                obj.uuid = str(uuid.uuid4())
                obj.nguoi_tao = _authService.get_user_uuid(request)
                obj.ngay_tao = datetime.now(timezone.utc)
                session.add(obj)
            else:
                # update existing
                obj = self.find_resource_user_manager(user_uuid, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.nguoi_sua = _authService.get_user_uuid(request)
                obj.ngay_sua = datetime.now(timezone.utc)
                
            # Nếu tồn tại password thì generate
            if data['password'].strip():
                obj.set_password(data['password'].strip())

            obj.name = data["username"]
            obj.full_name = data["full_name"]
            obj.email = data["email"]
            obj.sdt = data["sdt"]
            obj.chuc_vu_id = data["chuc_vu_id"]
            obj.don_vi_id = data["don_vi_id"]
            obj.is_active = data["is_active"]
            obj.acc_ke_khai = data["acc_ke_khai"]
            obj.acc_phe_duyet = data["acc_phe_duyet"]
            obj.tai_khoan_cap = int(data["tai_khoan_cap"] if data["tai_khoan_cap"] else 1)
            session.flush()  # Get obj.id when create new

            # Lưu lại trạng thái mật khẩu
            if data['password'].strip():
                password_history = self.PasswordHistory()
                password_history.user_id = obj.id
                password_history.password_hash = obj.password_hash
                password_history.created_at = datetime.now(timezone.utc)
                password_history.pass_hash = _encryptionService.encode_text(data['password'].strip())
                session.add(password_history)

            # update users roles
            self.update_collection(
                obj.roles_collection, data['role_ids'], self.Role, 'id', session
            )

            session.commit()
            session.close()
            return jsonify({"message": "Cập nhật dữ liệu thành công."}), 201
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def remove_item_user_manager(self, user_uuid):
        try:
            _authService = AuthService()
            # Check quyền tài khoản được phép xóa
            if not _authService.isAccess(request):
                return jsonify({"error": "Tài khoản không có quyền sử dụng chức năng này."}), 400
            session = self.session()
            obj = self.find_resource_user_manager(user_uuid, session)
            if obj is None:
                return jsonify({"error": "Không tìm thấy bản ghi."}), 404
            
            # Lưu lại trạng thái user bị xóa
            objUserRemoved = self.UserRemoved()
            objUserRemoved.id = str(uuid.uuid4())
            objUserRemoved.user_id = user_uuid
            userOld = obj.__dict__.copy()
            userOld.pop("_sa_instance_state", None)
            objUserRemoved.user_info = str(json.dumps(userOld))
            objUserRemoved.nguoi_tao = _authService.get_user_uuid(request)
            objUserRemoved.ngay_tao = datetime.now(timezone.utc)
            session.add(objUserRemoved)

            session.delete(obj)
            session.commit()
            return jsonify({"message": "Xóa dữ liệu thành công."}), 200
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def find_resource_user_manager(self, user_uuid, session):
        return session.query(self.User).filter_by(uuid=user_uuid).first()
