# HANDOFF — kamilovs-hotel-qr-backend

**Дата:** 2026-09-26 · **ПК:** «Камиловс»

## Статус: ПРИОСТАНОВЛЕН

Приём отзывов для QR-страницы отеля (`kamilovs-hotel-qr-frontend`). Страница выключена 2026-09-26,
поэтому и этот сервер больше не нужен. Код сохранён здесь, настройки Telegram-бота — в переменных окружения на Render.

## Сделано

- Страница для гостей (GitHub Pages) выключена.
- Сервер на Render (`kamilovs-hotel-qr-backend`, `srv-d527cdq4d50c73becdqg`, бесплатный тариф, Oregon)
  приостанавливается в панели Render: сервис → Settings → **Suspend Service**.

## Дальше (если понадобится включить снова)

1. Render → `kamilovs-hotel-qr-backend` → **Resume Service**.
2. Проверить https://kamilovs-hotel-qr-backend.onrender.com/health → `{"ok":true}`.
3. Включить страницу — см. HANDOFF.md в `kamilovs-hotel-qr-frontend`.
4. Перед повторным запуском: ограничить CORS адресом страницы (сейчас `*`) и добавить защиту от спама.

## Заметки

- Денег не тратил: бесплатный тариф Render.
- В репозитории лишняя папка `.idea` (не опасна).
