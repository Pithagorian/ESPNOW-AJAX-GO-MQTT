package src

import (
	"fmt"
	"strings"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

func connect(messageHandler mqtt.MessageHandler) mqtt.Client {
	var broker = "192.168.xx.xx"
	var port = 1883
	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tcp://%s:%d", broker, port))
	opts.SetClientID("golang")
	// opts.SetUsername("emqx")
	// opts.SetPassword("public")

	opts.SetDefaultPublishHandler(messageHandler)
	opts.OnConnect = connectHandler
	opts.OnConnectionLost = connectLostHandler
	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
	return client
}

var messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
	//topic := msg.Topic()
	payload := msg.Payload()
	if strings.Compare(string(payload), "\n") > 0 {
		fmt.Printf("last msg: %s\n", payload)
	}
	if strings.Compare("bye\n", string(payload)) == 0 {
		fmt.Println("exitting")
	}
}
var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
	fmt.Println("Connected")
}
var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
	fmt.Printf("Connect lost: %v", err)
}

func publish(client mqtt.Client, topic string, msg string) {
	text := fmt.Sprintf("%s", msg)
	token := client.Publish("remote_out", 0, false, text)
	token.Wait()
	// fmt.Println(token.Error())
	// num := 10
	// for i := 0; i < num; i++ {
	// 	text := fmt.Sprintf("Message %d", i)
	// 	token := client.Publish("topic/test", 0, false, text)
	// 	token.Wait()
	// 	time.Sleep(time.Second)
	// }
}

func sub(client mqtt.Client, topic string) {
	token := client.Subscribe(topic, 1, nil)
	token.Wait()
	fmt.Println(token.Error())
	fmt.Printf("Subscribed to topic: %s", topic)
}
