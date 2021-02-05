# Client
simulator de dispositivo en python a rabbit

## Uso.
### 1. Construir
```bash
docker build -t client .
```

### 2. Ejecutar (Correr primero el servidor)
```bash
docker run -it --rm --net=servidor_default client
```
