<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Welcome</title>
    </head>
    <body>
        <h1>Welcome</h1>
        @if (Route::has('login'))
            @auth
                @if (Route::has('dashboard'))
                    <a href="{{ route('dashboard', absolute: false) }}">dashboard</a>
                @endif
            @else
                <a href="{{ route('login', absolute: false) }}">login</a>
            @endauth
        @endif
    </body>
</html>
