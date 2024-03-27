@extends('layout')
@section('title', 'Dashboard')
@section('content')
    <h1>Welcome {{ $username }}</h1>
    @if (Route::has('chpasswd'))
    <a href="{{ route('chpasswd', absolute: false) }}">Change Password</a>
    @endif
    @if (session('shadow'))
    <p>Shadow password modified successfully</p>
    <div>
        {{ session('shadow') }}
    </div>
    @endif
    @if (session('ldap'))
    <p>ldap password modified successfully</p>
    @endif
@endsection
