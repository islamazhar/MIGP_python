package cuckoofilter

import (
	"bytes"
	"crypto/sha256"
	"hash/fnv"
	"math/rand"
	"strconv"
)

const (
	BUCKET_SIZE = 16 // increasing bucket_size will reduce query message size but increase response message size
	MAX_KICK_NUM = 1024 // Max number of kicks allowed
	FP_SEED = 2020 // Seeds for calculating fingerprints (SHA256)
	CAPACITY_FACTOR = 0.95 // Increase the filter's size by a factor to allow better capacity
)

type CFilter struct {
	buckets [][BUCKET_SIZE][]byte
	setSize uint
	numBuckets uint
	bucketSize int
}

// This function initializes a filter given the size of input set
func InitCFilter(setSize uint) *CFilter {

	numBuckets := uint(float32(setSize) / CAPACITY_FACTOR) / BUCKET_SIZE + 1
	buckets := make([][BUCKET_SIZE][]byte, numBuckets)
	return &CFilter{buckets, setSize, numBuckets, BUCKET_SIZE}
}

// This function add one element into the current filter
func (cf *CFilter) Add(element []byte) bool {

	fp, i1, i2 := GetFPI1I2(element, cf.numBuckets)
	if cf.insert(fp, i1) || cf.insert(fp, i2) {
		return true
	} else {
		for i := 0; i < MAX_KICK_NUM; i++ {
			ix := [2]uint{i1, i2}[rand.Intn(2)]
			jx := rand.Intn(BUCKET_SIZE)
			currFp := fp
			fp = cf.buckets[ix][jx]
			cf.buckets[ix][jx] = currFp
			if cf.insert(fp, getI2(fp, ix, cf.numBuckets)) {
				return true
			}
		}
		return false
	}
}

// This function encode the current filter into []bytes
func (cf *CFilter) Filter2Bytes() [][]byte {

	res := make([][]byte, cf.numBuckets * BUCKET_SIZE)
	for i, bucket := range cf.buckets {
		for j, cell := range bucket {
			index := (i * len(bucket)) + j
			res[index] = cell
		}
	}
	return res
}

// This function returns # of buckets
func (cf *CFilter) GetNumBuckets() uint {
	return cf.numBuckets
}

/////////////////////////////////////////

// This function returns a SHA224 hash output as the fingerprint of
// the given input element
func GetFP(element []byte) []byte {

	h := sha256.New224()
	h.Write(append(element, []byte(strconv.Itoa(FP_SEED))...))
	fp := h.Sum(nil)
	return fp
}

// This function returns an index (of a bucket) for the given input element
func getI1(element []byte, numBuckets uint) uint {

	return hashFunction(element, numBuckets)
}

// This function returns an alternative index (of a bucket) for the given
// input element
func getI2(fp []byte, i uint, numBuckets uint) uint {

	return (i ^ hashFunction(fp, numBuckets)) % numBuckets
}

// This function returns a SHA224 fingerprint and two indexes for the given
// input element
func GetFPI1I2(element []byte, numBuckets uint) ([]byte, uint, uint) {

	fp := GetFP(element)
	i1 := getI1(element, numBuckets)
	i2 := getI2(fp, i1, numBuckets)
	return fp, i1, i2
}


func GetBucketSize() int {

	return BUCKET_SIZE
}

// This function inserts a fingerprint to the bucket with the given
// index, and returns true if succeeds.
func (cf *CFilter) insert(fp []byte, index uint) bool {

	for i, currFp := range cf.buckets[index] {
		if bytes.Equal(currFp, []byte("")) {
			cf.buckets[index][i] = fp
			return true
		}
	}
	return false
}

// This function returns a hash value in the range of [0, numBuckets)
func hashFunction(input []byte, numBuckets uint) uint {

	newHash := fnv.New32a()
	_, err := newHash.Write(input)
	if err != nil {
		panic(err)
	}
	return uint(newHash.Sum32() >> 4) % numBuckets
}