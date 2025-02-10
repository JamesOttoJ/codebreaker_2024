import argparse
import asyncio
import logging
import threading
import _credentials
import grpc

seed_generation_pb2, seed_generation_pb2_grpc = grpc.protos_and_services(
    "seed_generation.proto"
)

auth_service_pb2, auth_service_pb2_grpc = grpc.protos_and_services(
    "auth.proto"
)

def worker(channel, thread_number):
    print("Thread started " + str(thread_number))
    seed_stub = seed_generation_pb2_grpc.SeedGenerationServiceStub(channel)
#    response = seed_stub.GetSeed(seed_generation_pb2.GetSeedRequest(username="test", password=""))
    i = 0
    while True:
        response = seed_stub.GetSeed(seed_generation_pb2.GetSeedRequest(username="JASPER_0", password=""))
        i += 1
        if (i % 10000 == 0): print("Thread: " + str(thread_number) + " | Count: " + str(i))
        #print("Received: " + str(response.seed) + ":" + str(response.count))

#    response = seed_stub.testEmbeddedByValue()
#    print("Received: " + str(response))

#    response = seed_stub.StressTest(seed_generation_pb2.StressTestRequest(count=3))
#    print("Received: " + str(response.response))

def run():
    # metadata = ('user-agent', 'grpc-go/1.64.0')
    channel = grpc.insecure_channel("localhost:50051")
    for i in range(10):
        print("Thread start: " + str(i))
        your_thread = threading.Thread(target=worker, args=(channel,i,))
        your_thread.start()
#    with grpc.insecure_channel("localhost:50052") as channel:
#        auth_stub = auth_service_pb2_grpc.AuthServiceStub(channel)
#        response = auth_stub.Ping(auth_service_pb2.PingRequest(ping=456))
#        print(response)

if __name__ == "__main__":
    logging.basicConfig()
    run()
