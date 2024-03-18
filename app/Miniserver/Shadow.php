<?php

namespace App\Miniserver;

use function Safe\json_encode;

abstract class Shadow
{
    static public function chpasswd(
        string $username,
        string $oldPassword,
        string $newPassword
    ) {
        $tcp = new TcpBuilder();
        $message = [
            "username" => $username,
            "old_password" => $oldPassword,
            "new_password" => $newPassword
        ];
        $message = json_encode($message);
        $ret = $tcp->connect()->send($message)->receive();
        echo $ret;
    }
}
