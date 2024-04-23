import redis

class RedisReplicationClient:
    def __init__(self, master_host='redis-master', master_port=6379, replica_host='redis-replica', replica_port=6379):
        self.master = redis.Redis(host=master_host, port=master_port)
        self.replica = redis.Redis(host=replica_host, port=replica_port)

    def get_car(self, car_id):
        car_data = self.replica.get(f"car:{car_id}")
        if car_data:
            return eval(car_data)
        return None

    def set_car(self, car_id, car_data):
        self.master.set(f"car:{car_id}", str(car_data))