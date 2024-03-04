<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use LdapRecord\Container;
use LdapRecord\Models\OpenLDAP\User;
use Tests\TestCase;

class LdapLoginTest extends TestCase
{
    /**
     * Test LDAP user connection
     * username: usertest
     * password: 123
     */
    public function test_login(): void
    {
        $connection = Container::getDefaultConnection();
        $user = User::findByOrFail('uid', 'usertest');
        $dn = $user->getDn();
        $testResonse = $connection->auth()->attempt($dn, '123');
        $this->assertTrue($testResonse);
    }
}
