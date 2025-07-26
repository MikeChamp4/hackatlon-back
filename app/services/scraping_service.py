import requests
import traceback
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


class ScrapingService:
    
    def __init__(self):
        self.session = requests.Session()
        # Headers para simular un navegador real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def scrape_tarragona_padron_info(self, url):
        """
        Hace scraping de la página del padrón de Tarragona y extrae la información del documento.
        """
        try:
            print(f"🌐 Haciendo scraping de: {url}")
            
            # Realizar la petición
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parsear el HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer información del documento
            document_info = self._extract_document_info(soup)
            
            return {
                'success': True,
                'url': url,
                'document_info': document_info,
                'status_code': response.status_code
            }
            
        except requests.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            traceback.print_exc()
            return {
                'success': False,
                'error': f"Error de conexión: {str(e)}",
                'url': url
            }
            
        except Exception as e:
            print(f"❌ Error general: {e}")
            traceback.print_exc()
            return {
                'success': False,
                'error': f"Error general: {str(e)}",
                'url': url
            }
    
    def _extract_document_info(self, soup):
        """
        Extrae la información específica del documento de la página.
        """
        document_info = {
            'title': '',
            'description': '',
            'requirements': [],
            'procedures': [],
            'additional_info': [],
            'raw_text': ''
        }
        
        try:
            # Extraer título del documento
            title_selectors = [
                'h1', 'h2.titulo', '.titulo-tramite', '.page-title',
                '[class*="titulo"]', '[class*="title"]'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem and title_elem.get_text(strip=True):
                    document_info['title'] = title_elem.get_text(strip=True)
                    break
            
            # Extraer descripción general
            description_selectors = [
                '.descripcion', '.description', '.resumen', '.summary',
                '[class*="descripcion"]', '[class*="description"]',
                'p.intro', '.contenido-principal p'
            ]
            
            for selector in description_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem and desc_elem.get_text(strip=True):
                    document_info['description'] = desc_elem.get_text(strip=True)
                    break
            
            # Extraer requisitos
            requirements_text = self._extract_section_text(soup, [
                'requisitos', 'requirements', 'documentos', 'documents',
                'necesario', 'requerido'
            ])
            document_info['requirements'] = requirements_text
            
            # Extraer procedimientos
            procedures_text = self._extract_section_text(soup, [
                'procedimiento', 'procedure', 'tramite', 'proceso',
                'pasos', 'steps', 'como'
            ])
            document_info['procedures'] = procedures_text
            
            # Extraer información adicional
            additional_selectors = [
                '.info-adicional', '.additional-info', '.notas', '.notes',
                '.importante', '.important', '.observaciones'
            ]
            
            for selector in additional_selectors:
                for elem in soup.select(selector):
                    text = elem.get_text(strip=True)
                    if text and len(text) > 10:
                        document_info['additional_info'].append(text)
            
            # Extraer todo el texto visible de la página
            # Eliminar scripts, estilos, etc.
            for script in soup(["script", "style", "meta", "link"]):
                script.decompose()
            
            # Obtener todo el texto
            all_text = soup.get_text()
            # Limpiar el texto
            lines = (line.strip() for line in all_text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)
            
            document_info['raw_text'] = clean_text
            
            print(f"✅ Información extraída exitosamente")
            return document_info
            
        except Exception as e:
            print(f"❌ Error extrayendo información: {e}")
            traceback.print_exc()
            return document_info
    
    def _extract_section_text(self, soup, keywords):
        """
        Extrae texto de secciones basándose en palabras clave.
        """
        texts = []
        
        for keyword in keywords:
            # Buscar por texto que contenga la palabra clave
            elements = soup.find_all(text=re.compile(keyword, re.IGNORECASE))
            
            for element in elements:
                parent = element.parent
                if parent:
                    # Obtener el contenido del elemento padre
                    text = parent.get_text(strip=True)
                    if text and len(text) > 20 and text not in texts:
                        texts.append(text)
                    
                    # También revisar hermanos siguientes
                    for sibling in parent.find_next_siblings():
                        sibling_text = sibling.get_text(strip=True)
                        if sibling_text and len(sibling_text) > 20:
                            texts.append(sibling_text)
                        if len(texts) >= 5:  # Limitar cantidad
                            break
        
        return texts[:10]  # Retornar máximo 10 elementos
