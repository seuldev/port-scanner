import socket
import threading

# Diccionario con puertos comunes y sus servicios
puertos_servicios = {
    20: "FTP (data)",
    21: "FTP (control)",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    115: "SFTP",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    161: "SNMP",
    194: "IRC",
    443: "HTTPS",
    445: "Microsoft-DS",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Proxy",
}

puertos_abiertos = []  # Lista global para guardar puertos abiertos
lock = threading.Lock()  # Para sincronizar acceso a la lista

def escanear_puerto(ip, port, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            servicio = puertos_servicios.get(port, "Servicio desconocido")
            print(f"Puerto {port} está ABIERTO - {servicio}")
            with lock:
                puertos_abiertos.append((port, servicio))
    except:
        pass
    finally:
        s.close()

def main():
    while True:
        ip = input("Introduce la IP objetivo: ")
        try:
            socket.inet_aton(ip)
            break
        except socket.error:
            print("IP inválida, intenta otra vez.")

    while True:
        try:
            inicio = int(input("Puerto inicial (1-65535): "))
            fin = int(input("Puerto final (1-65535): "))
            if 1 <= inicio <= 65535 and 1 <= fin <= 65535 and inicio <= fin:
                break
            else:
                print("Rango de puertos inválido, intenta otra vez.")
        except ValueError:
            print("Por favor ingresa números enteros válidos.")

    while True:
        try:
            timeout = float(input("Tiempo de espera por puerto en segundos (ej. 0.5): "))
            if timeout > 0:
                break
            else:
                print("Debe ser un número positivo.")
        except ValueError:
            print("Por favor ingresa un número válido.")

    while True:
        try:
            max_hilos = int(input("Cantidad máxima de hilos concurrentes (ej. 100): "))
            if max_hilos > 0:
                break
            else:
                print("Debe ser un número positivo.")
        except ValueError:
            print("Por favor ingresa un número válido.")

    print(f"\nEscaneando puertos del {inicio} al {fin} en {ip} con timeout {timeout}s y hasta {max_hilos} hilos...\n")

    threads = []
    for port in range(inicio, fin + 1):
        while threading.active_count() > max_hilos:
            pass  # Espera a que haya espacio para crear nuevo hilo

        t = threading.Thread(target=escanear_puerto, args=(ip, port, timeout))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    if puertos_abiertos:
        puertos_abiertos.sort(key=lambda x: x[0])  # Ordenar por puerto
        with open("puertos_abiertos.txt", "w") as f:
            for port, servicio in puertos_abiertos:
                f.write(f"Puerto {port} está ABIERTO - {servicio}\n")
        print(f"\nEscaneo terminado. Resultados guardados en puertos_abiertos.txt")
    else:
        print("\nNo se encontraron puertos abiertos en ese rango.")

if __name__ == "__main__":
    main()
