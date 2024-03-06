<?php

require_once realpath(__DIR__ . '/vendor/autoload.php');

use function Safe\fclose;
use function Safe\stream_socket_server;

class Miniserver
{

    private string $socketAddress;
    private $socket;
    private bool $stop = false;

    public function __construct()
    {
        echo "Starting miniserver... ";
        $dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
        $dotenv->load();
        $address = $_ENV['SOCKET_ADDRESS'];
        $this->socketAddress = "tcp://{$address}";
        $this->socket = $this->createSocket();
        pcntl_signal(SIGTERM, [$this, "sigHandler"]);
        pcntl_signal(SIGINT, [$this, "sigHandler"]);
        echo "done!\n";
        echo "Listening on {$this->socketAddress}\n";
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
            STREAM_SERVER_BIND | STREAM_SERVER_LISTEN,
            $context
        );
        return $socket;
    }

    public function __destruct()
    {
        echo "Closing miniserver... ";
        fclose($this->socket);
        echo "bye!\n";
    }

    private function sigHandler(int $signum)
    {
        $intNum = [SIGTERM, SIGINT];

        if (in_array($signum, $intNum)) {
            echo "Miniserver got signal {$signum}, server is closing soon.\n";
            $this->stop = true;
        }
    }

    public function execute()
    {
        echo "Starting main event loop\n";
        while (!$this->stop) {
            pcntl_signal_dispatch();
            $so = @stream_socket_accept($this->socket, 3, $peer_name);
            if (!$so)
                continue;
            $content = stream_get_contents($so);
            echo $content;
            fclose($so);
        }
    }
}

function main(): int
{
    $server = new Miniserver();
    $server->execute();
    return 0;
}

if (get_included_files()[0] === __FILE__ && php_sapi_name() === 'cli') {
    exit(main());
}
