@extends('layout')
@section('title', 'Login')
@section('content')
    <form method="POST">
        <div>
            @csrf
        </div>
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <div>
            <button type="submit">Login</button>
        </div>
    </form>
    @if ($errors->has('username'))
        <span>
            <strong>{{ $errors->first('username') }}</strong>
        </span>
    @endif
@endsection
