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
    Shadow::chpasswd("loled", "123", "123");
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
    return view('dashboard');
})->name('dashboard')->middleware(['auth', 'share.authenticated.user']);

Route::get('/chpasswd', function () {
    return view('chpasswd');
})->name('chpasswd')->middleware(['auth', 'share.authenticated.user']);
