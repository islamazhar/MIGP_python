package elgamal

import (
	"crypto/elliptic"
	"crypto/rand"
	"log"
	"math/big"
	"os"
)

type PublicKey struct {
	Curve *elliptic.Curve
	SecParam int
	Hx *big.Int
	Hy *big.Int
	PointCompression bool
}

type SecretKey struct {
	Curve *elliptic.Curve
	Hx *big.Int
	Hy *big.Int
	Priv []byte
}

type Ciphertext struct {
	C1x *big.Int
	C1y *big.Int
	C2x *big.Int
	C2y *big.Int
}

type CiphertextByte struct {
	C1 []byte
	C2 []byte
}

// This function generates a EC-ElGamal key pair
func KeyGen(secParam int, pointCompression bool) (*PublicKey, *SecretKey) {

	curve := *(initCurve(secParam))
	priv, Hx, Hy, _ := elliptic.GenerateKey(curve, rand.Reader)
	// create public key
	pk := &PublicKey{&curve, secParam,Hx, Hy, pointCompression}
	// create secret key
	sk := &SecretKey{&curve, Hx, Hy, priv}
	return pk, sk
}

// This function, given a public key, encrypts a plaintext message
// and return a ciphertext
func (pk *PublicKey) Encrypt(m *big.Int) *Ciphertext {

	curve := *pk.Curve
	z := NewCryptoRandom(curve.Params().N.Bytes())
	c1x, c1y := curve.ScalarBaseMult(z)
	Hzx, Hzy := curve.ScalarMult(pk.Hx, pk.Hy, z)
	gmx, gmy := curve.ScalarBaseMult(m.Bytes())
	c2x, c2y := curve.Add(gmx, gmy, Hzx, Hzy)

	c := &Ciphertext{c1x, c1y, c2x, c2y}

	return c
}

// This function, given a secret key, checks if the input ciphertext is an
// encryption of the input plaintext
func (sk *SecretKey) DecryptAndCheck(c *Ciphertext, test []byte) bool {
	curve := *sk.Curve
	tempx, tempy := curve.ScalarMult(c.C1x, c.C1y, sk.Priv)
	gmx, gmy := curve.ScalarBaseMult(test)
	resx, resy := curve.Add(tempx, tempy, gmx, gmy)
	if (resx.Cmp(c.C2x) == 0) && (resy.Cmp(c.C2y) == 0) {
		return true
	}
	return false
}

// This function, given a secret key, checks if the input ciphertext is an
// encryption of zero
func (sk *SecretKey) DecryptAndCheck0(c *Ciphertext) bool {
	curve := *sk.Curve
	tempx, tempy := curve.ScalarMult(c.C1x, c.C1y, sk.Priv)
	if (tempx.Cmp(c.C2x) == 0) && (tempy.Cmp(c.C2y) == 0) {
		return true
	}
	return false
}

// This function, given a public key, homomorphically add two ciphertexts
// together and returns a ciphertext of their sum. The function will re-randomize
// the resulting ciphertext (can be seen as homomorphic addition with an encryption of zero)
// if the input boolean variable "rand" is set to true.
func (pk *PublicKey) Add(cA, cB *Ciphertext, rand bool) *Ciphertext {
	curve := *pk.Curve
	ctemp1x, ctemp1y := curve.Add(cA.C1x, cA.C1y, cB.C1x, cB.C1y)
	ctemp2x, ctemp2y := curve.Add(cA.C2x, cA.C2y, cB.C2x, cB.C2y)

	if rand {
		zeroCT := pk.Encrypt(big.NewInt(0))
		randCtemp1x, randCtemp1y := curve.Add(ctemp1x, ctemp1y, zeroCT.C1x, zeroCT.C1y)
		randCtemp2x, randCtemp2y := curve.Add(ctemp2x, ctemp2y, zeroCT.C2x, zeroCT.C2y)
		c := &Ciphertext{randCtemp1x, randCtemp1y, randCtemp2x, randCtemp2y}
		return c
	}
	c := &Ciphertext{ctemp1x, ctemp1y, ctemp2x, ctemp2y}
	return c
}

// This function, given a public key, achieves scalar multiplication on the
// input ciphertext with a given scalar. The function will re-randomize the
//// resulting ciphertext (can be seen as homomorphic addition with an encryption of zero)
//// if the input boolean variable "rand" is set to true.
func (pk *PublicKey) ScalarMult(cA *Ciphertext, scalar *big.Int, rand bool) *Ciphertext {
	curve := *pk.Curve
	ctemp1x, ctemp1y := curve.ScalarMult(cA.C1x, cA.C1y, scalar.Bytes())
	ctemp2x, ctemp2y := curve.ScalarMult(cA.C2x, cA.C2y, scalar.Bytes())

	if rand {
		zeroCT := pk.Encrypt(big.NewInt(0))
		curve := *pk.Curve
		randCtemp1x, randCtemp1y := curve.Add(ctemp1x, ctemp1y, zeroCT.C1x, zeroCT.C1y)
		randCtemp2x, randCtemp2y := curve.Add(ctemp2x, ctemp2y, zeroCT.C2x, zeroCT.C2y)
		c := &Ciphertext{randCtemp1x, randCtemp1y, randCtemp2x, randCtemp2y}
		return c
	}

	c := &Ciphertext{ctemp1x, ctemp1y, ctemp2x, ctemp2y}
	return c
}

// This function, given a public key, achieves scalar multiplication on the
// input ciphertext with a randomly chosen scalar from Zn. The function will re-randomize the
// resulting ciphertext (can be seen as homomorphic addition with an encryption of zero)
// if the input boolean variable "rand" is set to true.
func (pk *PublicKey) ScalarMultRandomizer(cA *Ciphertext, rand bool) *Ciphertext {
	curve := *pk.Curve
	scalar := NewCryptoRandom(curve.Params().N.Bytes())

	ctemp1x, ctemp1y := curve.ScalarMult(cA.C1x, cA.C1y, scalar)
	ctemp2x, ctemp2y := curve.ScalarMult(cA.C2x, cA.C2y, scalar)

	if rand {
		zeroCT := pk.Encrypt(big.NewInt(0))
		randCtemp1x, randCtemp1y := curve.Add(ctemp1x, ctemp1y, zeroCT.C1x, zeroCT.C1y)
		randCtemp2x, randCtemp2y := curve.Add(ctemp2x, ctemp2y, zeroCT.C2x, zeroCT.C2y)
		c := &Ciphertext{randCtemp1x, randCtemp1y, randCtemp2x, randCtemp2y}
		return c
	}

	c := &Ciphertext{ctemp1x, ctemp1y, ctemp2x, ctemp2y}
	return c
}

// This function returns a ciphertext of the inverse of the input plaintext
func (pk *PublicKey) EncryptInv(m *big.Int) *Ciphertext {
	curve := *pk.Curve
	return pk.Encrypt(m.Sub(curve.Params().N, m))
}

// This function returns a random number smaller than max
func NewCryptoRandom(max []byte) []byte {
	maxInt := big.NewInt(0).SetBytes(max)
	randNum, err := rand.Int(rand.Reader, maxInt)
	if err != nil {
		log.Println(err)
	}

	return randNum.Bytes()
}

// This function initializes and returns the chosen curve
func initCurve(secParam int) *elliptic.Curve {
	//curve := elliptic.P192()
	var curve elliptic.Curve

	if secParam == 224 {
		curve = elliptic.P224()
	} else if secParam == 256 {
		curve = elliptic.P256()
	} else if secParam == 384 {
		curve = elliptic.P384()
	} else if secParam == 521 {
		curve = elliptic.P521()
	} else {}

	return &curve
}

//This function initializes a curve under the public key
func (pk *PublicKey) InitCurve() {
	pk.Curve = initCurve(pk.SecParam)
}


// This function encodes a ciphertext struct to bytes
func (pk *PublicKey) Ciphertext2Bytes(ciphertext *Ciphertext, pointCompression bool) *CiphertextByte {
	var C1, C2 []byte
	curve := *pk.Curve
	if pointCompression {
		C1 = elliptic.MarshalCompressed(curve, ciphertext.C1x, ciphertext.C1y)
		C2 = elliptic.MarshalCompressed(curve, ciphertext.C2x, ciphertext.C2y)
	} else {
		C1 = elliptic.Marshal(curve, ciphertext.C1x, ciphertext.C1y)
		C2 = elliptic.Marshal(curve, ciphertext.C2x, ciphertext.C2y)
	}

	ciphertextBytes := &CiphertextByte{C1, C2}
	return ciphertextBytes
}

// This function decodes ciphertext bytes back to a ciphertext struct
func (pk *PublicKey) Bytes2Ciphertext(ciphertextBytes *CiphertextByte, pointCompression bool) *Ciphertext {
	var C1x, C1y, C2x, C2y *big.Int
	curve := *pk.Curve
	if pointCompression {
		C1x, C1y = elliptic.UnmarshalCompressed(curve, ciphertextBytes.C1)
		C2x, C2y = elliptic.UnmarshalCompressed(curve, ciphertextBytes.C2)
	} else {
		C1x, C1y = elliptic.Unmarshal(curve, ciphertextBytes.C1)
		C2x, C2y = elliptic.Unmarshal(curve, ciphertextBytes.C2)
	}
	ciphertext := &Ciphertext{C1x, C1y, C2x, C2y}
	if !pk.CheckOnCurve(ciphertext) {
		os.Exit(1) // ill-formed ciphertexts detected
	}
	return ciphertext
}

// This function checks if a given ciphertext is a well-formed ciphertext
func (pk *PublicKey) CheckOnCurve(ciphertext *Ciphertext) bool {
	curve := *pk.Curve
	return curve.IsOnCurve(ciphertext.C1x, ciphertext.C1y) && curve.IsOnCurve(ciphertext.C2x, ciphertext.C2y)
}

