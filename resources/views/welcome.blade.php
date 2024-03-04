@extends('layout')
@section('title', 'Welcome')

@section('content')
    @if (Route::has('login'))
    @auth
        @if (Route::has('dashboard'))
            <a href="{{ route('dashboard', absolute: false) }}">dashboard</a>
        @endif
    @else
        <a href="{{ route('login', absolute: false) }}">login</a>
    @endauth
    @endif
@endsection