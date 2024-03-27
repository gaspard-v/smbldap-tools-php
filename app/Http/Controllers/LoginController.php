<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\MessageBag;

class LoginController extends Controller
{
    public function authenticate(Request $request): RedirectResponse
    {
        $messages = [
            'username.required' => 'Username is required!',
            'password.required' => 'Password is required!'
        ];
        $credentials = $request->validate([
            'username' => ['required', 'max:50'],
            'password' => ['required', 'max:50'],
        ], $messages);
        $credentials = [
            'uid' => $credentials['username'],
            'password' => $credentials['password'],
        ];
        if (!Auth::attempt($credentials)) {
            $errors = new MessageBag();
            $errors->add('credentials', 'The provided credentials do not match our records.');
            return back()->withErrors($errors);
        }
        $request->session()->regenerate();
        return redirect()->intended('dashboard');
    }
}
