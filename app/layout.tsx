import type { Metadata } from 'next';
export const metadata:Metadata={title:'Пчёлка · Карточки товаров',description:'Анализ фото, поиск сведений о продукте и готовые карточки для сайта.'};
export default function Layout({children}:{children:React.ReactNode}){return <html lang="ru"><body>{children}</body></html>}
