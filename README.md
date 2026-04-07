# FastAPI Test App

## Описание и бизнес-логика

Это тестовое приложение на **FastAPI**, демонстрирующее **гибкую RBAC-систему (Role-Based Access Control)** с JWT-аутентификацией.

Основная идея приложения — предоставить динамическую систему ролей и прав доступа, где доступ определяется не только ролью пользователя, но и **набором permissions для конкретных категорий ресурсов**.

---

## Основные сущности

### Users
Пользователи системы.

### Roles
Роли определяют набор permission-прав.

Примеры ролей:
- **Admin**
- **Manager**
- **User**

### Categories
Категории ресурсов приложения.

Например:
- users
- roles
- permissions
- products
- orders

### Permissions
Permissions связывают:

- **Role**
- **Category**
- набор действий

Каждый permission определяет, что конкретная роль может делать в определённой категории:

- `can_read`
- `can_create`
- `can_update`
- `can_delete`

Пример:
- роль **Manager**
- категория **products**
- может `read` и `update`
- не может `delete`

---

## Система аутентификации

- Используется **JWT Bearer Token**
- Пароли хранятся в виде **argon2 hash**
- После логина пользователь получает **access token**
- Токен используется для всех защищённых эндпоинтов через:

```http
Authorization: Bearer <token>
```

---

## Система авторизации (Policies)

Авторизация построена на **RBAC + Policies**.

### Как это работает
1. Пользователь логинится
2. JWT токен определяет пользователя
3. У пользователя есть одна или несколько ролей
4. У ролей есть permissions
5. Policy проверяет:
   - категорию ресурса
   - действие
   - наличие соответствующего permission

Пример проверки:

```python
policy.can_create("permissions")
policy.can_update("roles")
policy.can_read("categories")
```

---

## Seed данные

При запуске автоматически создаются тестовые пользователи:

| Email | Роль | Пароль |
|---|---|---|
| admin@example.com | admin | admin123 |
| manager@example.com | manager | manager123 |
| user@example.com | user | user123 |

---

## API возможности

### Users
- регистрация
- логин
- просмотр профиля

### Roles
- создание роли
- обновление роли
- удаление роли
- назначение роли пользователю
- отзыв роли у пользователя

### Categories
- CRUD категорий

### Permissions
- создание permission для role + category
- обновление прав
- удаление permission

---

## Запуск приложения

### Docker

```bash
docker-compose up --build
```

После запуска:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Авторизация в Swagger UI

1. Выполнить логин:

```http
POST /api/v1/sessions/login
```

```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

2. Скопировать `access_token`

3. Нажать **Authorize** в Swagger UI

4. Вставить:

```text
Bearer <your_token>
```

---

## Пример бизнес-логики

### Сценарий
Допустим есть:

- Role: `manager`
- Category: `products`

Permission:

```json
{
  "can_read": true,
  "can_create": false,
  "can_update": true,
  "can_delete": false
}
```

Это значит:

- manager может смотреть products
- manager может редактировать products
- manager не может создавать
- manager не может удалять
