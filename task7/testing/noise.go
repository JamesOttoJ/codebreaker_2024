package main

import (
  . "github.com/flynn/noise"
  "log"
  "fmt"
  "golang.org/x/crypto/curve25519"
  "errors"
)

type RandomInc byte

type MyHandshakeState HandshakeState

func (r *RandomInc) Read(p []byte) (int, error) {
	for i := range p {
		p[i] = byte(*r)
		*r = (*r) + 1
	}
	return len(p), nil
}

// NewX25519KeyFromPrivateKey creates a X25519Key from private key bytes.
func NewX25519KeyFromPrivateKey(privateKey [32]byte) DHKey {
	publicKey := new([32]byte)
	curve25519.ScalarBaseMult(publicKey, &privateKey)
	return DHKey{
      Private: privateKey[:],
      Public:  publicKey[:],
	}
}

// WriteMessage appends a handshake message to out. The message will include the
// optional payload if provided. If the handshake is completed by the call, two
// CipherStates will be returned, one is used for encryption of messages to the
// remote peer, the other is used for decryption of messages from the remote
// peer. It is an error to call this method out of sync with the handshake
// pattern.
func (s *MyHandshakeState) WriteMessage(out, payload []byte) ([]byte, *CipherState, *CipherState, error) {
	if !s.shouldWrite {
		return nil, nil, nil, errors.New("noise: unexpected call to WriteMessage should be ReadMessage")
	}
	if s.msgIdx > len(s.messagePatterns)-1 {
		return nil, nil, nil, errors.New("noise: no handshake messages left")
	}
	if len(payload) > MaxMsgLen {
		return nil, nil, nil, errors.New("noise: message is too long")
	}

	var err error
	for _, msg := range s.messagePatterns[s.msgIdx] {
		switch msg {
		case MessagePatternE:
			e, err := s.ss.cs.GenerateKeypair(s.rng)
			if err != nil {
				return nil, nil, nil, err
			}
			s.e = e
			out = append(out, s.e.Public...)
			s.ss.MixHash(s.e.Public)
			if s.willPsk {
				s.ss.MixKey(s.e.Public)
			}
		case MessagePatternS:
			if len(s.s.Public) == 0 {
				return nil, nil, nil, errors.New("noise: invalid state, s.Public is nil")
			}
			out, err = s.ss.EncryptAndHash(out, s.s.Public)
			if err != nil {
				return nil, nil, nil, err
			}
		case MessagePatternDHEE:
			dh, err := s.ss.cs.DH(s.e.Private, s.re)
			if err != nil {
				return nil, nil, nil, err
			}
			s.ss.MixKey(dh)
		case MessagePatternDHES:
			if s.initiator {
				dh, err := s.ss.cs.DH(s.e.Private, s.s.Public)
				if err != nil {
					return nil, nil, nil, err
				}
				s.ss.MixKey(dh)
			} else {
				dh, err := s.ss.cs.DH(s.s.Private, s.re)
				if err != nil {
					return nil, nil, nil, err
				}
				s.ss.MixKey(dh)
			}
		case MessagePatternDHSE:
			if s.initiator {
				dh, err := s.ss.cs.DH(s.s.Private, s.re)
				if err != nil {
					return nil, nil, nil, err
				}
				s.ss.MixKey(dh)
			} else {
				dh, err := s.ss.cs.DH(s.e.Private, s.rs)
				if err != nil {
					return nil, nil, nil, err
				}
				s.ss.MixKey(dh)
			}
		case MessagePatternDHSS:
			dh, err := s.ss.cs.DH(s.s.Private, s.rs)
			if err != nil {
				return nil, nil, nil, err
			}
			s.ss.MixKey(dh)
		case MessagePatternPSK:
			if len(s.psk) == 0 {
				return nil, nil, nil, errors.New("noise: cannot send psk message without psk set")
			}
			s.ss.MixKeyAndHash(s.psk)
		}
	}
	s.shouldWrite = false
	s.msgIdx++
	out, err = s.ss.EncryptAndHash(out, payload)
	if err != nil {
		return nil, nil, nil, err
	}

	if s.msgIdx >= len(s.messagePatterns) {
		cs1, cs2 := s.ss.Split()
		return out, cs1, cs2, nil
	}

	return out, nil, nil, nil
}

func main() {
  log.Printf("Starting...")
  cs := NewCipherSuite(DH25519, CipherChaChaPoly, HashBLAKE2s)
  rng := new(RandomInc)
  /*
  staticR, err := cs.GenerateKeypair(rng)
  if (err != nil) {
    fmt.Println(err)
  }
  fmt.Println("staticR:")
  fmt.Printf("%x\n", staticR.Public)
  
  staticS, err := cs.GenerateKeypair(rng)
  fmt.Println("staticS:")
  fmt.Printf("%x\n", staticS.Public)
  fmt.Printf("%x\n", staticS.Private)
  */
  staticRS := NewX25519KeyFromPrivateKey([32]byte{0xc0, 0x01, 0x48, 0x28, 0x3a, 0xe4, 0x59, 0xfc, 0x94, 0x51, 0x9a, 0x4d, 0x74, 0x9b, 0xd1, 0x75, 0x29, 0x76, 0x9c, 0xe0, 0x14, 0x57, 0x5a, 0x6f, 0xa5, 0x5f, 0x81, 0x27, 0x37, 0x6a, 0x84, 0x29})
  fmt.Printf("%x\n", staticRS.Public)
  staticS := NewX25519KeyFromPrivateKey([32]byte{0x10, 0xe8, 0xc8, 0x4a, 0xc5 ,0x9d ,0x38, 0xee, 0x4b, 0x77, 0xd1, 0xfb, 0x35, 0xda, 0xad, 0x74, 0x5b, 0x30, 0xc8, 0x4b, 0x37, 0xb8, 0xa1, 0x13, 0x90, 0xc4, 0x3f, 0xc6, 0xda, 0xb2, 0x6f, 0xe3})
  fmt.Printf("%x\n", staticS.Public)
  PubKey := []byte{0xe4, 0x51, 0xa5, 0x06, 0x7a, 0x33, 0xe8, 0x91, 0xa8, 0xd9, 0xcd, 0xe6, 0x5d, 0xa8, 0xf2, 0xfb, 0x74, 0x40, 0x5c, 0x7d, 0xeb, 0xf8, 0x9e, 0x31, 0x57, 0xf5, 0xc6, 0xe3, 0x45, 0x8e, 0xc3, 0x4e}
  hs, err := NewHandshakeState(Config{
    CipherSuite: cs,
    Random:      rng,
    Pattern:     HandshakeK,
    Initiator:   false,
    StaticKeypair: staticRS,
    PeerStatic:  PubKey,
  })
  
  if (err != nil) {
    fmt.Println("Error")
    fmt.Println(err)
  }
  hs.initiatior = true
  hs.shouldWrite = true
  hs = &MyHandshakeState{hs}
  hello, csEncrypt, csDecrypt, err := hs.WriteMessage(nil, nil)
  
  if (err != nil) {
    fmt.Println("Error")
    fmt.Println(err)
  }
  
  fmt.Println(csEncrypt)
  fmt.Println(csDecrypt)
  log.Printf("%x", hello)
}
