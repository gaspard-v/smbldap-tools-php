<?php

namespace App\Unix;

abstract class Shadow
{


    static public function chpasswd(
        string $username,
        string $oldPassword,
        string $newPassword
    ) {
        if (isset($argc) && isset($argv)) {
            exec("sudo php " . __FILE__ . " chpasswd");
            return;
        }
        var_dump(get_current_user());
    }
}

if (!isset($argc) || !isset($argv))
    return;
if ($argc < 2)
    return;
if ($argv[1] !== "chpasswd")
    return;
Shadow::chpasswd("", "", "");
