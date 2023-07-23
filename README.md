# Proxy_Checker
This project is a Python proxy checker that supports HTTP, HTTPS, SOCKS4, and SOCKS5.  It uses asynchronous operations to check and filter working proxies in an efficient and easy-to-use way.



# Instalación y Uso del Verificador de Proxies

Este proyecto consta de un verificador de proxies asincrónico en Python que permite verificar proxies para diferentes protocolos como HTTP, HTTPS, SOCKS4 y SOCKS5. El código fuente principal es ```main.py```

# Requisitos

Python 3.7+ : Para instalar Python, visite la página oficial de descarga de Python y siga las instrucciones.

aiohttp: Un cliente HTTP/HTTPs asíncrono. Puede instalarlo utilizando el gestor de paquetes pip:


```pip install aiohttp```

# Uso

Clonar el repositorio:


```git clone https://github.com/LvL23HT/proxy_checker.git ```
``` cd proxy-checker ```

Ejecute el programa:


```python main.py ```

Después de ejecutar el programa, se le presentará un menú para seleccionar el tipo de protocolo que desea verificar.

<img src="https://github.com/LvL23HT/Proxy_Checker/blob/main/screenshot.png" width="500">

Los proxys que desea verificar deben estar en el archivo proxies.txt

Pudes limitar el número de tareas segun las necesidades de tu PC y tu conexión a internet, por defecto 5000

```sem = asyncio.Semaphore(5000)```

También puedes aumentar el tiempo de respuesta para determinar si el proxy esta vivo, por defecto 5s. igualmente el servidor para la verificación, por defecto Google.

```async with sem, session.get('https://www.google.com', proxy=f'{protocol_type}://{proxy}', timeout=5) as response:```

# Pasos para la instalación y uso en diferentes sistemas operativos

## Windows:

Para instalar Python en Windows, descargue el instalador desde el sitio web oficial de Python y siga las instrucciones. El instalador incluirá pip, por lo que también podrá instalar aiohttp utilizando el comando ```pip install aiohttp``` en el símbolo del sistema.

## Linux:

Dependiendo de su distribución de Linux, es posible que ya tenga Python instalado. Puede verificar esto ejecutando ``` python3 --version``` . Si no está instalado, puede usar el gestor de paquetes de su distribución para instalar Python.

Después de instalar Python, puede instalar aiohttp con 
```pip3 install aiohttp```

## Termux (Android):

En Termux, primero deberá instalar Python con pkg install python. Luego, puede instalar aiohttp con ```pip install aiohttp```

Recuerde, en todos los sistemas operativos, debe clonar el repositorio y navegar hasta el directorio del proyecto antes de ejecutar el script con 
```python main.py```

Espero que este post sea útil para entender cómo usar este verificador de proxy. Si tienes alguna pregunta o problema, no dudes en abrir un nuevo issue.


# Aviso Legal

Este software se proporciona "tal cual", sin garantía de ningún tipo, expresa o implícita, incluyendo, pero no limitándose a, las garantías de comerciabilidad, idoneidad para un propósito particular y no infracción. En ningún caso, los autores o los titulares de los derechos de autor serán responsables de ninguna reclamación, daño u otra responsabilidad, ya sea en una acción de contrato, agravio o de otro tipo, derivada de, fuera de, o en conexión con el software o el uso u otros tratos en el software.

Además, este verificador de proxies se proporciona con fines educativos y de investigación. No promovemos, alentamos o apoyamos ninguna actividad ilegal asociada con el uso de proxies. El uso de proxies debe cumplir con las leyes locales y las políticas de los sitios web que está visitando. Por favor, asegúrese de que entiende y respeta las regulaciones y políticas relevantes antes de usar este software.


# Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.


Por favor, asegúrese de incluir una copia de la licencia en cualquier distribución que haga de este software o de cualquier software que incluya código de este proyecto.

# Website

https://level23hacktools.com
