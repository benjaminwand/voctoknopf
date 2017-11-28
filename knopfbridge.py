import errno, serial, socket

MIXER_HOST = '10.73.80.3'
MIXER_PORT = 9999

KNOPF_DEVICE = '/dev/tty.usbmodem1411'
KNOPF_BAUD = 9600

INTERVAL = 0.2

mixer_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mixer_conn.connect((MIXER_HOST, MIXER_PORT))

knopf_conn = serial.Serial(port = KNOPF_DEVICE, baudrate = KNOPF_BAUD,
                           timeout = INTERVAL)

print ('ok')

knopf_buffer = ''
mixer_buffer = ''

while True:
    knopf_buffer += knopf_conn.readline()
    reqs = knopf_buffer.split(b'\r\n')
    knopf_buffer = reqs.pop()

    for req in reqs:
        if req.startswith(b'< '):
            print('>>>', req[2:])
            mixer_conn.sendall(req[2:] + b'\n')
        else:
            print('DEBUG:', req)

    try:
        mixer_buffer += mixer_conn.recv(4096, socket.MSG_DONTWAIT)
    except socket.error as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            raise
    else:
        resps = mixer_buffer.split(b'\n')
        mixer_buffer = resps.pop()
        for resp in resps:
            print('<<<', resp)

mixer_conn.close()
knopf_conn.close()
