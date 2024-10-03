# Web API
## Installation (Linux)
### Create virtual python environment
```python -m venv .venv ```
### Activate venv from directory Ringier/WebAPI/
```source .venv/bin/activate```
### Install requirements
```pip install -r requirements.txt```
### Run app
```python app.py```
### Run tests 
``` python test_app.py```

## Usage
```GET http://127.0.0.1:5000/system-info```

```GET http://127.0.0.1:5000/return-value```

```POST http://127.0.0.1:5000/return-value``` 
(requires json payload)
#### Test POST 
##### Powershell
```Invoke-WebRequest -Uri http://127.0.0.1:5000/return-value `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"return_value":12}' `
  -UseBasicParsing```
##### Bash
```
curl -X POST 127.0.0.1:5000/return-value -H "Content-Type: application/json" -d '{"return_value": 17}'
```
