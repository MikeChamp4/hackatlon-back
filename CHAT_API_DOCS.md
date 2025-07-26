# Chat API Documentation

Este documento describe el nuevo endpoint `/chat` que permite interactuar con el modelo Gemma:7B local o remoto.

## Configuración Previa

### 1. Opción A: Instalar Ollama Localmente
```bash
# En Ubuntu/Debian
curl -fsSL https://ollama.ai/install.sh | sh

# En otros sistemas, visita: https://ollama.ai/download
```

### 2. Opción B: Conectar a PC Remoto
Si quieres usar el modelo en el PC de un compañero, ver: [REMOTE_CONNECTION_GUIDE.md](./REMOTE_CONNECTION_GUIDE.md)

### 3. Configurar Variables de Entorno
```bash
# Copiar plantilla
cp .env.example .env

# Editar .env para configurar Ollama
# Para localhost:
OLLAMA_HOST=http://localhost:11434

# Para PC remoto:
OLLAMA_HOST=http://IP_DEL_COMPAÑERO:11434
```

### 4. Descargar el modelo Gemma:7B (Solo si es local)
```bash
ollama pull gemma:7b
```

### 5. Verificar que el modelo está disponible
```bash
ollama list
```

## Endpoints Disponibles

### POST /chat
Envía una consulta al modelo Gemma:7B y obtiene una respuesta.

**Request Body:**
```json
{
    "query": "Tu pregunta aquí"
}
```

**Response (Éxito):**
```json
{
    "success": true,
    "response": "Respuesta del modelo...",
    "model": "gemma:7b",
    "query": "Tu pregunta aquí"
}
```

**Response (Error):**
```json
{
    "success": false,
    "error": "Descripción del error"
}
```

**Ejemplo de uso con curl:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Explícame qué es la inteligencia artificial"}'
```

### GET /chat/model-info
Obtiene información sobre el modelo Gemma:7B actual.

**Response (Éxito):**
```json
{
    "success": true,
    "model_info": {
        "name": "gemma:7b",
        "size": "4.8GB",
        "modified_at": "2024-01-15T10:30:00Z"
    }
}
```

**Ejemplo de uso con curl:**
```bash
curl -X GET http://localhost:8000/chat/model-info
```

## Códigos de Estado HTTP

- **200**: Operación exitosa
- **400**: Request inválido (falta query o está vacía)
- **500**: Error interno del servidor (modelo no disponible, error de conexión con Ollama, etc.)

## Posibles Errores

### Modelo no disponible
```json
{
    "success": false,
    "error": "El modelo gemma:7b no está disponible. Asegúrate de que esté instalado con 'ollama pull gemma:7b'"
}
```

### Query vacía
```json
{
    "error": "La query no puede estar vacía"
}
```

### Ollama no está ejecutándose
```json
{
    "success": false,
    "error": "Error al comunicarse con el modelo: Connection refused"
}
```

## Integración con Frontend

### JavaScript/TypeScript
```javascript
async function sendChatMessage(query) {
    try {
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('Respuesta del modelo:', data.response);
            return data.response;
        } else {
            console.error('Error:', data.error);
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
        throw error;
    }
}

// Uso
sendChatMessage("¿Cómo funciona el aprendizaje automático?")
    .then(response => {
        // Manejar la respuesta
        document.getElementById('chat-response').textContent = response;
    })
    .catch(error => {
        // Manejar errores
        console.error('Error:', error);
    });
```

### React
```jsx
import { useState } from 'react';

function ChatComponent() {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const sendMessage = async () => {
        if (!query.trim()) return;
        
        setLoading(true);
        setError('');
        
        try {
            const res = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });
            
            const data = await res.json();
            
            if (data.success) {
                setResponse(data.response);
            } else {
                setError(data.error);
            }
        } catch (err) {
            setError('Error de conexión con el servidor');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Escribe tu pregunta..."
                rows={4}
                cols={50}
            />
            <br />
            <button onClick={sendMessage} disabled={loading}>
                {loading ? 'Enviando...' : 'Enviar'}
            </button>
            
            {error && <div style={{color: 'red'}}>Error: {error}</div>}
            {response && (
                <div>
                    <h3>Respuesta:</h3>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
}
```

## Consideraciones de Rendimiento

1. **Tiempo de respuesta**: Las consultas pueden tomar varios segundos dependiendo de la complejidad y el hardware.
2. **Memoria**: Gemma:7B requiere aproximadamente 8GB de RAM para funcionar óptimamente.
3. **Concurrencia**: El modelo puede manejar una consulta a la vez por defecto.

## Troubleshooting

### Verificar que Ollama está funcionando
```bash
# Verificar el servicio
systemctl status ollama

# Verificar modelos disponibles
ollama list

# Probar el modelo directamente
ollama run gemma:7b "Hola, ¿cómo estás?"
```

### Logs del servicio
Los errores se registran en los logs de Flask. Verifica la consola donde ejecutas la aplicación para más detalles.
