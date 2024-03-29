<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LoginController;
use App\Http\Controllers\PasswdController;


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
    return view('welcome');
})->name("index");

Route::get('/login', function () {
    return view('login');
});

Route::get('/logout', [LoginController::class, 'logout'])->name('logout')->middleware(['auth']);

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

Route::post(
    '/chpasswd',
    [PasswdController::class, 'change_password']
)->name('chpasswd')->middleware(['auth', 'share.authenticated.user']);
