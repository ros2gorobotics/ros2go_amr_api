from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

import config

# กำหนดชื่อ Header ที่ Client ต้องแนบมา
API_KEY_NAME = "X-API-Key"

# สร้างตัวรับค่าจาก Header
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key_header: str = Security(api_key_header)):
    """
    ฟังก์ชันตรวจสอบว่า API Key ที่ส่งมาตรงกับใน config.py หรือไม่
    """
    if api_key_header == config.SECRET_API_KEY:
        return api_key_header
    
    # ถ้าไม่ตรง หรือไม่ได้แนบมา ให้เตะออกด้วย Status 403 Forbidden
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate API Key. Unauthorized access."
    )