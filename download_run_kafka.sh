curl https://dlcdn.apache.org/kafka/3.4.0/kafka_2.13-3.4.0.tgz -o kafka_2.13-3.4.0.tgz
tar -xzf kafka_2.13-3.4.0.tgz
cd kafka_2.13-3.4.0
# Start the ZooKeeper service
bin/zookeeper-server-start.sh config/zookeeper.properties
# Start the Kafka broker service
bin/kafka-server-start.sh config/server.properties