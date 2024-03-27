<?php

namespace App\Miniserver;

use function Safe\json_encode;
use function Safe\json_decode;

abstract class Shadow
{
    static public function chpasswd(
        string $username,
        string $oldPassword,
        string $newPassword
    ): array {
        $tcp = new TcpBuilder();
        $message = [
            "username" => $username,
            "old_password" => $oldPassword,
            "new_password" => $newPassword
        ];
        $message = json_encode($message);
        $data = $tcp->connect()->send($message)->receive();
        return json_decode($data, true);
    }
}
