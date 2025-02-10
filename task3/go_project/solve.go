package main

import (
  "math/rand"
  "log"
)

func main() {
  rand.Seed(515797029933644) // 0x1d51d5abed24c
  oldSeed := rand.Int63() & 0xffffffff
  count := 0
  for true {
    //    temp := 0x74736574 ^ oldSeed // "temp" little end
    temp := 0x7073616a ^ oldSeed // "jasp" little end
    temp = 0x305f7265 ^ temp // "er_0" little end
    temp = 0x38333035 ^ temp
//    temp := 0x4a415350 ^ oldSeed
//    temp = 0x45525f30 ^ temp
    count = count + 1
    seed := rand.Int63()
//    log.Printf("%x | %x | %d | %d\n", temp, oldSeed, seed, count)
//    break
    if (temp == 0x8b16bd5d) { log.Printf("Success! {\"username\":\"jasper_05038\",\"seed\":%d,\"count\":%d}\n", seed, count); break }
    if (count % 1000000 == 0) { log.Printf("Count: %d\n", count) }
    oldSeed = seed & 0xffffffff
  }
}
