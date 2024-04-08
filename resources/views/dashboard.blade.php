@extends('layout')
@section('title', 'Dashboard')
@section('content')
    <h1>Welcome {{ $username }}</h1>
    @if (Route::has('chpasswd'))
    <a href="{{ route('chpasswd', absolute: false) }}">Change Password</a>
    @endif
    @foreach (['shadow', 'ldap'] as $key)
        @if (session($key))
            <p>{{ session($key) }}</p>
        @endif
    @endforeach
@endsection
