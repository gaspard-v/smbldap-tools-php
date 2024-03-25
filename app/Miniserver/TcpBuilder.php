<?php

namespace App\Miniserver;

use Exception;

use function Safe\socket_create;
use function Safe\socket_connect;
use function Safe\socket_read;
use function Safe\socket_write;
use Safe\Exceptions\SocketsException;

class TcpBuilder
{
    /** @var \Socket|resource $client_socket */
    protected $client_socket;

    protected string $address;

    protected int $port;

    protected int $bufferSize;

    protected int $headerSize;

    public function __construct(
        string $address = "127.0.0.1",
        int $port = 48751,
        int $bufferSize = 8192,
        int $headerSize = 4
    ) {
        $this->address = $address;
        $this->port = $port;
        $this->bufferSize = $bufferSize;
        $this->headerSize = $headerSize;
        $this->client_socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    }

    public function __destruct()
    {
        $this->close();
    }

    public function connect()
    {
        socket_connect(
            $this->client_socket,
            $this->address,
            $this->port
        );
        return $this;
    }

    /**
     * Lit la taille des données à recevoir depuis le socket
     * @param resource $socket Le socket client
     * @return int La taille des données à recevoir
     * @throws Exception En cas d'erreur lors de la lecture de l'en-tête
     */
    protected function getDataSize()
    {

        $header = socket_read(
            $this->client_socket,
            $this->headerSize
        );

        if ($header === "") {
            throw new SocketsException("Unexpected empty header");
        }
        return current(unpack('N', $header));
    }

    /**
     * Envoie un message via le socket
     * @param string $message Le message à envoyer
     * @return self
     */
    public function send(string $message)
    {
        $header  = pack('N', strlen($message));
        socket_write($this->client_socket, $header);
        socket_write($this->client_socket, $message);
        return $this;
    }

    /**
     * Reçoit des données depuis le socket
     * @return string Les données reçues
     * @throws Exception En cas d'erreur lors de la réception des données
     */
    public function receive()
    {
        $data = '';
        $remainingSize = $this->getDataSize();
        while ($remainingSize > 0) {
            $chunk = socket_read(
                $this->client_socket,
                min($this->bufferSize, $remainingSize)
            );

            if ($chunk === "") {
                throw new SocketsException("Unexpected empty chunk");
            }
            $data .= $chunk;
            $remainingSize -= strlen($chunk);
        }
        return $data;
    }

    public function close()
    {
        socket_close($this->client_socket);
    }
}
