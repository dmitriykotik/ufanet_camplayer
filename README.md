# ufanet_camplayer
Программа для воспроизведения камер сайта maps.ufanet.ru с автоматическим обновлением токенов доступа.

# Превью
<img width="1920" height="1037" alt="image (16)" src="https://github.com/user-attachments/assets/129eb03a-c124-4723-a669-9cf896e79a7c" />

<img width="1920" height="1038" alt="image (17)" src="https://github.com/user-attachments/assets/9b6479fd-1a6c-4979-9b73-4c99e1d9f9e9" />

# Инструкция
- Зайдите на сайт maps.ufanet.ru.
- Выберите любую камеру.

<img width="480" height="460" alt="image (18)" src="https://github.com/user-attachments/assets/8413ce51-7ca5-43ce-82ab-c1e24ca257dd" />

- Скопируйте ссылку камеры.

<img width="525" height="48" alt="image" src="https://github.com/user-attachments/assets/d6630c1a-8652-4895-90b3-575696d72730" />

- Откройте файл `main.py` и вставьте эту ссылку в переменную `MAPS_URL`.
- Готово. Теперь откройте файл `start.bat` или `start.sh`.
- Также по желанию можно настроить разрешение окна при запуске в переменной `RESOLUTION` или переодичность получения нового токена в переменной `TOKEN_REFRESH_INTERVAL` (В секундах).

Код сам подберёт ip для получения потока стрима видеокамеры, а также сам будет автоматически обновлять токен доступа с переодичностью в 3 минуты (По умолчанию).

ПРОГРАММА СОЗДАНА ИСКЛЮЧИТЕЛЬНО В ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЯХ.
