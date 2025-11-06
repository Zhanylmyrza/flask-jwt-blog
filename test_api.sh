# Регистрация нового пользователя
curl -X POST http://localhost:5000/api/users/register \
     -H "Content-Type: application/json" \
     -d '{"username": "test_user", "email": "user@example.com", "password": "password123"}'

# Вход и получение токена
curl -X POST http://localhost:5000/api/users/login \
     -H "Content-Type: application/json" \
     -d '{"username": "test_user", "password": "password123"}'

# Получение списка пользователей (с токеном)
curl -X GET http://localhost:5000/api/users \
     -H "Authorization: Bearer <your_token>"

# Создание поста (с токеном)
curl -X POST http://localhost:5000/api/posts \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_token>" \
     -d '{"title": "Test Post", "content": "This is a test post"}'