<?php
/**
 * Plugin Name: Publimerca: auth para API REST
 * Description: Algunos servidores (LiteSpeed, FastCGI) borran el encabezado Authorization.
 *              Este plugin acepta la misma credencial Basic en X-Publimerca-Auth y la entrega
 *              a WordPress, que la valida como contraseña de aplicación. No abre ningún acceso nuevo:
 *              sin una contraseña de aplicación válida, la petición sigue rechazada.
 * Version: 1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( empty( $_SERVER['PHP_AUTH_USER'] ) && ! empty( $_SERVER['HTTP_X_PUBLIMERCA_AUTH'] ) ) {
	$header = trim( wp_unslash( $_SERVER['HTTP_X_PUBLIMERCA_AUTH'] ) );
	if ( 0 === stripos( $header, 'basic ' ) ) {
		$decoded = base64_decode( substr( $header, 6 ), true );
		if ( false !== $decoded && false !== strpos( $decoded, ':' ) ) {
			list( $user, $pass )      = explode( ':', $decoded, 2 );
			$_SERVER['PHP_AUTH_USER'] = $user;
			$_SERVER['PHP_AUTH_PW']   = $pass;
		}
	}
}
