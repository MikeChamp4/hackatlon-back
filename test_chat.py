#!/usr/bin/env python3
"""
Script de prueba para el endpoint /chat
"""

import requests
import json
import sys
import os

def test_chat_endpoint():
    """Prueba el endpoint /chat"""
    base_url = "http://localhost:8000"
    
    print("🧪 Iniciando pruebas del endpoint /chat...")
    
    # Mostrar configuración actual
    ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    print(f"🔧 Ollama configurado en: {ollama_host}")
    
    # Test 1: Verificar información del modelo
    print("\n📋 Test 1: Verificando información del modelo...")
    try:
        response = requests.get(f"{base_url}/chat/model-info")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Modelo disponible:")
                model_info = data.get('model_info', {})
                print(f"   - Nombre: {model_info.get('name', 'N/A')}")
                print(f"   - Tamaño: {model_info.get('size', 'N/A')}")
            else:
                print(f"❌ Error obteniendo info del modelo: {data.get('error')}")
                return False
        else:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. ¿Está ejecutándose en localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    # Test 2: Enviar una consulta simple
    print("\n💬 Test 2: Enviando consulta simple...")
    test_query = "Hola, ¿puedes explicarme en una línea qué es Python?"
    
    try:
        payload = {"query": test_query}
        response = requests.post(
            f"{base_url}/chat",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=60  # 60 segundos de timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Respuesta recibida exitosamente:")
                print(f"   - Query: {data.get('query', 'N/A')}")
                print(f"   - Modelo: {data.get('model', 'N/A')}")
                print(f"   - Respuesta: {data.get('response', 'N/A')[:200]}...")
            else:
                print(f"❌ Error en la respuesta: {data.get('error')}")
                return False
        else:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Timeout: La consulta tardó más de 60 segundos")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    # Test 3: Validar error con query vacía
    print("\n🚫 Test 3: Probando validación con query vacía...")
    try:
        payload = {"query": ""}
        response = requests.post(
            f"{base_url}/chat",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 400:
            print("✅ Validación de query vacía funciona correctamente")
        else:
            print(f"❌ Se esperaba código 400, se obtuvo {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    # Test 4: Validar error sin query
    print("\n🚫 Test 4: Probando validación sin campo query...")
    try:
        payload = {"mensaje": "test"}  # Campo incorrecto
        response = requests.post(
            f"{base_url}/chat",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 400:
            print("✅ Validación de campo requerido funciona correctamente")
        else:
            print(f"❌ Se esperaba código 400, se obtuvo {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    return True

def check_prerequisites():
    """Verifica los prerequisitos antes de ejecutar las pruebas"""
    print("🔍 Verificando prerequisitos...")
    
    # Verificar que ollama esté instalado
    import subprocess
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama está instalado y funcionando")
            if 'gemma:7b' in result.stdout:
                print("✅ Modelo gemma:7b está disponible")
                return True
            else:
                print("❌ Modelo gemma:7b no encontrado")
                print("💡 Ejecuta: ollama pull gemma:7b")
                return False
        else:
            print("❌ Ollama no está funcionando correctamente")
            return False
    except FileNotFoundError:
        print("❌ Ollama no está instalado")
        print("💡 Instala Ollama desde: https://ollama.ai/download")
        return False

if __name__ == "__main__":
    print("🤖 Test Suite para Chat API con Gemma:7B")
    print("=" * 50)
    
    if not check_prerequisites():
        print("\n❌ Los prerequisitos no se cumplen. Por favor, instala Ollama y el modelo gemma:7b")
        sys.exit(1)
    
    if test_chat_endpoint():
        print("\n🎊 ¡Todos los tests pasaron! El endpoint /chat está funcionando correctamente.")
        sys.exit(0)
    else:
        print("\n💥 Algunos tests fallaron. Revisa los logs para más detalles.")
        sys.exit(1)
