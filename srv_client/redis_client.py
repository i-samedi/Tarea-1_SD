import redis

class RedisClient:
    def __init__(self, host='redis', port=6379):
        self.client = redis.Redis(host=host, port=port)

    def get_car(self, car_id):
        car_data = self.client.get(f"car:{car_id}")
        if car_data:
            return eval(car_data)
        return None

    def set_car(self, car_id, car_data):
        self.client.set(f"car:{car_id}", str(car_data))