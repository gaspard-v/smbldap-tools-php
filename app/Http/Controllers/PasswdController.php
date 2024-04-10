<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Miniserver\Shadow;
use Illuminate\View\View;
use Illuminate\Support\MessageBag;
use Illuminate\Support\Facades\Redirect;
use Illuminate\Http\RedirectResponse;
use App\Crypt\SmbHash;
use function Safe\fopen;
use function Safe\json_encode;

class PasswdController extends Controller
{
    public function change_password(Request $request): View|RedirectResponse
    {
        $messages = [
            'current_password.required' => 'Current password is required!',
            'new_password.required' => 'New password is required!',
            'validate_new_password.required' => 'Password validation is required'
        ];
        $credentials = $request->validate([
            'current_password' => ['required', 'max:50'],
            'new_password' => ['required', 'max:25', 'min:10'],
            'validate_new_password' => ['required', 'max:25', 'min:10'],
        ], $messages);

        $errors = new MessageBag();
        if ($credentials['new_password'] !== $credentials['validate_new_password']) {
            $errors->add('password', 'Password mismatch');
            return Redirect::back()->withErrors($errors);
        }
        $current_password = $credentials['current_password'];
        $new_password = $credentials['new_password'];
        $user = $request->user();
        [$uid] = $user->uid;
        $shadow_return = $this->changeShadow($uid, $current_password, $new_password);
        $return_value = [];
        if ($shadow_return)
            $return_value = array_merge($return_value, ['shadow' => json_encode($shadow_return)]);
        if (!isset($shadow_return["rollback"]))
            $this->changeLdap($user, $new_password);

        $return_value = array_merge($return_value, ['ldap' => "Password modified"]);
        return redirect('/dashboard')->with($return_value);
    }

    protected function passwdUserExists(string $username): bool
    {
        $passwd_file = '/etc/passwd';
        $handle = fopen($passwd_file, 'r');
        try {
            while (($line = fgets($handle)) !== false) {
                $fields = explode(':', $line);
                if ($fields[0] === $username) {
                    return true;
                }
            }
            return false;
        } finally {
            @fclose($handle);
        }
    }

    static public function getDaysSinceEpoch(): int
    {
        $today = time();
        $epochTime = strtotime('1970-01-01');
        $daysSinceEpoch = ($today - $epochTime) / (24 * 60 * 60);

        return (int)$daysSinceEpoch;
    }

    protected function changeShadow(string $username, string $currentPassword, string $newPassword)
    {
        if (!$this->passwdUserExists($username))
            return;
        $miniserver = new Shadow();
        $return_value =  $miniserver->chpasswd($username, $currentPassword, $newPassword);
        if (200 != $return_value['status_code']) {
            $return_value["rollback"] = $miniserver->rollback();
        }
        $miniserver->close();
        return $return_value;
    }

    protected function changeLdap(mixed $user, string $newPassword)
    {
        $nthash = SmbHash::nthash($newPassword);
        $user->password = $newPassword;
        $user->sambaNTPassword = $nthash;
        $user->shadowLastChange = self::getDaysSinceEpoch();
        return $user->save();
    }
}
