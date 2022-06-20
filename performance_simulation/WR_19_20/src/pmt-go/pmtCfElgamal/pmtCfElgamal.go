package pmtCfElgamal

import (
	"bytes"
	"compress/gzip"
	"encoding/json"
	"io/ioutil"
	"math/big"
	"pmt-go/cuckoofilter"
	"pmt-go/elgamal"
	"runtime"
	"sync"
)

type ReqPara struct {
	CfSize int
	NumThreads int
}

type QueryMessage struct {
	CfSize int
	NumThreads int
	PointCompression bool
	PK *elgamal.PublicKey
	ECF1 []*elgamal.CiphertextByte
	ECF2 []*elgamal.CiphertextByte
	EPWD *elgamal.CiphertextByte
}

type ResponseMessage struct {
	Response []*elgamal.CiphertextByte
}

type InitializedQueryCTs struct {
	ECF1 []*elgamal.CiphertextByte
	ECF2 []*elgamal.CiphertextByte
	CTofOne1 *elgamal.CiphertextByte
	CTofOne2 *elgamal.CiphertextByte
}

func ReqInit(params int, cfSize int, numWorkers int, pointCompression bool) (*elgamal.PublicKey, *elgamal.SecretKey, *ReqPara) {

	pk, sk := elgamal.KeyGen(params, pointCompression)
	reqData := &ReqPara{cfSize, numWorkers}
	return pk, sk, reqData
}

func QueryGen(pk *elgamal.PublicKey, pwd2check []byte, reqPara *ReqPara, initQueryCTs *InitializedQueryCTs) *QueryMessage {
	cf := cuckoofilter.InitCFilter(uint(reqPara.CfSize))
	ecf1 := initQueryCTs.ECF1
	ecf2 := initQueryCTs.ECF2
	fp, i1, i2:= cuckoofilter.GetFPI1I2(pwd2check, cf.GetNumBuckets())
	ecf1[i1] = initQueryCTs.CTofOne1
	ecf2[i2] = initQueryCTs.CTofOne2
	epwd := pk.Ciphertext2Bytes(pk.EncryptInv(big.NewInt(0).SetBytes(fp)), pk.PointCompression)
	queryMessage := &QueryMessage{reqPara.CfSize, reqPara.NumThreads, pk.PointCompression, pk, ecf1, ecf2, epwd}

	return queryMessage
}

func RespFilterGen(responderSet []string) [][]*big.Int {

	var encodedCF [][]*big.Int

	cf := cuckoofilter.InitCFilter(uint(len(responderSet)))
	for i:=0; i < len(responderSet); i++ {
		if !(cf.Add([]byte(responderSet[i]))) {
			break
		}
	}
	//fmt.Println("[CF] # of items in the CF: >>>", cf.GetCount())

	for j := 0; j < cuckoofilter.GetBucketSize(); j++ {
		var encodedCFSeq []*big.Int
		for i := 0; i < len(cf.Filter2Bytes()); i++ {
			func(i int) {
				if i % cuckoofilter.GetBucketSize() == j {
					encodedCFSeq = append(encodedCFSeq, big.NewInt(0).SetBytes(cf.Filter2Bytes()[i]))
				}
			}(i)
		}
		encodedCF = append(encodedCF, encodedCFSeq)
	}

	return encodedCF
}

func ResponseGen(queryMessage *QueryMessage, encodedCF [][]*big.Int) *ResponseMessage {

	var response []*elgamal.CiphertextByte
	resultResp := make(chan *elgamal.Ciphertext, 2 * cuckoofilter.GetBucketSize())
	pk := queryMessage.PK
	pk.InitCurve()

	homomorphicOps(pk, queryMessage.ECF1, encodedCF, queryMessage.EPWD, resultResp, queryMessage.NumThreads)
	homomorphicOps(pk, queryMessage.ECF2, encodedCF, queryMessage.EPWD, resultResp, queryMessage.NumThreads)
	for i := 0; i < 2 * cuckoofilter.GetBucketSize(); i++ {
		response = append(response, queryMessage.PK.Ciphertext2Bytes(<- resultResp, queryMessage.PK.PointCompression))
	}

	responseMessage := &ResponseMessage{response}
	close(resultResp)
	return responseMessage
}

func ResponseDecrypt(pk *elgamal.PublicKey, sk *elgamal.SecretKey, reqPara *ReqPara, responseMessage *ResponseMessage) bool {
	var respDec sync.WaitGroup
	chWorker := make(chan int, reqPara.NumThreads)
	chPositives := make(chan bool, len(responseMessage.Response))

	defer close(chWorker)
	defer close(chPositives)

	for i := 0; i < len(responseMessage.Response); i++ {
		chWorker <- 1
		respDec.Add(1)
		go func(i int) {
			defer respDec.Done()
			ct := pk.Bytes2Ciphertext(responseMessage.Response[i], pk.PointCompression)
			if sk.DecryptAndCheck0(ct) {
				chPositives <- true
			}
			<- chWorker
		}(i)
	}
	respDec.Wait()

	if len(chPositives) > 0 {
		return true
	} else {
		return false
	}

}


func ReqEncryptConstants(pk *elgamal.PublicKey, reqPara *ReqPara) *InitializedQueryCTs {
	cf := cuckoofilter.InitCFilter(uint(reqPara.CfSize))
	ecf1, ecf2 := all0ecfGenReq(pk, int(cf.GetNumBuckets()))
	ctOne1 := pk.Ciphertext2Bytes(pk.Encrypt(big.NewInt(1)), pk.PointCompression)
	ctOne2 := pk.Ciphertext2Bytes(pk.Encrypt(big.NewInt(1)), pk.PointCompression)
	pk.Ciphertext2Bytes(pk.Encrypt(big.NewInt(1)), pk.PointCompression)
	return &InitializedQueryCTs{ecf1, ecf2, ctOne1, ctOne2}
}

func all0ecfGenReq(pk *elgamal.PublicKey, numBuckets int) ([]*elgamal.CiphertextByte, []*elgamal.CiphertextByte) {
	var reqGen sync.WaitGroup

	ecf1 := make([]*elgamal.CiphertextByte, numBuckets)
	ecf2 := make([]*elgamal.CiphertextByte, numBuckets)
	chWorker := make(chan int, runtime.GOMAXPROCS(runtime.NumCPU())) // for faster precomputation

	for i := 0; i < numBuckets; i++ {
		chWorker <- 1
		reqGen.Add(1)
		go func(i int) {
			defer reqGen.Done()
			c := pk.Encrypt(big.NewInt(0))
			ecf1[i] = pk.Ciphertext2Bytes(c, pk.PointCompression)
			<- chWorker
		}(i)
	}

	for i := 0; i < numBuckets; i++ {
		chWorker <- 1
		reqGen.Add(1)
		go func(i int) {
			defer reqGen.Done()
			c := pk.Encrypt(big.NewInt(0))
			ecf2[i] = pk.Ciphertext2Bytes(c, pk.PointCompression)
			<- chWorker
		}(i)
	}

	reqGen.Wait()
	close(chWorker)
	return ecf1, ecf2
}

func homomorphicOps(pk *elgamal.PublicKey, ecfReq []*elgamal.CiphertextByte, ecfResp [][]*big.Int, epwd *elgamal.CiphertextByte, resultResp chan *elgamal.Ciphertext, numWorkers int) {
	var respMult sync.WaitGroup
	var respAdd sync.WaitGroup

	//if len(ecfReq) != len(ecfResp[0]){
	//	fmt.Println(len(ecfReq))
	//	fmt.Println(len(ecfResp))
	//	fmt.Println(len(ecfResp[0]))
	//	fmt.Println("Something went wrong with Cuckoo filters.")
	//}

	chMultiBuffs := make([]chan*elgamal.Ciphertext, cuckoofilter.GetBucketSize())
	chWorkerMulti := make(chan int, numWorkers)
	chWorkerAdd := make(chan int, numWorkers)

	for j := 0; j < len(ecfResp); j++ {
		chMultiBuffs[j] = make(chan *elgamal.Ciphertext, len(ecfReq))
		for i := 0; i < len(ecfReq); i++ {
			chWorkerMulti <- 1
			respMult.Add(1)
			go func(i int, j int) {
				defer respMult.Done()
				c := pk.Bytes2Ciphertext(ecfReq[i], pk.PointCompression)
				ct := pk.ScalarMult(c, ecfResp[j][i], false)
				chMultiBuffs[j] <- ct
				<- chWorkerMulti
			}(i, j)
		}
	}
	respMult.Wait()
	close(chWorkerMulti)

	epwdCT := pk.Bytes2Ciphertext(epwd, pk.PointCompression)
	for j := 0; j < len(chMultiBuffs); j++ {
		chWorkerAdd <- 1
		respAdd.Add(1)
		go func(j int) {
			defer respAdd.Done()
			res := <-chMultiBuffs[j]
			for i := 0; len(chMultiBuffs[j]) > 0; i++ {
				res = pk.Add(res, <-chMultiBuffs[j], false)
			}
			res = pk.Add(res, epwdCT, false)
			res = pk.ScalarMultRandomizer(res, false)
			resultResp <- res
			<-chWorkerAdd
		}(j)
	}
	respAdd.Wait()

	close(chWorkerAdd)
	for i := 0; i < len(chMultiBuffs); i++ {
		close(chMultiBuffs[i])
	}
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