<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>@yield('title', 'Welcome')</title>
    </head>
    <body>
        <header>
            <h1>@yield('title', 'Welcome')</h1>
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