from flask_jwt_extended import decode_token

class AuthService:
    def __init__(self):
        pass

    def get_token_cookie(self, req):
        token = req.cookies.get('access_token_cookie')
        if not token:
            return None
        return token
    
    def get_userinfo(self, req):
        token = self.get_token_cookie(req)
        if token:
            decoded_token = decode_token(token)
            user_info = decoded_token.get("user_info")
            return user_info
        return None
    
    def get_user_uuid(self, req):
        token = self.get_token_cookie(req)
        if token:
            decoded_token = decode_token(token)
            user_info = decoded_token.get("user_info")
            return user_info.get('uuid')
        return 'dev'
    
    def get_user_id(self, req):
        token = self.get_token_cookie(req)
        if token:
            decoded_token = decode_token(token)
            user_info = decoded_token.get("user_info")
            return user_info.get('id')
        return None
    
    def isAccess(self, req):
        token = self.get_token_cookie(req)
        if token:
            decoded_token = decode_token(token)
            user_roles = decoded_token.get("roles")
            role_level = decoded_token.get("tai_khoan_cap")
            if "admin" in user_roles:
                return True
            else:
                # Từ cấp UBND Quận mới có thể thực hiện cập nhật tài khoản cấp 1
                if role_level >= 2:
                    return True
        return False