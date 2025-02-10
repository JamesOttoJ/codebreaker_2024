package main

import (
	"context"
	"flag"
	"log"
	"time"
//    "runtime"

//    "github.com/zenthangplus/goccm"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	pb "codebreakers/proto/seed_generation"
)

var (
	addr = flag.String("addr", "localhost:50051", "the address to connect to")
)


func main() {
	flag.Parse()
	// Set up a connection to the server.
	conn, err := grpc.NewClient(*addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewSeedGenerationServiceClient(conn)

    ctx, cancel := context.WithTimeout(context.Background(), time.Minute)
	defer cancel()
    r, err := c.GetSeed(ctx, &pb.GetSeedRequest{Username: "test", Password: ""})
	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}
    log.Printf("Seed: %x | Count: %x", r.GetSeed(), r.GetCount())
}
