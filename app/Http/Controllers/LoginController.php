<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Http\RedirectResponse;

class LoginController extends Controller
{
    public function authenticate(Request $request): RedirectResponse
    {
        $messages = [
            'username.required' => 'Username is required!',
            'password.required' => 'Password is required!'
        ];
        $credentials = $request->validate([
            'username' => ['required'],
            'password' => ['required'],
        ], $messages);
        $credentials = [
            'sn' => $credentials['username'],
            'password' => $credentials['password'],
        ];
        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();

            return redirect()->intended('dashboard');
        }
        return back()->withErrors([
            'username' => 'The provided credentials do not match our records.',
        ])->onlyInput('username');
    }
}
