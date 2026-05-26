import ftplib
import logging

# Configuramos logging para ver los comandos enviados y recibidos (El Canal de Control en acción)
logging.basicConfig(level=logging.DEBUG)

def conectar_ftp_y_descargar(host, usuario, password, archivo, usar_pasivo=True):
    try:
        print(f"=== Iniciando conexión FTP a {host} ===")
        
        # 1. Establecer Canal de Control (Puerto 21 por defecto)
        ftp = ftplib.FTP(host)
        ftp.login(user=usuario, passwd=password)
        
        # 2. Configurar el Modo FTP (Activo o Pasivo)
        if usar_pasivo:
            print("Configurando: MODO PASIVO (Cliente inicia canal de datos)")
            ftp.set_pasv(True)  # Envía el comando PASV
        else:
            print("Configurando: MODO ACTIVO (Servidor inicia canal de datos)")
            ftp.set_pasv(False) # Envía el comando PORT
            
        # 3. Iniciar la transferencia (Abre el Canal de Datos)
        print(f"Iniciando descarga de: {archivo}")
        with open(f"descargado_{archivo}", 'wb') as file_local:
            # Comando RETR es para descargar. Aquí se negocian los puertos según el modo elegido.
            ftp.retrbinary(f'RETR {archivo}', file_local.write)
            
        print("Transferencia completada exitosamente.")
        
    except Exception as e:
        print(f"Error en la transferencia: {e}")
        print("NOTA: Si falló en Modo Activo, probablemente tu Firewall/NAT bloqueó la conexión entrante del puerto 20 del servidor.")
        
    finally:
        # Cerrar Canal de Control
        ftp.quit()

# --- Ejecución de Ejemplo ---
if __name__ == "__main__":
    HOST = "test.rebex.net"
    USER = "demo"
    PASS = "password"
    ARCHIVO = "readme.txt"
    
    # Prueba 1: Modo Pasivo (Usualmente exitoso detrás de NAT)
    conectar_ftp_y_descargar(HOST, USER, PASS, ARCHIVO, usar_pasivo=True)
    
    print("\n" + "="*50 + "\n")
    
    # Prueba 2: Modo Activo (Usualmente falla (timeout) si estás detrás de un router doméstico)
    conectar_ftp_y_descargar(HOST, USER, PASS, ARCHIVO, usar_pasivo=False)
