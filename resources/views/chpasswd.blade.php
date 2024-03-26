@extends('layout')
@section('title', 'Dashboard')
@section('content')
<form method="POST">
    <div>
        @csrf
    </div>
    <div>
        <label for="current_password">Current password:</label>
        <input type="password" id="current_password" name="current_password" required>
    </div>
    <div>
        <label for="new_password">New password:</label>
        <input type="password" id="new_password" name="new_password" required>
    </div>
    <div>
        <label for="validate_new_password">Validate new password:</label>
        <input type="password" id="validate_new_password" name="validate_new_password" required>
    </div>
    <div>
        <button type="submit">Change Password</button>
    </div>
</form>
@endsection
