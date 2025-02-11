import hashlib

#Hashear la contraseña
def hashearContrasena(contrasena: str) -> str:
    return hashlib.sha256(contrasena.encode()).hexdigest()

#Comprobar la contraseña hasheada
def comprobarContrasena(contrasena: str, conHasheada: str) -> bool:
    return hashearContrasena(contrasena) == conHasheada
