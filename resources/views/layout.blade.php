<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>@yield('title', 'Welcome')</title>
    </head>
    <body>
        <header>
            <h2><a href={{ url('/') }}>Index</a></h2>
            <h1>@yield('title', 'Welcome')</h1>
            @if (Route::has('logout'))
            @auth
            <a href="{{ route('logout', absolute: false) }}">Logout</a>
            @endif
        </header>
        <main>
            @yield('content')
        </main>
        @hasSection('footer')
            <footer>
                @yield('footer')
            </footer>
        @endif
    </body>
</html>
