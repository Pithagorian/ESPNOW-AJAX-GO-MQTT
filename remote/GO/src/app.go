package src
import(
	"strings"
	//"time"
	mqtt "github.com/eclipse/paho.mqtt.golang"
	"fmt"
	"html/template"
	// "io/ioutil"
	"net/http"

)

var buttonChoice string = ""
var client mqtt.Client
var tpl *template.Template
var colMap = map[string]string{"0": "blue",
"1": "green",
"2": "red",
"3": "yellow",
}
func init() {
	client = connect(messageHandler)
	tpl = template.Must(template.ParseFiles("index.html"))
}

var messageHandler mqtt.MessageHandler = func(c mqtt.Client, m mqtt.Message) {
	//topic := m.Topic()
	msg := string(m.Payload())
	fmt.Println(msg)
	if strings.Compare(msg, "\n") > 0 {
		buttonChoice = msg
	}
}

func Start() {
	sub(client, "numbers")
	http.HandleFunc("/", index)
	http.HandleFunc("/handler", handler(client, "remote_out"))
	http.HandleFunc("/inhandler", inHandler(&buttonChoice))
	http.ListenAndServe(":8080", nil)
	return
}
