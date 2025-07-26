# 🔗 Configuración para Conectar a PC Remoto

## 📍 **¿Dónde se llama al modelo?**

El modelo se llama desde **`app/services/chat_service.py`** en la línea **37**:

```python
# Línea 37 - Aquí es donde se hace la llamada
response = client.chat(
    model=service.model_name,
    messages=[
        {
            'role': 'user',
            'content': query
        }
    ]
)
```

## 🌐 **Cómo conectarte al PC de tu compañero**

### **Paso 1: Configurar la URL de Ollama**

Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

### **Paso 2: Editar el archivo .env**

```bash
# Cambia esta línea en el archivo .env:
OLLAMA_HOST=http://IP_DE_TU_COMPAÑERO:11434

# Ejemplos:
# OLLAMA_HOST=http://192.168.1.100:11434
# OLLAMA_HOST=http://10.0.0.50:11434
# OLLAMA_HOST=http://172.16.0.25:11434
```

### **Paso 3: Obtener la IP del PC de tu compañero**

Tu compañero debe ejecutar en su PC:

```bash
# En Linux/Mac
ip addr show | grep inet

# En Windows
ipconfig

# O más simple
hostname -I
```

### **Paso 4: Configurar Ollama en el PC de tu compañero**

Tu compañero debe configurar Ollama para aceptar conexiones externas:

#### **Opción A: Variable de entorno (Recomendado)**
```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

#### **Opción B: Servicio systemd (Linux)**
```bash
# Editar el archivo de servicio
sudo systemctl edit ollama

# Agregar:
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"

# Reiniciar
sudo systemctl restart ollama
```

### **Paso 5: Verificar la conexión**

```bash
# Desde tu PC, prueba la conexión
curl http://IP_DE_TU_COMPAÑERO:11434/api/tags

# Debe devolver la lista de modelos disponibles
```

### **Paso 6: Probar el endpoint**

```bash
# Ejecutar el script de pruebas
OLLAMA_HOST=http://IP_DE_TU_COMPAÑERO:11434 python test_chat.py

# O probar directamente
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hola desde remoto!"}'
```

## 🔥 **Ejemplo completo**

Si tu compañero tiene IP `192.168.1.100`, tu archivo `.env` debe tener:

```bash
OLLAMA_HOST=http://192.168.1.100:11434
```

Y tu compañero debe ejecutar:

```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

## 🚨 **Troubleshooting**

### **Error de conexión**
```bash
# Verificar que el puerto esté abierto
telnet IP_DE_TU_COMPAÑERO 11434

# Verificar firewall (tu compañero)
sudo ufw allow 11434
```

### **Modelo no encontrado**
```bash
# Tu compañero debe tener el modelo
ollama pull gemma:7b
ollama list
```

### **Verificar configuración actual**
```bash
# Ver la configuración actual
curl http://localhost:8000/chat/model-info
```

## 📝 **Resumen del flujo**

1. **Tu compañero**: Configura Ollama para aceptar conexiones externas
2. **Tu compañero**: Tiene el modelo Gemma:7B descargado
3. **Tú**: Configuras `OLLAMA_HOST` en tu `.env`
4. **Tú**: Ejecutas tu aplicación Flask
5. **Frontend**: Envía requests a tu Flask API
6. **Tu Flask API**: Se conecta al Ollama de tu compañero
7. **Respuesta**: Viene del modelo en el PC de tu compañero

```
Frontend → Tu Flask API → PC Compañero (Ollama + Gemma:7B) → Respuesta
```
