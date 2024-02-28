<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use LdapRecord\Container;
use LdapRecord\Models\OpenLDAP\User;

class LoginController extends Controller
{
    /**
     * Handle an authentication attempt.
     */
    public function authenticate(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'username' => ['required', 'username'],
            'password' => ['required'],
        ]);
        $connection = Container::getConnection('default');
        $user = User::findByOrFail('sn', $credentials['username']);

        if ($connection->auth()->attempt($user->getDn(), $credentials['password'])) {
            $request->session()->regenerate();

            return redirect()->intended('dashboard');
        }

        return back()->withErrors([
            'email' => 'The provided credentials do not match our records.',
        ])->onlyInput('email');
    }
}
