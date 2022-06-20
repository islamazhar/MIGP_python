package pmtBfElgamal

import (
	"bytes"
	"compress/gzip"
	"encoding/json"
	"github.com/willf/bloom"
	"io/ioutil"
	"math/big"
	"pmt-go/elgamal"
	"runtime"
	"sync"
)

const (
	hfNum = 20
)

type ReqPara struct {
	Params int
	SetSize int
	BfLength int
	NumThreads int
	PointCompression bool
}

type QueryMessage struct {
	BfSize int
	BfLength int
	NumThreads int
	PointCompression bool
	PK *elgamal.PublicKey
	EBF []*elgamal.CiphertextByte
}

type ResponseMessage struct {
	Response *elgamal.CiphertextByte
}

type InitializedQueryCTs struct {
	CTofOnes []*elgamal.CiphertextByte
	ebf []*elgamal.CiphertextByte
}

var mutex sync.Mutex

func ReqInit(params int, setSize int, numWorkers int, pointCompression bool) (*elgamal.PublicKey, *elgamal.SecretKey, *ReqPara) {
	pk, sk := elgamal.KeyGen(params, pointCompression)
	bfLength := int(float64(setSize) * (1.44 * float64(hfNum)))
	reqPara := &ReqPara{params, setSize, bfLength, numWorkers, pointCompression}

	return pk, sk, reqPara
}

func QueryGen(pk *elgamal.PublicKey, pwd2check []byte, reqPara *ReqPara, initQueryCTs *InitializedQueryCTs) *QueryMessage {

	ebf := initQueryCTs.ebf
	bf := bloom.New(uint(reqPara.BfLength), uint(hfNum))
	bf.AddString(string(pwd2check))
	bfIndex := []uint64{0}

	for i, j := 0, 0; uint(i) < bf.Cap() && j < len(initQueryCTs.CTofOnes); i++ {
		bfIndex = []uint64{uint64(i)}
		if bf.TestLocations(bfIndex) {
			ebf[i] = initQueryCTs.CTofOnes[j]
			j++
		}
	}
	queryMessage := &QueryMessage{reqPara.SetSize, reqPara.BfLength, reqPara.NumThreads,reqPara.PointCompression, pk, ebf}

	return queryMessage
}

func RespFilterGen(responderSet []string) *bloom.BloomFilter {

	bf := bloom.New(uint(float64(len(responderSet)) * (1.44 * float64(hfNum))), uint(hfNum))
	for i := 0; i < len(responderSet); i++ {
		bf.AddString(responderSet[i])
	}

	return bf
}

func ResponseGen(queryMessage *QueryMessage, bf *bloom.BloomFilter) *ResponseMessage {
	pk := queryMessage.PK
	pk.InitCurve()
	response := homomorphicOps(pk, queryMessage.EBF, bf, queryMessage.NumThreads)
	responseMessage := &ResponseMessage{response}


	return responseMessage
}

func ResponseDecrypt(pk *elgamal.PublicKey, sk *elgamal.SecretKey, reqPara *ReqPara, responseMessage *ResponseMessage) bool {

	ct := pk.Bytes2Ciphertext(responseMessage.Response, pk.PointCompression)
	return sk.DecryptAndCheck0(ct)
}


func homomorphicOps(pk *elgamal.PublicKey, ebf []*elgamal.CiphertextByte, bf *bloom.BloomFilter, numWorkers int) *elgamal.CiphertextByte {

	var respAdd sync.WaitGroup

	chAddBuffs := make(chan *elgamal.Ciphertext, bf.Cap())
	chWorkerAdd := make(chan int, numWorkers)

	for i := 0; uint(i) < bf.Cap(); i++ {
		chWorkerAdd <- 1
		respAdd.Add(1)
		go func(i int) {
			defer respAdd.Done()
			if !bf.TestLocations([]uint64{uint64(i)}) {
				chAddBuffs <- pk.Bytes2Ciphertext(ebf[i], pk.PointCompression)
			}
			<- chWorkerAdd
		}(i)
	}
	respAdd.Wait()

	response := pk.Encrypt(big.NewInt(0))
	for ; len(chAddBuffs) > 0; {
		chWorkerAdd <- 1
		respAdd.Add(1)
		go func() {
			defer respAdd.Done()
			if len(chAddBuffs) != 0 {
				newCT := pk.Add(response, <-chAddBuffs, false)
				mutex.Lock()
				response = newCT
				mutex.Unlock()
			}
			<- chWorkerAdd
		}()

	}
	respAdd.Wait()
	close(chAddBuffs)
	close(chWorkerAdd)
	return pk.Ciphertext2Bytes(response, pk.PointCompression)
}


func ReqEncryptConstants (pk *elgamal.PublicKey, reqPara *ReqPara) *InitializedQueryCTs {
	var reqGen sync.WaitGroup
	chWorker := make(chan int, runtime.GOMAXPROCS(runtime.NumCPU())) // for faster precomputation

	ctOfOnes := make([]*elgamal.CiphertextByte, hfNum*2)
	for i := 0; i < len(ctOfOnes); i++ {
		chWorker <- 1
		reqGen.Add(1)
		go func(i int) {
			defer reqGen.Done()
			ctOfOnes[i] = pk.Ciphertext2Bytes(pk.Encrypt(big.NewInt(1)), pk.PointCompression)
			<- chWorker
		}(i)
	}
	reqGen.Wait()

	ebf := make([]*elgamal.CiphertextByte, reqPara.BfLength)
	for i := 0; i < len(ebf); i++ {
		chWorker <- 1
		reqGen.Add(1)
		go func(i int) {
			defer reqGen.Done()
			c := pk.Encrypt(big.NewInt(0))
			ebf[i] = pk.Ciphertext2Bytes(c, pk.PointCompression)
			<- chWorker
		}(i)
	}
	reqGen.Wait()
	close(chWorker)
	return &InitializedQueryCTs{ctOfOnes, ebf}
}


// This function encodes a query message struct into bytes.
func EncodeQuery(queryMessage *QueryMessage) []byte {

	queryMessageJson, _ := json.Marshal(*queryMessage)
	var b bytes.Buffer
	w := gzip.NewWriter(&b)
	_, err := w.Write(queryMessageJson)
	err = w.Close()
	if err != nil {
		panic(err)
	}
	msg := []byte(b.String())

	return msg
}


// This function decodes a query message in bytes back to struct.
func DecodeQuery(queryMessageBytes []byte) *QueryMessage {

	var queryMessage QueryMessage

	r, err := gzip.NewReader(bytes.NewBuffer(queryMessageBytes))
	if err != nil {
		panic(err)
	}
	jsonQM, err := ioutil.ReadAll(r)
	err = r.Close()
	if err != nil {
		panic(err)
	}

	err = json.Unmarshal(jsonQM, &queryMessage)
	err = r.Close()
	if err != nil {
		panic(err)
	}

	return &queryMessage
}


// This function encodes a response message struct to bytes.
func EncodeResponse(responseMessage *ResponseMessage) []byte {

	responseMessageJson, _ := json.Marshal(*responseMessage)
	var b bytes.Buffer
	w := gzip.NewWriter(&b)
	_, err := w.Write(responseMessageJson)
	err = w.Close()
	if err != nil {
		//fmt.Println("gzip error occurred!!!")
		panic(err)
	}
	msg := []byte(b.String())

	return msg
}

// This function decodes a response message in bytes to struct.
func DecodeResponse(responseMessageBytes []byte) *ResponseMessage {

	var responseMessage ResponseMessage

	r, err := gzip.NewReader(bytes.NewBuffer(responseMessageBytes))
	if err != nil {
		panic(err)
	}
	jsonRM, err := ioutil.ReadAll(r)
	err = r.Close()
	if err != nil {
		panic(err)
	}

	err = json.Unmarshal(jsonRM, &responseMessage)
	if err != nil {
		panic(err)
	}

	return &responseMessage
}