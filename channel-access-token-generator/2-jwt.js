const fs = require('fs')
const jose = require('node-jose');
require('dotenv').config();

const rawData = fs.readFileSync('./private.key');
const privateKey = JSON.parse(rawData);
const header = {
	alg: privateKey.alg,
	typ: 'JWT',
	kid: process.env.KID,
};
const payload = {
	iss: process.env.CHANNEL_ID,
	sub: process.env.CHANNEL_ID,
	aud: "https://api.line.me/",
	exp: Math.floor(new Date().getTime() / 1000) +  30 * 60,
	token_exp: 1 * 24 * 3600,
};
jose.JWS.createSign({ format: 'compact', fields: header }, privateKey)
	.update(JSON.stringify(payload))
	.final()
	.then(console.log)
