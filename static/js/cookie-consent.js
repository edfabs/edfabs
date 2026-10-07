/*
 * Consentimiento de cookies de edfabs.com
 * Markup y estilos: skeleton/templates/partials/cookie_consent.html
 *
 * Los scripts no esenciales se escriben como
 *   <script type="text/plain" data-ck-category="analytics" ...>
 * y solo se activan si la categoría fue aceptada.
 * API pública: window.edfCookies.open()
 */
(function () {
	'use strict';

	const COOKIE_NAME = 'edf_cookie_consent';
	const VERSION = 1; // Subirlo obliga a pedir consentimiento de nuevo
	const MAX_AGE = 60 * 60 * 24 * 365; // 12 meses
	const CATEGORIES = ['analytics'];
	const VENDOR_COOKIES = {
		analytics: [/^_ga$/, /^_ga_/, /^_gid$/, /^_gat/],
	};

	let banner, modal, dialog, switches;
	let lastFocus = null;

	// ── Cookie de consentimiento ──────────────────────────────────────────

	function readConsent() {
		const match = document.cookie.match(new RegExp('(?:^|; )' + COOKIE_NAME + '=([^;]*)'));
		if (!match) return null;
		try {
			const data = JSON.parse(decodeURIComponent(match[1]));
			return data && data.v === VERSION ? data : null;
		} catch (e) {
			return null;
		}
	}

	function writeConsent(choices) {
		const data = { v: VERSION, necessary: true };
		CATEGORIES.forEach((cat) => { data[cat] = !!choices[cat]; });
		data.ts = new Date().toISOString();

		// Secure solo en https para que funcione también en localhost
		const secure = location.protocol === 'https:' ? '; Secure' : '';
		document.cookie = COOKIE_NAME + '=' + encodeURIComponent(JSON.stringify(data)) +
			'; path=/; max-age=' + MAX_AGE + '; SameSite=Lax' + secure;
		return data;
	}

	// Borra las cookies de un proveedor en el host y en todos sus dominios padre (.edfabs.com)
	function deleteVendorCookies(category) {
		const patterns = VENDOR_COOKIES[category] || [];
		const parts = location.hostname.split('.');
		const domains = [''];
		for (let i = 0; i < parts.length - 1; i++) {
			domains.push('; domain=.' + parts.slice(i).join('.'));
		}
		document.cookie.split('; ').forEach((pair) => {
			const name = pair.split('=')[0];
			if (!patterns.some((re) => re.test(name))) return;
			domains.forEach((domain) => {
				document.cookie = name + '=; path=/; max-age=0' + domain;
			});
		});
	}

	// ── Activación de scripts bloqueados ──────────────────────────────────

	function activateCategory(category) {
		const selector = 'script[type="text/plain"][data-ck-category="' + category + '"]:not([data-ck-done])';
		document.querySelectorAll(selector).forEach((blocked) => {
			const script = document.createElement('script');
			Array.from(blocked.attributes).forEach((attr) => {
				if (attr.name === 'type' || attr.name === 'data-ck-category') return;
				script.setAttribute(attr.name, attr.value);
			});
			if (!blocked.src) script.textContent = blocked.textContent;
			blocked.setAttribute('data-ck-done', '');
			blocked.after(script);
		});
	}

	function applyConsent(consent, previous) {
		const revoked = previous && CATEGORIES.some((cat) => previous[cat] && !consent[cat]);
		if (revoked) {
			CATEGORIES.forEach((cat) => {
				if (previous[cat] && !consent[cat]) deleteVendorCookies(cat);
			});
			// Los scripts ya ejecutados no se pueden descargar: recargar la página
			location.reload();
			return;
		}
		CATEGORIES.forEach((cat) => {
			if (consent[cat]) activateCategory(cat);
		});
	}

	function save(choices) {
		const previous = readConsent();
		const consent = writeConsent(choices);
		hideBanner();
		closeModal();
		applyConsent(consent, previous);
	}

	function allChoices(value) {
		const choices = {};
		CATEGORIES.forEach((cat) => { choices[cat] = value; });
		return choices;
	}

	// ── Banner ────────────────────────────────────────────────────────────

	function showBanner() { banner.hidden = false; }
	function hideBanner() { banner.hidden = true; }

	// ── Panel ─────────────────────────────────────────────────────────────

	function setSwitch(btn, on) {
		btn.setAttribute('aria-checked', on ? 'true' : 'false');
		btn.querySelector('.ck-switch__state').textContent = on ? 'On' : 'Off';
	}

	function focusables() {
		return Array.from(dialog.querySelectorAll('button:not([disabled]), a[href]'));
	}

	function openModal() {
		const consent = readConsent() || {};
		switches.forEach((btn) => setSwitch(btn, !!consent[btn.dataset.ckSwitch]));

		lastFocus = document.activeElement;
		modal.hidden = false;
		document.body.style.overflow = 'hidden';
		dialog.focus();
		document.addEventListener('keydown', onModalKeydown);
	}

	function closeModal() {
		if (modal.hidden) return;
		modal.hidden = true;
		document.body.style.overflow = '';
		document.removeEventListener('keydown', onModalKeydown);

		// Si el elemento que abrió el panel ya no está visible (banner oculto), no se puede regresar el foco ahí
		if (lastFocus && document.contains(lastFocus) && lastFocus.offsetParent !== null) {
			lastFocus.focus();
		}
		lastFocus = null;
	}

	function onModalKeydown(event) {
		if (event.key === 'Escape') {
			event.preventDefault();
			closeModal();
			return;
		}
		if (event.key !== 'Tab') return;

		const items = focusables();
		const first = items[0];
		const last = items[items.length - 1];
		const active = document.activeElement;
		if (event.shiftKey && (active === first || active === dialog)) {
			event.preventDefault();
			last.focus();
		} else if (!event.shiftKey && active === last) {
			event.preventDefault();
			first.focus();
		}
	}

	// ── Init ──────────────────────────────────────────────────────────────

	function onAction(event) {
		const target = event.target.closest('[data-ck-action], [data-ck-switch]');
		if (!target) return;

		if (target.dataset.ckSwitch) {
			setSwitch(target, target.getAttribute('aria-checked') !== 'true');
			return;
		}
		switch (target.dataset.ckAction) {
			case 'accept-all': save(allChoices(true)); break;
			case 'reject': save(allChoices(false)); break;
			case 'customize': openModal(); break;
			case 'close': closeModal(); break;
			case 'save': {
				const choices = {};
				switches.forEach((btn) => { choices[btn.dataset.ckSwitch] = btn.getAttribute('aria-checked') === 'true'; });
				save(choices);
				break;
			}
		}
	}

	function init() {
		const root = document.getElementById('ck-root');
		if (!root) return;
		banner = document.getElementById('ck-banner');
		modal = document.getElementById('ck-modal');
		dialog = modal.querySelector('[role="dialog"]');
		switches = Array.from(modal.querySelectorAll('[data-ck-switch]'));

		root.addEventListener('click', onAction);
		// Clic en el fondo oscuro cierra el panel
		modal.addEventListener('click', (event) => {
			if (event.target === modal) closeModal();
		});
		// Enlaces externos al componente (footer)
		document.querySelectorAll('[data-ck-open]').forEach((el) => {
			el.addEventListener('click', (event) => {
				event.preventDefault();
				window.edfCookies.open();
			});
		});

		const consent = readConsent();
		if (consent) {
			applyConsent(consent, null);
		} else {
			showBanner();
		}
	}

	window.edfCookies = {
		open: openModal,
	};

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', init);
	} else {
		init();
	}
})();
