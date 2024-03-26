<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Http\RedirectResponse;

class PasswdController extends Controller
{
    public function authenticate(Request $request): RedirectResponse
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

        if ($credentials['new_password'] !== $credentials['validate_new_password']) {
            return back()->withErrors([
                'password' => 'Password mismatch',
            ])->onlyInput('username');
        }
        return redirect()->intended('dashboard');
    }
}
