# Setup Fuel Pump


## Local Development

```
cd ~/maestro  #change to repo root
sudo apt-get install -y python3-pip python3-venv
python3 -m venv fuel-pump-env
source fuel-pump-env/bin/activate
pip install -r ./docker/fuel-pump/requirements.txt
mkdir -p ./fuel-pump-env/app
cp ./docker/fuel-pump/fuel-pump.py fuel-pump-env/app/main.py
cd fuel-pump-env/app/
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Build Container

```
docker build -t fuelpump:1.0 -f docker/fuel-pump/dockerfile .
```