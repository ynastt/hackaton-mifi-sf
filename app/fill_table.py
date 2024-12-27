import asyncio
from uuid import uuid4

import pandas
from sqlalchemy import text

from app.database.connection import session
from app.database.models import Exhibit


async def fill_exhibits_table():
    df = pandas.read_excel('app/data/data.xlsx')
    unique_df = df.drop_duplicates(subset='Экспонат')
    async with session() as db:
        # Шаг 4: Вставка данных в таблицу
        for _, row in unique_df.iterrows():
            # Преобразуем данные для вставки в Exhibit
            exhibit = Exhibit(
                id=uuid4(),  # Генерация уникального id
                name=row['Экспонат'],  # Значение столбца 'Экспонат'
                description=row.get('Краткое описание', None),
                wiki_link=row.get('Ссылка на Википедию', None),  # Значение столбца 'Краткое описание', если есть
            )

            # Добавление в сессию
            db.add(exhibit)

        # Шаг 5: Сохранение изменений в базе данных
        await db.commit()
        labels = {0: 'Бурлаки на волге', 1: 'Венера Милосская', 2: 'Дама из Осера', 3: 'Девятый вал', 4: 'Запорожцы',
                  5: 'Клятва Горациев', 6: 'Ладья Данте', 7: 'Мона Лиза, Джоконда', 8: 'Ника Самофракийская',
                  9: 'Плот «Медузы»', 10: 'Портрет Шаляпина', 11: 'Последний день Помпеи',
                  12: 'Психея, оживлённая поцелуем Амура', 13: 'Свобода, ведущая народ', 14: 'Смерть Марата',
                  15: 'Стела Меша', 16: 'Храм Дендур', 17: 'Вашингтон переправляется через Делавэр',
                  18: 'Пара четырехствольных поворотных ударных пистолетов Генри Пелама Файнса Пелама-Клинтона, 4-го герцога Ньюкасл-андер-Лайна (1785–1851), с парой карманных пистолетов с замком Box-Lock Turn-Off, футляром и принадлежностями',
                  19: 'Сабля в Ножнах', 20: 'Портрет Джиневры де Бенчи', 21: 'Потир аббата Сугерия из Сен-Дени',
                  22: 'Часы «Павлин»', 23: 'Скорчившийся мальчик', 24: 'Мумия жреца Па-ди-иста', 25: 'Живопись'}
        for label, name in labels.items():
            sql = text("""
        UPDATE exhibits 
        SET label = :label
        WHERE name = :name
    """)
            await db.execute(sql, {"label": str(label), "name": name})

        await db.commit()

        print("Данные успешно добавлены в таблицу.")


if __name__ == '__main__':
    asyncio.run(fill_exhibits_table())
