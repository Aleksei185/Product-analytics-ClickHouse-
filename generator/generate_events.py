import random
from datetime import datetime, timedelta
import clickhouse_connect

client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,
    username='default',
    password=''
)

pages = ['/home', '/catalog', '/product', '/cart', '/checkout']
countries = ['Russia', 'Germany', 'USA', 'China', 'Brazil', 'India']

RETENTION_PROBS = [1.0, 0.40, 0.25, 0.15, 0.10, 0.07, 0.05, 0.03]

def get_user_profile():
    r = random.random()
    if r < 0.05:
        return 4
    elif r < 0.15:
        return 3
    elif r < 0.30:
        return 2
    else:
        return 1

def generate_events(num_users=10000, days_back=30):
    events = []
    now = datetime.now()
    start_date = now - timedelta(days=days_back)

    for user_id in range(1, num_users + 1):
        registration_day = random.randint(0, days_back - 1)
        reg_date = start_date + timedelta(days=registration_day)
        country = random.choice(countries)
        profile = get_user_profile()

        for day_offset in range(8):
            current_date = reg_date + timedelta(days=day_offset)
            if current_date > now:
                break

            if day_offset > 0:
                if random.random() > RETENTION_PROBS[day_offset]:
                    break

            session_time = current_date.replace(
                hour=random.randint(8, 22),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )

            events.append((session_time, user_id, 'page_view', random.choice(pages), country))

            if profile >= 2 and random.random() < 0.7:
                events.append((session_time + timedelta(minutes=2), user_id, 'add_to_cart', '/cart', country))

            if profile >= 3 and random.random() < 0.8:
                events.append((session_time + timedelta(minutes=5), user_id, 'checkout', '/checkout', country))

            if profile >= 4 and random.random() < 0.9:
                events.append((session_time + timedelta(minutes=7), user_id, 'purchase', '/checkout', country))

    return events

def insert_events(events):
    client.insert(
        'analytics.events',
        events,
        column_names=['event_time', 'user_id', 'event_type', 'page', 'country']
    )

if __name__ == '__main__':
    print("Очистка таблицы...")
    client.command('TRUNCATE TABLE analytics.events')

    print("Генерация событий...")
    events = generate_events(num_users=10000, days_back=30)

    print(f"Сгенерировано {len(events)} событий")
    print("Загрузка в ClickHouse...")
    insert_events(events)

    result = client.query('SELECT COUNT(*) FROM analytics.events')
    print(f"Всего событий в таблице: {result.result_rows[0][0]}")
