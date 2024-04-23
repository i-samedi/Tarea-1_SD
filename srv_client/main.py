import time
import grpc
import cars_data_pb2
import cars_data_pb2_grpc
from redis_client import RedisClient
from redis_cluster_client import RedisClusterClient
from redis_replication_client import RedisReplicationClient
from grpc import retry

#Redis Clasic
class CarService(cars_data_pb2_grpc.CarServiceServicer):
    def __init__(self):
        self.redis_client = RedisClient()

    def GetCar(self, request, context):
        car_id = request.id
        car_data = self.redis_client.get_car(car_id)

        if car_data:
            response = cars_data_pb2.CarResponse(
                id=car_data['id'],
                car_name=car_data['car_name'],
                Present_Price=car_data['Present_Price']
            )
            return response
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Car not found")
            return cars_data_pb2.CarResponse()
        
# Redis Cluster
class CarService(cars_data_pb2_grpc.CarServiceServicer):
    def __init__(self):
        startup_nodes = [
            {"host": "redis-cluster", "port": "7000"},
            {"host": "redis-cluster", "port": "7001"},
            {"host": "redis-cluster", "port": "7002"}
        ]
        self.redis_cluster_client = RedisClusterClient(startup_nodes)

    def GetCar(self, request, context):
        car_id = request.id
        car_data = self.redis_cluster_client.get_car(car_id)

        if car_data:
            response = cars_data_pb2.CarResponse(
                id=car_data['id'],
                car_name=car_data['car_name'],
                Present_Price=car_data['Present_Price']
            )
            return response
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Car not found")
            return cars_data_pb2.CarResponse()

# Redis Replication
class CarService(cars_data_pb2_grpc.CarServiceServicer):
    def __init__(self):
        self.redis_replication_client = RedisReplicationClient()

    def GetCar(self, request, context):
        car_id = request.id
        car_data = self.redis_replication_client.get_car(car_id)

        if car_data:
            response = cars_data_pb2.CarResponse(
                id=car_data['id'],
                car_name=car_data['car_name'],
                Present_Price=car_data['Present_Price']
            )
            return response
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Car not found")
            return cars_data_pb2.CarResponse()


def main():
    server_address = 'localhost:50052'

    max_attempts = 10

    channel = grpc.insecure_channel(server_address)
    stub = cars_data_pb2_grpc.CarServiceStub(channel)

    request = cars_data_pb2.CarRequest(id=1)  # Cambia el id según sea necesario

    # Agregar un tiempo de espera antes de hacer la llamada gRPC
    print("Esperando 60 segundos antes de hacer la llamada gRPC...")
    time.sleep(60)

    attempts = 0
    while attempts < max_attempts:
        try:
            response = stub.GetCar(request)
            print(f"ID del coche: {response.id}")
            print(f"Nombre del coche: {response.car_name}")
            print(f"Precio actual: {response.Present_Price}")
            break  
        except grpc.RpcError as e:
            attempts += 1
            print(f"Error: {e.details()} (Intento {attempts}/{max_attempts})")
            if attempts == max_attempts:
                print("Se alcanzó el número máximo de intentos. Saliendo.")
            else:
                time.sleep(5)

if __name__ == '__main__':
    main()
