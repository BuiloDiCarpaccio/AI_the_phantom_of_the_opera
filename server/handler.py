import json
import socket
import struct
from .types import QuestionType


HOST = 'localhost'
PORT = 12000

class ServerHandler:

    def __init__(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __enter__(self):
        self._socket.connect((HOST, PORT))

        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self._socket.close()

    def _receive_json(self) -> bytes:
        length_buff = self._recvall(4)

        if length_buff is None:
            return None
        length, = struct.unpack('!I', length_buff)
        return self._recvall(length)

    def _recvall(self, count: int) -> bytes:
        buff = b''

        while count:
            new_buff = self._socket.recv(count)

            if not new_buff:
                return None
            buff += new_buff
            count -= len(new_buff)
        return buff

    def _send_json(self, data: bytes) -> None:
        length = len(data)

        self._socket.sendall(struct.pack('!I', length))
        self._socket.sendall(data)

    def receive(self) -> QuestionType:
        data = self._receive_json()

        if data is None:
            return None
        return json.loads(data)

    def send(self, response: int) -> None:
        data = json.dumps(response).encode('utf-8')

        self._send_json(data)
