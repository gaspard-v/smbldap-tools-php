<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LoginController;
use Illuminate\Support\Facades\Auth;

use App\Miniserver\Shadow;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    Shadow::chpasswd("", "", "");
    return view('welcome');
});

Route::get('/login', function () {
    return view('login');
});

Route::post(
    '/login',
    [LoginController::class, 'authenticate']
)->name('login');

Route::get('/dashboard', function () {
    $user = Auth::user();
    [$username] = $user->uid;
    return view(
        'dashboard',
        ['username' => $username]
    );
})->name('dashboard')->middleware('auth');
