<?php

require_once realpath(__DIR__ . '/vendor/autoload.php');

use function Safe\stream_socket_recvfrom;
use function Safe\fclose;
use function Safe\stream_socket_server;

class Miniserver
{

    private string $socketAddress;
    private $socket;
    private bool $stop = false;

    public function __construct()
    {
        echo "Starting miniserver...\n";
        $dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
        $dotenv->load();
        $address = $_ENV['SOCKET_ADDRESS'];
        $this->socketAddress = "udp://{$address}";
        $this->socket = $this->createSocket();
        pcntl_signal(SIGTERM, [$this, "sigHandler"]);
        pcntl_signal(SIGINT, [$this, "sigHandler"]);
    }

    private function createSocket()
    {
        $context = stream_context_create([
            'socket' => [
                'backlog' => 1,
                'so_reuseport' => true,
            ],
        ]);
        $socket = stream_socket_server(
            $this->socketAddress,
            $errno,
            $errstr,
            STREAM_SERVER_BIND,
            $context
        );
        return $socket;
    }

    public function __destruct()
    {
        echo "Closing miniserver...\n";
        fclose($this->socket);
    }

    private function sigHandler(int $signum)
    {
        $intNum = [SIGTERM, SIGINT];

        if (in_array($signum, $intNum)) {
            echo "Signal got, server is closing soon...\n";
            $this->stop = true;
        }
    }

    public function execute()
    {
        while (!$this->stop) {
            $read   = [$this->socket];
            $write  = NULL;
            $except = NULL;

            pcntl_signal_dispatch();
            $numChangedStreams = @stream_select($read, $write, $except, 3);
            if (!$numChangedStreams)
                continue;
            $content = "";
            while ($data = stream_socket_recvfrom($this->socket, 8192, 0, $peer)) {
                $content .= $data;
            }
            echo $content;
        }
    }
}

$server = new Miniserver();
$server->execute();
