<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Welcome</title>

</head>

<body>
    @if (Route::has('login'))
    <a href="{{ route('login', absolute: false) }}">Login</a>
    @else
    <p>Website is in maintenance mode</p>
    @endif
</body>

</html>