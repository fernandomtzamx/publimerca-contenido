<?php
/**
 * Plugin Name: Publimerca: auth para API REST
 * Description: Permite que el agente de Publimerca publique por la API REST con contraseña de aplicación en servidores que borran el encabezado Authorization (LiteSpeed, FastCGI) o con plugins que consultan el usuario antes de tiempo. No abre acceso nuevo: sin contraseña de aplicación válida todo sigue rechazado.
 * Version: 1.1
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// 1. Credencial alterna: X-Publimerca-Auth lleva el mismo "Basic base64(usuario:contraseña)".
if ( empty( $_SERVER['PHP_AUTH_USER'] ) ) {
	$publimerca_header = '';
	if ( ! empty( $_SERVER['HTTP_X_PUBLIMERCA_AUTH'] ) ) {
		$publimerca_header = $_SERVER['HTTP_X_PUBLIMERCA_AUTH'];
	} elseif ( ! empty( $_SERVER['HTTP_AUTHORIZATION'] ) ) {
		$publimerca_header = $_SERVER['HTTP_AUTHORIZATION'];
	} elseif ( ! empty( $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ) ) {
		$publimerca_header = $_SERVER['REDIRECT_HTTP_AUTHORIZATION'];
	}
	$publimerca_header = trim( (string) $publimerca_header );
	if ( 0 === stripos( $publimerca_header, 'basic ' ) ) {
		$publimerca_decoded = base64_decode( substr( $publimerca_header, 6 ), true );
		if ( false !== $publimerca_decoded && false !== strpos( $publimerca_decoded, ':' ) ) {
			list( $publimerca_user, $publimerca_pass ) = explode( ':', $publimerca_decoded, 2 );
			$_SERVER['PHP_AUTH_USER'] = $publimerca_user;
			$_SERVER['PHP_AUTH_PW']   = $publimerca_pass;
		}
	}
}

// 2. Reconocer peticiones a la API REST desde el inicio, aunque otro plugin
//    consulte el usuario actual antes de que WordPress defina REST_REQUEST.
add_filter(
	'application_password_is_api_request',
	function ( $is_api_request ) {
		if ( $is_api_request ) {
			return true;
		}
		$uri = isset( $_SERVER['REQUEST_URI'] ) ? (string) $_SERVER['REQUEST_URI'] : '';
		return false !== strpos( $uri, '/wp-json/' ) || isset( $_GET['rest_route'] );
	}
);

// 3. Si alguien ya fijó el usuario como "anónimo" antes de tiempo, recalcularlo
//    al iniciar la API REST, cuando la contraseña de aplicación sí se evalúa.
add_action(
	'rest_api_init',
	function () {
		if ( ! empty( $_SERVER['PHP_AUTH_USER'] ) && 0 === get_current_user_id() ) {
			$GLOBALS['current_user'] = null;
			wp_get_current_user();
		}
	},
	0
);
