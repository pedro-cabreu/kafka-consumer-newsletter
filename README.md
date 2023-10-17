
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

4. Run the python app

```bash
python3 src/views/mainWindow.py
```

5. Ready to go! Now the new notifications will be displayed on the pyqt window.

## License

[GPL-2.0](https://choosealicense.com/licenses/gpl-2.0/)

