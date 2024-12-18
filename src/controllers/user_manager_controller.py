import uuid
from flask import jsonify, request
from datetime import datetime, timezone
from .controller_v2 import ControllerV2
from services.auth_service import AuthService


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
            "/api/categories/user-manager/page",
            "get_data_by_page_user_manager",
            self.get_data_by_page_user_manager,
            methods=["POST"],
        )
        # get by id
        self.app.add_url_rule(
            "/api/categories/user-manager/detail/<id>",
            "get_by_id_user_manager",
            self.get_by_id_user_manager,
            methods=["GET"],
        )
        # create
        self.app.add_url_rule(
            "/api/categories/user-manager/create",
            "create_or_update_item_user_manager",
            self.create_or_update_item_user_manager,
            methods=["POST"],
        )
        # update
        self.app.add_url_rule(
            "/api/categories/user-manager/update/<id>",
            "create_or_update_item_user_manager",
            self.create_or_update_item_user_manager,
            methods=["PUT"],
        )
        # delete
        self.app.add_url_rule(
            "/api/categories/user-manager/delete/<id>",
            "remove_item_user_manager",
            self.remove_item_user_manager,
            methods=["DELETE"],
        )

    def get_data_by_page_user_manager(self):
        session = self.session()

        body_request = request.get_json()
        req_page = body_request["start"]
        req_size = body_request["length"]
        req_search = body_request["search"]
        req_order = body_request["order"]
        req_columns = body_request["columns"]

        query = session.query(self.User)
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
                self.User.ngay_tao.desc(),
            )

        # Phân trang
        data = query.limit(req_size).offset(req_page).all()
        count = query.count()
        jsonData = [
            {
                "id": t1.id,
                "username": t1.name,
                "full_name": t1.full_name,
                "email": t1.email,
                "chuc_vu_id": t1.chuc_vu_id,
                "ten_chuc_vu": "",
                "don_vi_id": t1.don_vi_id,
                "ten_don_vi": "",
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

    def get_by_id_user_manager(self, id):
        session = self.session()
        query = self.find_resource_user_manager(id, session)
        jsonData = {
            "id": query.id,
            "username": query.name,
            "full_name": query.full_name,
            "email": query.email,
            "chuc_vu_id": query.chuc_vu_id,
            "ten_chuc_vu": "",
            "don_vi_id": query.don_vi_id,
            "ten_don_vi": "",
            "ngay_tao": self.convertUTCDateToVNTime(query.ngay_tao),
        }
        session.close()
        return jsonify({"result": jsonData})

    def create_or_update_item_user_manager(self, id=None):
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
                obj = self.find_resource_user_manager(id, session)
                if obj is None:
                    return jsonify({"error": "Không tìm thấy bản ghi."}), 401
                obj.nguoi_sua = _authService.get_user_uuid(request)
                obj.ngay_sua = datetime.now(timezone.utc)

            obj.ma_user_manager = data["ma_user_manager"]
            obj.ten_user_manager = data["ten_user_manager"]
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

    def remove_item_user_manager(self, id):
        try:
            _authServices = AuthService()
            session = self.session()
            
            obj = self.find_resource_user_manager(id, session)
            if obj is None:
                return jsonify({"error": "Không tìm thấy bản ghi."}), 404
            
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

    def find_resource_user_manager(self, id, session):
        return session.query(self.User).filter_by(uuid=id).first()
