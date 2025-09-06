// Copyright 2016 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

// Package blake2s implements the BLAKE2s hash algorithm defined by RFC 7693
// and the extendable output function (XOF) BLAKE2Xs.
//
// BLAKE2s is optimized for 8- to 32-bit platforms and produces digests of any
// size between 1 and 32 bytes.
// For a detailed specification of BLAKE2s see https://blake2.net/blake2.pdf
// and for BLAKE2Xs see https://blake2.net/blake2x.pdf
//
// If you aren't sure which function you need, use BLAKE2s (Sum256 or New256).
// If you need a secret-key MAC (message authentication code), use the New256
// function with a non-nil key.
//
// BLAKE2X is a construction to compute hash values larger than 32 bytes. It
// can produce hash values between 0 and 65535 bytes.
package task6

import (
	"crypto"
	"encoding/binary"
	"errors"
	"hash"
    "math/bits"
    "log"
  )

const (
	// The blocksize of BLAKE2s in bytes.
	BlockSize = 64

	// The hash size of BLAKE2s-256 in bytes.
	Size = 32

	// The hash size of BLAKE2s-128 in bytes.
	Size128 = 16
)

var errKeySize = errors.New("blake2s: invalid key size")

var iv = [8]uint32{
	0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
	0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
}

var (
	useSSE4  = false
	useSSSE3 = false
	useSSE2  = false
)

// Copyright 2016 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

// the precomputed values for BLAKE2s
// there are 10 16-byte arrays - one for each round
// the entries are calculated from the sigma constants.
var precomputed = [10][16]byte{
	{0, 2, 4, 6, 1, 3, 5, 7, 8, 10, 12, 14, 9, 11, 13, 15},
	{14, 4, 9, 13, 10, 8, 15, 6, 1, 0, 11, 5, 12, 2, 7, 3},
	{11, 12, 5, 15, 8, 0, 2, 13, 10, 3, 7, 9, 14, 6, 1, 4},
	{7, 3, 13, 11, 9, 1, 12, 14, 2, 5, 4, 15, 6, 10, 0, 8},
	{9, 5, 2, 10, 0, 7, 4, 15, 14, 11, 6, 3, 1, 12, 8, 13},
	{2, 6, 0, 8, 12, 10, 11, 3, 4, 7, 15, 1, 13, 5, 14, 9},
	{12, 1, 14, 4, 5, 15, 13, 10, 0, 6, 9, 8, 7, 3, 2, 11},
	{13, 7, 12, 3, 11, 14, 1, 9, 5, 15, 8, 2, 0, 4, 6, 10},
	{6, 14, 11, 0, 15, 9, 3, 8, 12, 13, 1, 10, 2, 7, 4, 5},
	{10, 8, 7, 1, 2, 4, 6, 5, 15, 9, 3, 13, 11, 14, 12, 0},
}

func hashBlocksGeneric(h *[8]uint32, c *[2]uint32, flag uint32, blocks []byte) {
	var m [16]uint32
	c0, c1 := c[0], c[1]

	for i := 0; i < len(blocks); {
		c0 += BlockSize
		if c0 < BlockSize {
			c1++
		}

		v0, v1, v2, v3, v4, v5, v6, v7 := h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7]
		v8, v9, v10, v11, v12, v13, v14, v15 := iv[0], iv[1], iv[2], iv[3], iv[4], iv[5], iv[6], iv[7]
		v12 ^= c0
		v13 ^= c1
		v14 ^= flag

		for j := range m {
			m[j] = uint32(blocks[i]) | uint32(blocks[i+1])<<8 | uint32(blocks[i+2])<<16 | uint32(blocks[i+3])<<24
			i += 4
		}

		for k := range precomputed {
			s := &(precomputed[k])

			v0 += m[s[0]]
			v0 += v4
			v12 ^= v0
			v12 = bits.RotateLeft32(v12, -16)
			v8 += v12
			v4 ^= v8
			v4 = bits.RotateLeft32(v4, -12)
			v1 += m[s[1]]
			v1 += v5
			v13 ^= v1
			v13 = bits.RotateLeft32(v13, -16)
			v9 += v13
			v5 ^= v9
			v5 = bits.RotateLeft32(v5, -12)
			v2 += m[s[2]]
			v2 += v6
			v14 ^= v2
			v14 = bits.RotateLeft32(v14, -16)
			v10 += v14
			v6 ^= v10
			v6 = bits.RotateLeft32(v6, -12)
			v3 += m[s[3]]
			v3 += v7
			v15 ^= v3
			v15 = bits.RotateLeft32(v15, -16)
			v11 += v15
			v7 ^= v11
			v7 = bits.RotateLeft32(v7, -12)

			v0 += m[s[4]]
			v0 += v4
			v12 ^= v0
			v12 = bits.RotateLeft32(v12, -8)
			v8 += v12
			v4 ^= v8
			v4 = bits.RotateLeft32(v4, -7)
			v1 += m[s[5]]
			v1 += v5
			v13 ^= v1
			v13 = bits.RotateLeft32(v13, -8)
			v9 += v13
			v5 ^= v9
			v5 = bits.RotateLeft32(v5, -7)
			v2 += m[s[6]]
			v2 += v6
			v14 ^= v2
			v14 = bits.RotateLeft32(v14, -8)
			v10 += v14
			v6 ^= v10
			v6 = bits.RotateLeft32(v6, -7)
			v3 += m[s[7]]
			v3 += v7
			v15 ^= v3
			v15 = bits.RotateLeft32(v15, -8)
			v11 += v15
			v7 ^= v11
			v7 = bits.RotateLeft32(v7, -7)

			v0 += m[s[8]]
			v0 += v5
			v15 ^= v0
			v15 = bits.RotateLeft32(v15, -16)
			v10 += v15
			v5 ^= v10
			v5 = bits.RotateLeft32(v5, -12)
			v1 += m[s[9]]
			v1 += v6
			v12 ^= v1
			v12 = bits.RotateLeft32(v12, -16)
			v11 += v12
			v6 ^= v11
			v6 = bits.RotateLeft32(v6, -12)
			v2 += m[s[10]]
			v2 += v7
			v13 ^= v2
			v13 = bits.RotateLeft32(v13, -16)
			v8 += v13
			v7 ^= v8
			v7 = bits.RotateLeft32(v7, -12)
			v3 += m[s[11]]
			v3 += v4
			v14 ^= v3
			v14 = bits.RotateLeft32(v14, -16)
			v9 += v14
			v4 ^= v9
			v4 = bits.RotateLeft32(v4, -12)

			v0 += m[s[12]]
			v0 += v5
			v15 ^= v0
			v15 = bits.RotateLeft32(v15, -8)
			v10 += v15
			v5 ^= v10
			v5 = bits.RotateLeft32(v5, -7)
			v1 += m[s[13]]
			v1 += v6
			v12 ^= v1
			v12 = bits.RotateLeft32(v12, -8)
			v11 += v12
			v6 ^= v11
			v6 = bits.RotateLeft32(v6, -7)
			v2 += m[s[14]]
			v2 += v7
			v13 ^= v2
			v13 = bits.RotateLeft32(v13, -8)
			v8 += v13
			v7 ^= v8
			v7 = bits.RotateLeft32(v7, -7)
			v3 += m[s[15]]
			v3 += v4
			v14 ^= v3
			v14 = bits.RotateLeft32(v14, -8)
			v9 += v14
			v4 ^= v9
			v4 = bits.RotateLeft32(v4, -7)
		}

		h[0] ^= v0 ^ v8
		h[1] ^= v1 ^ v9
		h[2] ^= v2 ^ v10
		h[3] ^= v3 ^ v11
		h[4] ^= v4 ^ v12
		h[5] ^= v5 ^ v13
		h[6] ^= v6 ^ v14
		h[7] ^= v7 ^ v15
	}
	c[0], c[1] = c0, c1
}


func hashBlocks(h *[8]uint32, c *[2]uint32, flag uint32, blocks []byte) {
	hashBlocksGeneric(h, c, flag, blocks)
}

// Sum256 returns the BLAKE2s-256 checksum of the data.
func Sum256(data []byte) [Size]byte {
	var sum [Size]byte
	checkSum(&sum, Size, data)
	return sum
}

// New256 returns a new hash.Hash computing the BLAKE2s-256 checksum. A non-nil
// key turns the hash into a MAC. The key must between zero and 32 bytes long.
// When the key is nil, the returned hash.Hash implements BinaryMarshaler
// and BinaryUnmarshaler for state (de)serialization as documented by hash.Hash.
func New256(key []byte) (hash.Hash, error) { return newDigest(Size, key) }

func init() {
	crypto.RegisterHash(crypto.BLAKE2s_256, func() hash.Hash {
		h, _ := New256(nil)
		return h
	})
}

// New128 returns a new hash.Hash computing the BLAKE2s-128 checksum given a
// non-empty key. Note that a 128-bit digest is too small to be secure as a
// cryptographic hash and should only be used as a MAC, thus the key argument
// is not optional.
func New128(key []byte) (hash.Hash, error) {
	if len(key) == 0 {
		return nil, errors.New("blake2s: a key is required for a 128-bit hash")
	}
	return newDigest(Size128, key)
}

func newDigest(hashSize int, key []byte) (*digest, error) {
	if len(key) > Size {
		return nil, errKeySize
	}
	d := &digest{
		size:   hashSize,
		keyLen: len(key),
	}
	copy(d.key[:], key)
	d.Reset()
	return d, nil
}

func checkSum(sum *[Size]byte, hashSize int, data []byte) {
	var (
		h [8]uint32
		c [2]uint32
	)

	h = iv
	h[0] ^= uint32(hashSize) | (1 << 16) | (1 << 24)

	if length := len(data); length > BlockSize {
		n := length &^ (BlockSize - 1)
		if length == n {
			n -= BlockSize
		}
		hashBlocks(&h, &c, 0, data[:n])
		data = data[n:]
	}

	var block [BlockSize]byte
	offset := copy(block[:], data)
	remaining := uint32(BlockSize - offset)

	if c[0] < remaining {
		c[1]--
	}
	c[0] -= remaining

	hashBlocks(&h, &c, 0xFFFFFFFF, block[:])

	for i, v := range h {
		binary.LittleEndian.PutUint32(sum[4*i:], v)
	}
}

type digest struct {
	h      [8]uint32
	c      [2]uint32
	size   int
	block  [BlockSize]byte
	offset int

	key    [BlockSize]byte
	keyLen int
}

const (
	magic         = "b2s"
	marshaledSize = len(magic) + 8*4 + 2*4 + 1 + BlockSize + 1
)

func (d *digest) MarshalBinary() ([]byte, error) {
	if d.keyLen != 0 {
		return nil, errors.New("crypto/blake2s: cannot marshal MACs")
	}
	b := make([]byte, 0, marshaledSize)
	b = append(b, magic...)
	for i := 0; i < 8; i++ {
		b = appendUint32(b, d.h[i])
	}
	b = appendUint32(b, d.c[0])
	b = appendUint32(b, d.c[1])
	// Maximum value for size is 32
	b = append(b, byte(d.size))
	b = append(b, d.block[:]...)
	b = append(b, byte(d.offset))
	return b, nil
}

func (d *digest) UnmarshalBinary(b []byte) error {
	if len(b) < len(magic) || string(b[:len(magic)]) != magic {
		return errors.New("crypto/blake2s: invalid hash state identifier")
	}
	if len(b) != marshaledSize {
		return errors.New("crypto/blake2s: invalid hash state size")
	}
	b = b[len(magic):]
	for i := 0; i < 8; i++ {
		b, d.h[i] = consumeUint32(b)
	}
	b, d.c[0] = consumeUint32(b)
	b, d.c[1] = consumeUint32(b)
	d.size = int(b[0])
	b = b[1:]
	copy(d.block[:], b[:BlockSize])
	b = b[BlockSize:]
	d.offset = int(b[0])
	return nil
}

func (d *digest) BlockSize() int { return BlockSize }

func (d *digest) Size() int { return d.size }

func (d *digest) Reset() {
	d.h = iv
	d.h[0] ^= uint32(d.size) | (uint32(d.keyLen) << 8) | (1 << 16) | (1 << 24)
	d.offset, d.c[0], d.c[1] = 0, 0, 0
	if d.keyLen > 0 {
		d.block = d.key
		d.offset = BlockSize
	}
}

func (d *digest) Write(p []byte) (n int, err error) {
	n = len(p)

	if d.offset > 0 {
		remaining := BlockSize - d.offset
		if n <= remaining {
			d.offset += copy(d.block[d.offset:], p)
			return
		}
		copy(d.block[d.offset:], p[:remaining])
		hashBlocks(&d.h, &d.c, 0, d.block[:])
		d.offset = 0
		p = p[remaining:]
	}

	if length := len(p); length > BlockSize {
		nn := length &^ (BlockSize - 1)
		if length == nn {
			nn -= BlockSize
		}
		hashBlocks(&d.h, &d.c, 0, p[:nn])
		p = p[nn:]
	}

	d.offset += copy(d.block[:], p)
	return
}

func (d *digest) Sum(sum []byte) []byte {
	var hash [Size]byte
	d.finalize(&hash)
	return append(sum, hash[:d.size]...)
}

func (d *digest) finalize(hash *[Size]byte) {
	var block [BlockSize]byte
	h := d.h
	c := d.c

	copy(block[:], d.block[:d.offset])
	remaining := uint32(BlockSize - d.offset)
	if c[0] < remaining {
		c[1]--
	}
	c[0] -= remaining

	hashBlocks(&h, &c, 0xFFFFFFFF, block[:])
	for i, v := range h {
		binary.LittleEndian.PutUint32(hash[4*i:], v)
	}
}

func appendUint32(b []byte, x uint32) []byte {
	var a [4]byte
	binary.BigEndian.PutUint32(a[:], x)
	return append(b, a[:]...)
}

func consumeUint32(b []byte) ([]byte, uint32) {
	x := binary.BigEndian.Uint32(b)
	return b[4:], x
}

func checksum() {
  var result [32]byte
  var temp []byte
  //checkSum(&result, 32, []byte{0xcd, 0xeb, 0x7a, 0x7c, 0x3b, 0x41, 0xb8, 0xae, 0x16, 0x56, 0xe3, 0xfa, 0xf1, 0x9f, 0xc4, 0x6a, 0xda, 0x09, 0x8d, 0xeb, 0x9c, 0x32, 0xb1 ,0xfd, 0x86, 0x62, 0x05, 0x16, 0x5f, 0x49, 0xb8, 0x80})
  checkSum(&result, 32, []byte("Noise_K_25519_ChaChaPoly_BLAKE2s"))
  log.Printf("%x", result)
  temp = result[:]
  checkSum(&result, 32, temp)
  log.Printf("%x", result)
}
