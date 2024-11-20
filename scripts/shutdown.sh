pkill -xf "kubectl port-forward svc/opera-service 3001:3000"
pkill -xf "kubectl port-forward svc/mosquitto-service 1884:1883"
pkill -xf "maestro up 0"
