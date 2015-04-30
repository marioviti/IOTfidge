import hashlib
import os

def get_hash_salt(passwd):
	ret ={"hash": "", "salt":""} 
	i = 0
	salt = ""
	while i < 32:
		a = os.urandom(1)
		if a.isalnum():
			i = i + 1
			salt = salt + a
	ret['salt'] = salt
	hash_object = hashlib.sha256(salt+passwd)
	hex_dig = hash_object.hexdigest()
	ret['hash'] = hex_dig
	return ret

def hash_with_salt(salt,passwd):
	ret ={"hash": ""} 
	hash_object = hashlib.sha256(salt+passwd)
	hex_dig = hash_object.hexdigest()
	ret['hash'] = hex_dig
	return ret