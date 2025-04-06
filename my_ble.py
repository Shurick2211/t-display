import ubluetooth
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_MTU_EXCHANGED = const(21)
_IRQ_L2CAP_ACCEPT = const(22)
_IRQ_L2CAP_CONNECT = const(23)
_IRQ_L2CAP_DISCONNECT = const(24)
_IRQ_L2CAP_RECV = const(25)
_IRQ_L2CAP_SEND_READY = const(26)
_IRQ_CONNECTION_UPDATE = const(27)
_IRQ_ENCRYPTION_UPDATE = const(28)
_IRQ_GET_SECRET = const(29)
_IRQ_SET_SECRET = const(30)
_GATTS_NO_ERROR = const(0x00)
_GATTS_ERROR_READ_NOT_PERMITTED = const(0x02)
_GATTS_ERROR_WRITE_NOT_PERMITTED = const(0x03)
_GATTS_ERROR_INSUFFICIENT_AUTHENTICATION = const(0x05)
_GATTS_ERROR_INSUFFICIENT_AUTHORIZATION = const(0x08)
_GATTS_ERROR_INSUFFICIENT_ENCRYPTION = const(0x0f)
_PASSKEY_ACTION_NONE = const(0)
_PASSKEY_ACTION_INPUT = const(2)
_PASSKEY_ACTION_DISPLAY = const(3)
_PASSKEY_ACTION_NUMERIC_COMPARISON = const(4)

class BLEUART:
    def __init__(self, name="ESP32-UART"):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq)
        self._connections = set()
        self._register_services()
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            # A central has connected to this peripheral.
            conn_handle, addr_type, addr = data
            print("📶 Connected")
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            # A central has disconnected from this peripheral.
            conn_handle, addr_type, addr = data
            print("🔌 Disconnected")
            self._connections.remove(conn_handle)
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            # A client has written to this characteristic or descriptor.
            conn_handle, attr_handle = data
            msg = self.ble.gatts_read(self.rx).decode('utf-8').strip()
            print(f"📨 Received: {msg}")
            self.send("✅ Got your message!")
        elif event == _IRQ_GATTS_READ_REQUEST:
            # A client has issued a read. Note: this is only supported on STM32.
            # Return a non-zero integer to deny the read (see below), or zero (or None)
            # to accept the read.
            conn_handle, attr_handle = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_SCAN_RESULT:
            # A single scan result.
            addr_type, addr, adv_type, rssi, adv_data = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_SCAN_DONE:
            # Scan duration finished or manually stopped.
            pass
        elif event == _IRQ_PERIPHERAL_CONNECT:
            # A successful gap_connect().
            conn_handle, addr_type, addr = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            # Connected peripheral has disconnected.
            conn_handle, addr_type, addr = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTC_SERVICE_RESULT:
            # Called for each service found by gattc_discover_services().
            conn_handle, start_handle, end_handle, uuid = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTC_SERVICE_DONE:
            # Called once service discovery is complete.
            # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            # Called for each characteristic found by gattc_discover_services().
            conn_handle, end_handle, value_handle, properties, uuid = data
        elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
            # Called once service discovery is complete.
            # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTC_DESCRIPTOR_RESULT:
            # Called for each descriptor found by gattc_discover_descriptors().
            conn_handle, dsc_handle, uuid = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTC_DESCRIPTOR_DONE:
            # Called once service discovery is complete.
            # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTC_READ_RESULT:
            # A gattc_read() has completed.
            conn_handle, value_handle, char_data = data
        elif event == _IRQ_GATTC_READ_DONE:
            # A gattc_read() has completed.
            # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, value_handle, status = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTC_WRITE_DONE:
            # A gattc_write() has completed.
            # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, value_handle, status = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTC_NOTIFY:
            # A server has sent a notify request.
            conn_handle, value_handle, notify_data = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTC_INDICATE:
            # A server has sent an indicate request.
            conn_handle, value_handle, notify_data = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GATTS_INDICATE_DONE:
            # A client has acknowledged the indication.
            # Note: Status will be zero on successful acknowledgment, implementation-specific value otherwise.
            conn_handle, value_handle, status = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_MTU_EXCHANGED:
            # ATT MTU exchange complete (either initiated by us or the remote device).
            conn_handle, mtu = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_L2CAP_ACCEPT:
            # A new channel has been accepted.
            # Return a non-zero integer to reject the connection, or zero (or None) to accept.
            conn_handle, cid, psm, our_mtu, peer_mtu = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_L2CAP_CONNECT:
            # A new channel is now connected (either as a result of connecting or accepting).
            conn_handle, cid, psm, our_mtu, peer_mtu = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_L2CAP_DISCONNECT:
            # Existing channel has disconnected (status is zero), or a connection attempt failed (non-zero status).
            conn_handle, cid, psm, status = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_L2CAP_RECV:
            # New data is available on the channel. Use l2cap_recvinto to read.
            conn_handle, cid = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_L2CAP_SEND_READY:
            # A previous l2cap_send that returned False has now completed and the channel is ready to send again.
            # If status is non-zero, then the transmit buffer overflowed and the application should re-send the data.
            conn_handle, cid, status = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_CONNECTION_UPDATE:
            # The remote device has updated connection parameters.
            conn_handle, conn_interval, conn_latency, supervision_timeout, status = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_ENCRYPTION_UPDATE:
            # The encryption state has changed (likely as a result of pairing or bonding).
            conn_handle, encrypted, authenticated, bonded, key_size = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_GET_SECRET:
            # Return a stored secret.
            # If key is None, return the index'th value of this sec_type.
            # Otherwise return the corresponding value for this sec_type and key.
            sec_type, index, key = data
            print(f"Event {event} Data {data} ")
        elif event == _IRQ_SET_SECRET:
            # Save a secret to the store for this sec_type and key.
            sec_type, key, value = data
            print(f"Event {event} Data {data} ")


    def _register_services(self):
        UART_UUID = ubluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
        UART_TX = (ubluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'),
                   ubluetooth.FLAG_READ | ubluetooth.FLAG_NOTIFY,)
        UART_RX = (ubluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'),
                   ubluetooth.FLAG_WRITE,)
        UART_SERVICE = (UART_UUID, (UART_TX, UART_RX,),)
        SERVICES = (UART_SERVICE,)
        ((self.tx, self.rx,),) = self.ble.gatts_register_services(SERVICES)

    def _advertise(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = b'\x02\x01\x06' + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        print("📡 Advertising...")

    def send(self, data):
        for conn_handle in self._connections:
            self.ble.gatts_notify(conn_handle, self.tx, data + "\n")
