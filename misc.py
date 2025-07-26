import redis
from decouple import config

redis = redis.Redis(
    host=config('REDIS_HOST'),
    port=config('REDIS_PORT'),
    username=config('REDIS_USER'),
    password=config('REDIS_PASSWORD')
)
conn = False

while not conn:
    try:
        info = redis.info()
        print(info['redis_version'])
        response = redis.ping()

        if response:
            print('подключение успешно')
            conn = True
        else:
            print('не удалось подключиться к redis')
    except Exception as e:
        print(f'error: {e}')