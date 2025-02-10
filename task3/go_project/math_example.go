package main

import (
  "math/rand"
  "log"
)

func main() {
  rand.Seed(515797029933644) // 0x1d51d5abed24c
  log.Printf("%x\n", rand.Int63())
  log.Printf("%x\n", rand.Int63())
  log.Printf("%x\n", rand.Int63())
}
