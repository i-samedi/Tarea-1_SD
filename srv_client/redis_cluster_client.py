import redis

class RedisClusterClient:
    def __init__(self, startup_nodes):
        self.client = redis.Redis(startup_nodes)

    def get_car(self, car_id):
        car_data = self.client.get(f"car:{car_id}")
        if car_data:
            return eval(car_data)
        return None

    def set_car(self, car_id, car_data):
        self.client.set(f"car:{car_id}", str(car_data))