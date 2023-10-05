
# Kafka Consumer 
A simple python app that consumes a kafka server.


## Run Locally

1. Run the zookeeper

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties

```

2. Run the Kafka Server

```bash
bin/kafka-server-start.sh config/server.properties
```

3. Run the producer

```bash
bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092
```


## License

[GPL-2.0](https://choosealicense.com/licenses/gpl-2.0/)

