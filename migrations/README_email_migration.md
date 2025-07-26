# Migración: Añadir Columna Email a Usuarios

## 📝 Descripción
Esta migración añade la columna `email` a la tabla `users` para permitir el almacenamiento de correos electrónicos de usuarios.

## 🔄 Cambios Realizados

### Base de Datos
- ✅ Añadida columna `email VARCHAR(255) NULL` después de `username`
- ✅ Añadida restricción `UNIQUE KEY unique_email` para evitar emails duplicados
- ✅ Actualizados algunos registros de ejemplo con emails

### Código
- ✅ Modelo `UserModel` ya tenía el campo `email`
- ✅ Añadidos DTOs para manejo de usuarios con email:
  - `UserCreateRequest`
  - `UserUpdateRequest` 
  - `UserResponse`

## 📊 Estructura Final de la Tabla

```sql
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `sexo` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `unique_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
```

## 🚀 Cómo Usar

### Crear Usuario con Email
```python
from models.dto import UserCreateRequest

user_data = UserCreateRequest(
    username="nuevo.usuario",
    email="nuevo.usuario@example.com",
    password="password123",
    birth_date="1990-01-01",
    sexo="M"
)
```

### Actualizar Email de Usuario
```sql
UPDATE users SET email = 'nuevo.email@example.com' WHERE id = 1;
```

## 🔙 Rollback
Para revertir esta migración:

```sql
ALTER TABLE `users` DROP KEY `unique_email`;
ALTER TABLE `users` DROP COLUMN `email`;
```

## 📂 Archivos Modificados
- `/migrations/001_add_email_to_users.sql` - Script de migración
- `/app/models/dto.py` - Añadidos DTOs para usuarios
- `/add_email_column.sql` - Script completo con datos de ejemplo

## ✅ Verificación
```sql
-- Verificar estructura
DESCRIBE users;

-- Verificar datos
SELECT id, username, email FROM users LIMIT 5;
```
