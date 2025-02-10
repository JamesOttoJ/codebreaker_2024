package main

import (
	"context"
    "flag"
    "net"
    "fmt"
    "log"

	"google.golang.org/grpc"
//	"google.golang.org/grpc/codes"
//	"google.golang.org/grpc/status"

//	grpc_auth "github.com/grpc-ecosystem/go-grpc-middleware/auth"
//	grpc_ctxtags "github.com/grpc-ecosystem/go-grpc-middleware/tags"
    pb "codebreakers/proto/auth_service"
)

var (
	port = flag.Int("port", 50052, "The server port")
)

type server struct {
	pb.UnimplementedAuthServiceServer
}

func (s *server) Authenticate(_ context.Context, in *pb.AuthRequest) (*pb.AuthResponse, error) {
//	log.Printf("Received: Authenticate")
    return &pb.AuthResponse{Success: true}, nil
}

func (s *server) RegisterOTPSeed(_ context.Context, in *pb.RegisterOTPSeedRequest) (*pb.RegisterOTPSeedResponse, error) {
//	log.Printf("Received: Register Seed")
//    if (in.GetCount() % 1000000 == 0) { log.Printf("Rcv seed count: %d\n", in.GetCount()) }
    return &pb.RegisterOTPSeedResponse{Success: true}, nil
}

func (s *server) Ping(_ context.Context, in *pb.PingRequest) (*pb.PingResponse, error) {
//	log.Printf("Received: Ping")
    return &pb.PingResponse{Response: 8765}, nil
}

func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterAuthServiceServer(s, &server{})
	log.Printf("server listening at %v", lis.Addr())
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
