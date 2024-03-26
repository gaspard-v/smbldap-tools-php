<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Miniserver\Shadow;
use Illuminate\View\View;
use Illuminate\Support\MessageBag;
use Illuminate\Support\Facades\Redirect;
use Illuminate\Http\RedirectResponse;
use function Safe\fopen;

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

        // TODO correct this
        $this->changeShadow($uid, $current_password, $new_password);
        return view('passwd');
    }

    protected function passwdUserExists(string $username): bool
    {
        $passwd_file = '/etc/passwd';
        $handle = @fopen($passwd_file, 'r');
        try {
            while (($line = fgets($handle)) !== false) {
                $fields = explode(':', $line);
                if ($fields[0] === $username) {
                    return true;
                }
            }
            return false;
        } finally {
            fclose($handle);
        }
    }

    protected function changeShadow(string $username, string $currentPassword, string $newPassword)
    {
        if (!$this->passwdUserExists($username))
            return;
        $response = Shadow::chpasswd($username, $currentPassword, $newPassword);
    }
}
