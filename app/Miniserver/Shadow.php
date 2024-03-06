<?php

namespace App\Miniserver;

use Exception;

use function Safe\stream_socket_client;
use function Safe\fclose;

abstract class Shadow
{
    static public function chpasswd(
        string $username,
        string $oldPassword,
        string $newPassword
    ) {
        $address = $_ENV['SOCKET_ADDRESS'];
        $address = "tcp://{$address}";
        $context = stream_context_create();
        $socket = stream_socket_client($address, $error_code, $error_message, 10, STREAM_CLIENT_CONNECT, $context);
        stream_socket_sendto($socket, "test");
        try {
            fclose($socket);
        } catch (Exception $err) {
            //TODO
        }
    }
}
