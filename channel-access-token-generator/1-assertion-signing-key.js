const crypto = require('crypto');
const { writeFileSync } = require('fs');

(async () => {
	const pair = await crypto.subtle.generateKey(
		{
			name: 'RSASSA-PKCS1-v1_5',
			modulusLength: 2048,
			publicExponent: new Uint8Array([1, 0, 1]),
			hash: 'SHA-256'
		},
		true,
		['sign', 'verify']
	);
	 
	writeFileSync('private.key', JSON.stringify(await crypto.subtle.exportKey('jwk', pair.privateKey)))
	writeFileSync('public.key', JSON.stringify(await crypto.subtle.exportKey('jwk', pair.publicKey)))
})();
