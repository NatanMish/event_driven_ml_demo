# Event Driven Machine Learning Demo
This is a demo of an event driven machine learning application. The application allowsa user to simulate data based on a linear regression model...

## Getting Started
### Prerequisites
* Python 3.8 or higher
* Poetry
* Docker
* Minikube
* Kubectl

### Installing
1. Clone the repository
2. Install dependencies
```bash
poetry install
```
3. Start minikube
```bash
minikube start
```
4. Deploy  Kafka and Zookeeper
```bash
kubectl apply -f kafka_kubernetes.yaml
```
Once the zookeeper pods are running, update the kafka_kubernetes/kafka.yaml file with the IP address of the zookeeper pods. Then redeploy the kafka pods.
5. Mount the minikube virtual machine to the local file system
```bash
minikube mount /Users:/Users
```
6. Build and push the FastAPI image to your docker registry
```bash
docker build -t <your_docker_registry>/online_learner:latest .
docker push <your_docker_registry>/online_learner:latest
```
