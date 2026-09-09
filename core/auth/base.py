import hashlib
from pwdlib import PasswordHash
import jwt
from fastapi.security import OAuth2PasswordBearer

password_hasher = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")