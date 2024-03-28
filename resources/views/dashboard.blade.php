@extends('layout')
@section('title', 'Dashboard')
@section('content')
    <h1>Welcome {{ $username }}</h1>
    @if (Route::has('chpasswd'))
    <a href="{{ route('chpasswd', absolute: false) }}">Change Password</a>
    @endif
    @if (session('shadow'))
    <p>
        {{ session('shadow') }}
    </p>
    @endif
    @if (session('ldap'))
    <p>{{ session('ldap') }}</p>
    @endif
@endsection
