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
        $tcp = new TcpBuilder();
        $ret = $tcp->connect()->send("test")->receive();
        echo $ret;
    }
}
