import grpc
import cars_data_pb2
import cars_data_pb2_grpc
import psycopg2
from concurrent import futures
import time

def connect_to_postgres(conn_str, max_retries=10, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(conn_str)
            print("Conexión establecida con la base de datos PostgreSQL.")
            return conn
        except psycopg2.Error as e:
            retries += 1
            print(f"Error al conectar con la base de datos PostgreSQL ({retries}/{max_retries}): {e}")
            time.sleep(retry_delay)

    print("No se pudo establecer la conexión con la base de datos PostgreSQL después de los reintentos.")
    return None

def main():
    server_address = 'localhost:50052'    
    
    POSTGRES_HOST = 'postgres'  
    POSTGRES_PORT = 5432
    POSTGRES_DB = 'tarea1'
    POSTGRES_USER = 'tiago'
    POSTGRES_PASSWORD = 'tarea11'

    conn_str = f"host={POSTGRES_HOST} port={POSTGRES_PORT} dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD}"

    conn = connect_to_postgres(conn_str)
    if conn is None:
        return 

    # Agregar retardo antes de iniciar el servidor gRPC
    print("Esperando 10 segundos antes de iniciar el servidor gRPC...")
    time.sleep(10)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cars_data_pb2_grpc.add_CarServiceServicer_to_server(CarService(conn), server)
    server.add_insecure_port(server_address)
    server.start()
    print(f'Servidor gRPC escuchando en {server_address}')

    time.sleep(5)

    server.wait_for_termination()
    

    

class CarService(cars_data_pb2_grpc.CarServiceServicer):
    def __init__(self, conn):
        self.conn = conn

    def GetCar(self, request, context):
        car_id = request.id
        cur = self.conn.cursor()
        cur.execute("SELECT id, car_name, Present_Price FROM cars WHERE id = %s", (car_id,))
        car = cur.fetchone()
        cur.close()

        if car:
            response = cars_data_pb2.CarResponse(
                id=car[0],
                car_name=car[1],
                Present_Price=car[2]
            )
            return response
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Car not found")
            return cars_data_pb2.CarResponse()

if __name__ == '__main__':
    main()