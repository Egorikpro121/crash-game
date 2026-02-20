# Crash Game Frontend

Frontend приложение для Telegram Mini App Crash Game с идеальной дизайн-системой в стиле неоморфизм.

## Технологии

- **React 18** - UI библиотека
- **TypeScript** - Типизация
- **Styled Components** - CSS-in-JS
- **Vite** - Сборщик
- **React Router** - Маршрутизация
- **Framer Motion** - Анимации

## Структура проекта

```
frontend/
├── src/
│   ├── design-system/     # Дизайн-система
│   │   ├── tokens/        # Design tokens
│   │   ├── foundations/   # Базовые стили
│   │   ├── components/    # Базовые компоненты
│   │   ├── animations/    # Анимации
│   │   ├── utilities/     # Утилиты
│   │   └── icons/         # Иконки
│   ├── components/        # Компоненты приложения
│   ├── pages/            # Страницы
│   └── styles/           # Глобальные стили
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Установка

```bash
cd frontend
npm install
```

## Запуск

```bash
npm run dev
```

## Сборка

```bash
npm run build
```

## Дизайн-система

Дизайн-система построена на принципах неоморфизма с темной темой. Все компоненты используют единые токены для цветов, типографики, spacing и теней.

### Использование компонентов

```tsx
import { Button, Card, Input } from '@/design-system';

function App() {
  return (
    <Card>
      <Input label="Amount" />
      <Button variant="primary">Submit</Button>
    </Card>
  );
}
```

## Лицензия

MIT
