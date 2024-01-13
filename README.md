# Pod Info
Container image that return info about the running pod

### Paths

- `/`: web page
- `/json`: info as json

```json
{
    "hostname": "1c314e3d63cd",
    "ip": "172.17.0.2",
    "method": "GET",
    "namespace": "",
    "remote_addr": "172.17.0.1",
    "uri": "/json"
}
```

### Build
```bash
docker build -t pod-info:1.0.0 . 
```

### Run
```bash
docker run -p 8080:8080 --name pod-indo pod-info:1.0.0
```