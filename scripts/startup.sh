maestro up 0 &
sleep 60
kubectl port-forward svc/mosquitto-service 1884:1883 &
kubectl port-forward svc/opera-service 3001:3000 &
