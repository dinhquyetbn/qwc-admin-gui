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
        return None
    
    def get_user_id(self, req):
        token = self.get_token_cookie(req)
        if token:
            decoded_token = decode_token(token)
            user_info = decoded_token.get("user_info")
            return user_info.get('id')
        return None