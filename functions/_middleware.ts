// Cloudflare Pages Functions middleware
// Этот файл нужен только если используете Pages Functions
// Для статического фронтенда можно удалить

export const onRequest: PagesFunction = async (context) => {
  return context.next();
};
