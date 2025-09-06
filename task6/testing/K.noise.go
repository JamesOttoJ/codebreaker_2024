/*
K:
  -> s
  <- s
  ...
  -> e, es, ss
*/

// Implementation Version: 1.0.4

/* ---------------------------------------------------------------- *
 * PARAMETERS                                                       *
 * ---------------------------------------------------------------- */

package main

import (
	"crypto/rand"
	"crypto/subtle"
	"encoding/binary"
	"errors"
	"golang.org/x/crypto/blake2s"
	"golang.org/x/crypto/chacha20poly1305"
	"golang.org/x/crypto/curve25519"
	"golang.org/x/crypto/hkdf"
	"hash"
	"io"
	"math"
  "log"
  "fmt"
  "bytes"
  "encoding/base32"
  "strings"
)

/* ---------------------------------------------------------------- *
 * TYPES                                                            *
 * ---------------------------------------------------------------- */

type keypair struct {
	public_key  [32]byte
	private_key [32]byte
}

type messagebuffer struct {
	ne         [32]byte
	ns         []byte
	ciphertext []byte
}

type cipherstate struct {
	k [32]byte
	n uint64
}

type symmetricstate struct {
	cs cipherstate
	ck [32]byte
	h  [32]byte
}

type handshakestate struct {
	ss  symmetricstate
	s   keypair
	e   keypair
	rs  [32]byte
	re  [32]byte
	psk [32]byte
}

type noisesession struct {
	hs  handshakestate
	h   [32]byte
	cs1 cipherstate
	cs2 cipherstate
	mc  uint64
	i   bool
}

/* ---------------------------------------------------------------- *
 * CONSTANTS                                                        *
 * ---------------------------------------------------------------- */

var emptyKey = [32]byte{
	0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00,
}

var minNonce = uint64(0)

/* ---------------------------------------------------------------- *
 * UTILITY FUNCTIONS                                                *
 * ---------------------------------------------------------------- */

func getPublicKey(kp *keypair) [32]byte {
	return kp.public_key
}

func isEmptyKey(k [32]byte) bool {
	return subtle.ConstantTimeCompare(k[:], emptyKey[:]) == 1
}

func validatePublicKey(k []byte) bool {
	forbiddenCurveValues := [12][]byte{
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{224, 235, 122, 124, 59, 65, 184, 174, 22, 86, 227, 250, 241, 159, 196, 106, 218, 9, 141, 235, 156, 50, 177, 253, 134, 98, 5, 22, 95, 73, 184, 0},
		{95, 156, 149, 188, 163, 80, 140, 36, 177, 208, 177, 85, 156, 131, 239, 91, 4, 68, 92, 196, 88, 28, 142, 134, 216, 34, 78, 221, 208, 159, 17, 87},
		{236, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127},
		{237, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127},
		{238, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127},
		{205, 235, 122, 124, 59, 65, 184, 174, 22, 86, 227, 250, 241, 159, 196, 106, 218, 9, 141, 235, 156, 50, 177, 253, 134, 98, 5, 22, 95, 73, 184, 128},
		{76, 156, 149, 188, 163, 80, 140, 36, 177, 208, 177, 85, 156, 131, 239, 91, 4, 68, 92, 196, 88, 28, 142, 134, 216, 34, 78, 221, 208, 159, 17, 215},
		{217, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255},
		{218, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255},
		{219, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 25},
	}

	for _, testValue := range forbiddenCurveValues {
		if subtle.ConstantTimeCompare(k[:], testValue[:]) == 1 {
			panic("Invalid public key")
		}
	}
	return true
}
/* ---------------------------------------------------------------- *
 * PRIMITIVES                                                       *
 * ---------------------------------------------------------------- */

func incrementNonce(n uint64) uint64 {
	return n + 1
}

func dh(private_key [32]byte, public_key [32]byte) [32]byte {
	var ss [32]byte
	curve25519.ScalarMult(&ss, &private_key, &public_key)
	return ss
}

func generateKeypair() keypair {
	var public_key [32]byte
	var private_key [32]byte
	_, _ = rand.Read(private_key[:])
	curve25519.ScalarBaseMult(&public_key, &private_key)
	if validatePublicKey(public_key[:]) {
		return keypair{public_key, private_key}
	}
	return generateKeypair()
}

func generatePublicKey(private_key [32]byte) [32]byte {
	var public_key [32]byte
	curve25519.ScalarBaseMult(&public_key, &private_key)
	return public_key
}

func encrypt(k [32]byte, n uint64, ad []byte, plaintext []byte) []byte {
	var nonce [12]byte
	var ciphertext []byte
	enc, _ := chacha20poly1305.New(k[:])
	binary.LittleEndian.PutUint64(nonce[4:], n)
	ciphertext = enc.Seal(nil, nonce[:], plaintext, ad)
	return ciphertext
}

func decrypt(k [32]byte, n uint64, ad []byte, ciphertext []byte) (bool, []byte, []byte, error) {
	var nonce [12]byte
	var plaintext []byte
	enc, err := chacha20poly1305.New(k[:])
	binary.LittleEndian.PutUint64(nonce[4:], n)
	plaintext, err = enc.Open(nil, nonce[:], ciphertext, ad)
	return (err == nil), ad, plaintext, err
}

func getHash(a []byte, b []byte) [32]byte {
	return blake2s.Sum256(append(a, b...))
}

func hashProtocolName(protocolName []byte) [32]byte {
	var h [32]byte
	if len(protocolName) <= 32 {
		copy(h[:], protocolName)
	} else {
		h = getHash(protocolName, []byte{})
	}
	return h
}

func blake2HkdfInterface() hash.Hash {
	h, _ := blake2s.New256([]byte{})
	return h
}

func getHkdf(ck [32]byte, ikm []byte) ([32]byte, [32]byte, [32]byte) {
	var k1 [32]byte
	var k2 [32]byte
	var k3 [32]byte
	output := hkdf.New(blake2HkdfInterface, ikm[:], ck[:], []byte{})
	io.ReadFull(output, k1[:])
	io.ReadFull(output, k2[:])
	io.ReadFull(output, k3[:])
	return k1, k2, k3
}

/* ---------------------------------------------------------------- *
 * STATE MANAGEMENT                                                 *
 * ---------------------------------------------------------------- */

/* CipherState */
func initializeKey(k [32]byte) cipherstate {
	return cipherstate{k, minNonce}
}

func hasKey(cs *cipherstate) bool {
	return !isEmptyKey(cs.k)
}

func setNonce(cs *cipherstate, newNonce uint64) *cipherstate {
	cs.n = newNonce
	return cs
}

func encryptWithAd(cs *cipherstate, ad []byte, plaintext []byte) (*cipherstate, []byte, error) {
	var err error
	if cs.n == math.MaxUint64-1 {
		err = errors.New("encryptWithAd: maximum nonce size reached")
		return cs, []byte{}, err
	}
	e := encrypt(cs.k, cs.n, ad, plaintext)
	cs = setNonce(cs, incrementNonce(cs.n))
	return cs, e, err
}

func decryptWithAd(cs *cipherstate, ad []byte, ciphertext []byte) (*cipherstate, []byte, bool, error) {
	var err error
	if cs.n == math.MaxUint64-1 {
		err = errors.New("decryptWithAd: maximum nonce size reached")
		return cs, []byte{}, false, err
	}
	valid, ad, plaintext, err := decrypt(cs.k, cs.n, ad, ciphertext)
	if valid {
		cs = setNonce(cs, incrementNonce(cs.n))
	}
	return cs, plaintext, valid, err
}

func reKey(cs *cipherstate) *cipherstate {
	e := encrypt(cs.k, math.MaxUint64, []byte{}, emptyKey[:])
	copy(cs.k[:], e)
	return cs
}

/* SymmetricState */

func initializeSymmetric(protocolName []byte) symmetricstate {
	h := hashProtocolName(protocolName)
	ck := h
	cs := initializeKey(emptyKey)
	return symmetricstate{cs, ck, h}
}

func mixKey(ss *symmetricstate, ikm [32]byte) *symmetricstate {
	ck, tempK, _ := getHkdf(ss.ck, ikm[:])
	ss.cs = initializeKey(tempK)
	ss.ck = ck
	return ss
}

func mixHash(ss *symmetricstate, data []byte) *symmetricstate {
	ss.h = getHash(ss.h[:], data)
	return ss
}

func mixKeyAndHash(ss *symmetricstate, ikm [32]byte) *symmetricstate {
	var tempH [32]byte
	var tempK [32]byte
	ss.ck, tempH, tempK = getHkdf(ss.ck, ikm[:])
	ss = mixHash(ss, tempH[:])
	ss.cs = initializeKey(tempK)
	return ss
}

func getHandshakeHash(ss *symmetricstate) [32]byte {
	return ss.h
}

func encryptAndHash(ss *symmetricstate, plaintext []byte) (*symmetricstate, []byte, error) {
	var ciphertext []byte
	var err error
	if hasKey(&ss.cs) {
		_, ciphertext, err = encryptWithAd(&ss.cs, ss.h[:], plaintext)
		if err != nil {
			return ss, []byte{}, err
		}
	} else {
		ciphertext = plaintext
	}
	ss = mixHash(ss, ciphertext)
	return ss, ciphertext, err
}

func decryptAndHash(ss *symmetricstate, ciphertext []byte) (*symmetricstate, []byte, bool, error) {
	var plaintext []byte
	var valid bool
	var err error
	if hasKey(&ss.cs) {
		_, plaintext, valid, err = decryptWithAd(&ss.cs, ss.h[:], ciphertext)
		if err != nil {
			return ss, []byte{}, false, err
		}
	} else {
		plaintext, valid = ciphertext, true
	}
	ss = mixHash(ss, ciphertext)
	return ss, plaintext, valid, err
}

func split(ss *symmetricstate) (cipherstate, cipherstate) {
	tempK1, tempK2, _ := getHkdf(ss.ck, []byte{})
	cs1 := initializeKey(tempK1)
	cs2 := initializeKey(tempK2)
	return cs1, cs2
}

/* HandshakeState */

func initializeInitiator(prologue []byte, s keypair, rs [32]byte, psk [32]byte) handshakestate {
	var ss symmetricstate
	var e keypair
	var re [32]byte
	name := []byte("Noise_K_25519_ChaChaPoly_BLAKE2s")
	ss = initializeSymmetric(name)
	mixHash(&ss, prologue)
	mixHash(&ss, s.public_key[:])
	mixHash(&ss, rs[:])
	return handshakestate{ss, s, e, rs, re, psk}
}

func initializeResponder(prologue []byte, s keypair, rs [32]byte, psk [32]byte) handshakestate {
	var ss symmetricstate
	var e keypair
	var re [32]byte
	name := []byte("Noise_K_25519_ChaChaPoly_BLAKE2s")
	ss = initializeSymmetric(name)
	mixHash(&ss, prologue)
	mixHash(&ss, rs[:])
	mixHash(&ss, s.public_key[:])
	return handshakestate{ss, s, e, rs, re, psk}
}

func writeMessageA(hs *handshakestate, payload []byte) ([32]byte, messagebuffer, cipherstate, cipherstate, error) {
	var err error
	var messageBuffer messagebuffer
	ne, ns, ciphertext := emptyKey, []byte{}, []byte{}
	hs.e = generateKeypair()
	ne = hs.e.public_key
	mixHash(&hs.ss, ne[:])
	/* No PSK, so skipping mixKey */
	mixKey(&hs.ss, dh(hs.e.private_key, hs.s.public_key))
	mixKey(&hs.ss, dh(hs.s.private_key, hs.rs))
	_, ciphertext, err = encryptAndHash(&hs.ss, payload)
	if err != nil {
		cs1, cs2 := split(&hs.ss)
		return hs.ss.h, messageBuffer, cs1, cs2, err
	}
	messageBuffer = messagebuffer{ne, ns, ciphertext}
	cs1, cs2 := split(&hs.ss)
	return hs.ss.h, messageBuffer, cs1, cs2, err
}

func writeMessageRegular(cs *cipherstate, payload []byte) (*cipherstate, messagebuffer, error) {
	var err error
	var messageBuffer messagebuffer
	ne, ns, ciphertext := emptyKey, []byte{}, []byte{}
	cs, ciphertext, err = encryptWithAd(cs, []byte{}, payload)
	if err != nil {
		return cs, messageBuffer, err
	}
	messageBuffer = messagebuffer{ne, ns, ciphertext}
	return cs, messageBuffer, err
}

func readMessageA(hs *handshakestate, message *messagebuffer) ([32]byte, []byte, bool, cipherstate, cipherstate, error) {
	var err error
	var plaintext []byte
	var valid2 bool = false
	var valid1 bool = true
	if validatePublicKey(message.ne[:]) {
		hs.re = message.ne
	}
	mixHash(&hs.ss, hs.re[:])
	/* No PSK, so skipping mixKey */
	mixKey(&hs.ss, dh(hs.s.private_key, hs.re))
	mixKey(&hs.ss, dh(hs.s.private_key, hs.rs))
	_, plaintext, valid2, err = decryptAndHash(&hs.ss, message.ciphertext)
	cs1, cs2 := split(&hs.ss)
	return hs.ss.h, plaintext, (valid1 && valid2), cs1, cs2, err
}

func readMessageRegular(cs *cipherstate, message *messagebuffer) (*cipherstate, []byte, bool, error) {
	var err error
	var plaintext []byte
	var valid2 bool = false
	/* No encrypted keys */
	_, plaintext, valid2, err = decryptWithAd(cs, []byte{}, message.ciphertext)
	return cs, plaintext, valid2, err
}

/* ---------------------------------------------------------------- *
 * PROCESSES                                                        *
 * ---------------------------------------------------------------- */

func InitSession(initiator bool, prologue []byte, s keypair, rs [32]byte) noisesession {
	var session noisesession
	psk := emptyKey
	if initiator {
		session.hs = initializeInitiator(prologue, s, rs, psk)
	} else {
		session.hs = initializeResponder(prologue, s, rs, psk)
	}
	session.i = initiator
	session.mc = 0
	return session
}

func SendMessage(session *noisesession, message []byte) (*noisesession, messagebuffer, error) {
	var err error
	var messageBuffer messagebuffer
	if session.mc == 0 {
		session.h, messageBuffer, session.cs1, _, err = writeMessageA(&session.hs, message)
		session.hs = handshakestate{}
      }
	if session.mc > 0 {
		if session.i {
			_, messageBuffer, err = writeMessageRegular(&session.cs1, message)
		} else {
			_, messageBuffer, err = writeMessageRegular(&session.cs1, message)
		}
	}
	session.mc = session.mc + 1
	return session, messageBuffer, err
}

func RecvMessage(session *noisesession, message *messagebuffer) (*noisesession, []byte, bool, error) {
	var err error
	var plaintext []byte
	var valid bool
	if session.mc == 0 {
		session.h, plaintext, valid, session.cs1, _, err = readMessageA(&session.hs, message)
		session.hs = handshakestate{}
	}
	if session.mc > 0 {
		if session.i {
			_, plaintext, valid, err = readMessageRegular(&session.cs1, message)
		} else {
			_, plaintext, valid, err = readMessageRegular(&session.cs1, message)
		}
	}
	session.mc = session.mc + 1
	return session, plaintext, valid, err
}

func main() {
  log.Printf("Starting...")

  privateKey := [32]byte{0xc0, 0x01, 0x48, 0x28, 0x3a, 0xe4, 0x59, 0xfc, 0x94, 0x51, 0x9a, 0x4d, 0x74, 0x9b, 0xd1, 0x75, 0x29, 0x76, 0x9c, 0xe0, 0x14, 0x57, 0x5a, 0x6f, 0xa5, 0x5f, 0x81, 0x27, 0x37, 0x6a, 0x84, 0x29}
  publicKey := [32]byte{0x88, 0x4c, 0x80, 0x93, 0x74, 0x46, 0x44, 0x72, 0xca, 0x6b, 0x93, 0x7c, 0xe3, 0x62, 0x07, 0x50, 0xca, 0xf3, 0x56, 0x9f, 0x06, 0x9f, 0x09, 0xee, 0xef, 0xf4, 0xc8, 0x9e, 0x41, 0x61, 0x40, 0x0e}
  staticRS := keypair{
    private_key: privateKey,
    public_key:  publicKey,
  }

  PubKey := [32]byte{0xe4, 0x51, 0xa5, 0x06, 0x7a, 0x33, 0xe8, 0x91, 0xa8, 0xd9, 0xcd, 0xe6, 0x5d, 0xa8, 0xf2, 0xfb, 0x74, 0x40, 0x5c, 0x7d, 0xeb, 0xf8, 0x9e, 0x31, 0x57, 0xf5, 0xc6, 0xe3, 0x45, 0x8e, 0xc3, 0x4e}
  
  prologue := []byte{}
  buf := new(bytes.Buffer)
  // Reset sessions at the start of each iteration
  initiatorSession := InitSession(false, prologue, staticRS, PubKey)
  responderSession := InitSession(false, prologue, staticRS, PubKey)

  payload := []byte("aaaaa")
  // Send message and get updated session
  sessionPtr, messageBuffer1, err := SendMessage(&initiatorSession, payload)
  if err != nil {
    fmt.Println("Error in SendMessage:", err)
    return
  }
  initiatorSession = *sessionPtr

  buf.Write(messageBuffer1.ne[:])
  buf.Write(messageBuffer1.ns)
  buf.Write(messageBuffer1.ciphertext)

  // Print result and domain format
  fmt.Printf("%x\n", buf.Bytes())
  fillerX := "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  
  encoded := base32.HexEncoding.EncodeToString(buf.Bytes())
  if (len(encoded) < 63){
    fmt.Printf("x%s.x%s.x%s.net-x7yfcbnc.example.com.\n", strings.Replace(encoded[:len(encoded)], "=", "z", -1) + fillerX[:62-len(encoded)], fillerX, fillerX)
  } else if (len(encoded) < 125) {
    fmt.Printf("x%s.x%s.x%s.net-x7yfcbnc.example.com.\n", encoded[:62], strings.Replace(encoded[62:len(encoded)], "=", "z", -1) + fillerX[:124-len(encoded)], fillerX)
  } else if (len(encoded) < 187) {
    fmt.Printf("x%s.x%s.x%s.net-x7yfcbnc.example.com.\n", encoded[:62], encoded[62:124], strings.Replace(encoded[124:len(encoded)], "=", "z", -1) + fillerX[:124-len(encoded)])
  } else {
    fmt.Printf("Too long of a result")
  }
  buf.Reset()
  // Receive message and get updated session
  sessionPtr, plaintext, valid1, err := RecvMessage(&responderSession, &messageBuffer1)
  if err != nil || !valid1 {
    fmt.Printf("Handshake failed at responder: %s\n", err)
  }
  responderSession = *sessionPtr
  
  fmt.Printf("%x\n", plaintext)
 }
