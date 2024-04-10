<?php

namespace App\Miniserver;

use function Safe\json_encode;
use function Safe\json_decode;

class Shadow
{
    const CHANGE_PASSWORD = "CHANGE_PASSWORD";
    const ROLLBACK = "ROLLBACK";

    protected TcpBuilder $tcp;

    public function __construct()
    {
        $this->tcp = new TcpBuilder();
        $this->tcp->connect();
    }

    public function chpasswd(
        string $username,
        string $oldPassword,
        string $newPassword
    ): array {
        $message = [
            "action" => self::CHANGE_PASSWORD,
            "data" => [
                "username" => $username,
                "old_password" => $oldPassword,
                "new_password" => $newPassword
            ]
        ];
        $message = json_encode($message);
        $data = $this->tcp->send($message)->receive();
        return json_decode($data, true);
    }
    public function rollback(): array
    {
        $message = ["action" => self::ROLLBACK];
        $message = json_encode($message);
        $data = $this->tcp->send($message)->receive();
        return json_decode($data, true);
    }

    public function close()
    {
        return $this->tcp->close();
    }
}
