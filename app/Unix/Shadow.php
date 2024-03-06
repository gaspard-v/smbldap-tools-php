<?php

namespace App\Unix;

use function Safe\fwrite;
use function Safe\fopen;

abstract class Shadow
{
    static public function chpasswd(
        string $username,
        string $oldPassword,
        string $newPassword
    ) {
        $pipePath = $_ENV["PIPE_PATH"];
        $pipe = fopen($pipePath, 'w');
        fwrite($pipe, "test");
    }
}
