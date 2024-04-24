package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"
)

const expectedToken = "sk-123" // 这里填你的密钥

// EventStream 结构体用于生成事件流格式数据
type EventStream struct {
	ID                string `json:"id"`
	Object            string `json:"object"`
	Created           int64  `json:"created"`
	Model             string `json:"model"`
	SystemFingerprint string `json:"system_fingerprint"`
	Choices           []struct {
		Index         int    `json:"index"`
		Message       Message `json:"message"`
		Logprobs      *int   `json:"logprobs"`
		FinishReason  string `json:"finish_reason"`
	} `json:"choices"`
}

// Message 结构体用于表示变化的内容
type Message struct {
	Role    string `json:"role,omitempty"`
	Content string `json:"content,omitempty"`
}

func main() {
	http.HandleFunc("/v1/chat/completions", handleRequest)
	fmt.Println("Server is running on port 8080")
	http.ListenAndServe(":8080", nil)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
	// 设置跨域头部
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
	w.Header().Set("Access-Control-Allow-Headers", "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")

	// 验证 Authorization 头部和令牌
	authHeader := r.Header.Get("Authorization")
	if authHeader != fmt.Sprintf("Bearer %s", expectedToken) {
		http.Error(w, "无效的令牌", http.StatusUnauthorized)
		return
	}

	// 确保请求是 POST 请求，并且路径正确
	if r.Method != "POST" {
		http.Error(w, "Not found", http.StatusNotFound)
		return
	}

	// 读取请求体
	var requestBody map[string]interface{}
	if err := json.NewDecoder(r.Body).Decode(&requestBody); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	stream, ok := requestBody["stream"].(bool)
	if !ok {
		http.Error(w, "stream 参数缺失或类型错误", http.StatusBadRequest)
		return
	}

	// 构造新的请求发送到目标 API
	url := "https://multillm.ai-pro.org/api/openai-completion"
	client := &http.Client{}

	// Convert requestBody to JSON
	requestBodyBytes, err := json.Marshal(requestBody)
	if err != nil {
		http.Error(w, "Failed to convert requestBody to JSON", http.StatusInternalServerError)
		return
	}

	req, err := http.NewRequest("POST", url, strings.NewReader(string(requestBodyBytes)))
	if err != nil {
		http.Error(w, "创建请求失败", http.StatusInternalServerError)
		return
	}
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, "无法连接到后端 API", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	// 如果 stream 参数为 true，则使用事件流格式发送响应
	if stream {
		w.Header().Set("Content-Type", "text/event-stream")
		w.Header().Set("Cache-Control", "no-cache")
		w.Header().Set("Connection", "keep-alive")

		var responseData EventStream
		if err := json.NewDecoder(resp.Body).Decode(&responseData); err != nil {
			http.Error(w, "解析响应失败", http.StatusInternalServerError)
			return
		}

		// 分割内容并发送
		chunks := strings.Split(responseData.Choices[0].Message.Content, " ")
		for _, chunk := range chunks {
			fmt.Fprintf(w, "data: %s\n\n", chunk)
			flusher, ok := w.(http.Flusher)
			if ok {
				flusher.Flush()
			}
			time.Sleep(1 * time.Second) // 延迟发送，模拟流式效果
		}
	} else {
		// 如果不是流式响应，则直接返回响应数据
		io.Copy(w, resp.Body)
	}
}
