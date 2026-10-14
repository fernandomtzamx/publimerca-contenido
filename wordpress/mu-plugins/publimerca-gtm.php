<?php
/**
 * Plugin Name: Publimerca: Google Tag Manager
 * Description: Carga el contenedor de Google Tag Manager en todo el sitio público. GA4 y demás etiquetas se configuran dentro de GTM, no aquí.
 * Version: 1.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const PUBLIMERCA_GTM_ID = 'GTM-5PTRT2J';

/**
 * Solo en el sitio público: nada en el admin, la API, feeds ni vistas previas del personalizador.
 */
function publimerca_gtm_activo() {
	if ( is_admin() || is_feed() || is_customize_preview() ) {
		return false;
	}
	if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
		return false;
	}
	return true;
}

// Script principal, lo más arriba posible del <head>.
add_action(
	'wp_head',
	function () {
		if ( ! publimerca_gtm_activo() ) {
			return;
		}
		$id = esc_js( PUBLIMERCA_GTM_ID );
		echo "<!-- Google Tag Manager -->\n";
		echo "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n";
		echo "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n";
		echo "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n";
		echo "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n";
		echo "})(window,document,'script','dataLayer','{$id}');</script>\n";
		echo "<!-- End Google Tag Manager -->\n";
	},
	1
);

// Respaldo noscript, justo después de abrir <body>.
add_action(
	'wp_body_open',
	function () {
		if ( ! publimerca_gtm_activo() ) {
			return;
		}
		$id = esc_attr( PUBLIMERCA_GTM_ID );
		echo "<!-- Google Tag Manager (noscript) -->\n";
		echo "<noscript><iframe src=\"https://www.googletagmanager.com/ns.html?id={$id}\" height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript>\n";
		echo "<!-- End Google Tag Manager (noscript) -->\n";
	},
	1
);
