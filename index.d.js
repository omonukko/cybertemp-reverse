(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([[1931], {1281: function (e, t, r) {
  Promise.resolve().then(r.bind(r, 1832));
}, 1832: function (e, t, r) {
  "use strict";
  r.r(t), r.d(t, {default: function () {
    return e_;
  }});
  var a = r(3860), s = r(259), n = r(8270), i = r(4461), l = r(6245), o = r(2746), c = r(6060), d = r(3600), u = r(3379), m = r(4385), f = r(5552), h = r(5639), x = r(8), p = r(9673), g = r(1433), b = r(8206), w = r(7654), y = r(4595), v = r(5202);
  let j = false, N = null;
  async function _() {
    j || (N || (N = (0, v.ZP)("/w.wasm").then(() => {
      j = true;
    })), await N);
  }
  async function E() {
    let e, t;
    await _();
    let r = {difficulty: Math.floor(2 * Math.random()) + 5, salt_length: Math.floor(4 * Math.random()) + 8, iterations: Math.floor(2 * Math.random()) + 1};
    try {
      e = (0, v.Z9)(r.difficulty, r.salt_length, r.iterations, "cybertemp");
    } catch (e) {
      throw e;
    }
    try {
      t = JSON.parse(e);
    } catch (e) {
      throw e;
    }
    return t.config || (t.config = r), t;
  }
  async function C(e) {
    {
      let t = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAh6p66pVDFDfd+MRPa22g\njYhI//6XZKUbb/rRAzYgcyyzb73hBEqRMmCtDKNvIUe+qXI1xX1JHsSnT+Hi5wsu\nfuW44RlFTlRuhM4entshgr+S8lAlLH914Sz5N2hLB9hgZmAMecQIhCOTjYG1t4NU\nA8ggbVLKalBz83gsTup+U+6S+OGji5Cq2vbKVIHYKTZHqoQKNzCH6A6z0E+AoygB\nyk1H98YHFoebpYoqVk0NCORBB+/ZLIa+guB83cS6sAL+SFYWxBcW9DwwzaJnFOIp\npNq0WgL3ggAt97CuGBMbuET0sEtxCfYPFnD/BL9QnQJONbuUUPBvfpLSkFJZhyy3\nkQIDAQAB\n-----END PUBLIC KEY-----";
      if (!t) throw Error("NEXT_PUBLIC_COOKIE_ENCRYPTION_KEY is not set");
      let r = atob(t.replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace(/\s+/g, "")), a = new Uint8Array(r.length);
      for (let e = 0; e < r.length; e++) a[e] = r.charCodeAt(e);
      let s = await window.crypto.subtle.importKey("spki", a.buffer, {name: "RSA-OAEP", hash: "SHA-256"}, false, ["encrypt"]);
      return btoa(String.fromCharCode(...new Uint8Array(await window.crypto.subtle.encrypt({name: "RSA-OAEP"}, s, (new TextEncoder).encode(e)))));
    }
  }
  let S = null, A = 0, k = null;
  async function I() {
    let e = arguments.length > 0 && undefined !== arguments[0] && arguments[0], t = Date.now() - A;
    if (!e && A > 0 && t < 15e5) return;
    let a = await E(), s = await C(JSON.stringify({...a, createdAt: Date.now()})), n = Math.random().toString(36).slice(2) + Date.now();
    return new Promise((e, t) => {
      let i = (S || (S = new Worker(r.tu(new URL(r.p + r.u(7732), r.b)), {type: undefined})), S);
      i._latestPowRequestId = n;
      let l = setTimeout(() => {
        i.removeEventListener("message", o), t(Error("PoW challenge timeout - generating new challenge"));
      }, 6e4), o = async r => {
        let {solution: a, error: c, requestId: d} = r.data;
        if (i._latestPowRequestId === n) {
          if (clearTimeout(l), i.removeEventListener("message", o), a) try {
            let t = await C(JSON.stringify(a));
            document.cookie = "__bp=".concat(s, "|").concat(t, "; path=/; secure; sameSite=strict"), A = Date.now(), k && clearTimeout(k), k = setTimeout(() => {
              I(true).catch(console.error);
            }, 15e5), e();
          } catch (e) {
            t(e);
          } else c && t(Error(c));
        }
      };
      i.addEventListener("message", o), i.postMessage({challengeStr: JSON.stringify(a), maxIterations: 1e6, requestId: n});
    });
  }
