import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
  vus: 2,
  duration: '20s',
  thresholds: {
  'http_req_duration': ['p(95)<3000'],  
  'http_req_failed': ['rate<0.5'],      
  'checks': ['rate>0.80'],             
  },
};

const BASE = 'https://restcountries.com/v3.1';

function hasCountryShape(c) {
  if (!c || typeof c !== 'object') return false;
  const nameOk = !!(c.name && typeof c.name.common === 'string');
  const cca2Ok = (typeof c.cca2 === 'string') || (typeof c.cca3 === 'string');
  const popOk = (typeof c.population === 'number') || (typeof c.population === 'undefined');
  const capitalOk = Array.isArray(c.capital) || typeof c.capital === 'string' || c.capital === undefined;
  return nameOk && cca2Ok && popOk && capitalOk;
}

export default function () {
  group('GET /all', () => {
    const res = http.get(`${BASE}/all`);
    check(res, {
      'all: status 200': (r) => r.status === 200,
      'all: parseable json': (r) => {
        try { JSON.parse(r.body); return true; } catch (e) { return false; }
      },
      'all: non-empty array': (r) => {
        try { const a = JSON.parse(r.body); return Array.isArray(a) && a.length > 0; } catch { return false; }
      },
      'all: p95 quick': (r) => r.timings.duration < 1000,
    });

    try {
      const arr = JSON.parse(res.body);
      if (arr.length) {
        check(arr[0], { 'all:first has expected shape': (c) => hasCountryShape(c) });
      }
    } catch (e) { }

    sleep(1);
  });

  group('GET /name/{name}', () => {
    const tests = [
      { url: `${BASE}/name/turkey`, expect: 'Turkey', desc: 'happy: turkey' },
      { url: `${BASE}/name/tuRkEy`, expect: 'Turkey', desc: 'case-insensitive' },
      { url: `${BASE}/name/finland?fullText=true`, expect: 'Finland', desc: 'fullText exact' },
      { url: `${BASE}/name/somecompletelymadeupcountryname`, expect: null, desc: 'not found' },
    ];

    for (const t of tests) {
      const r = http.get(t.url);
      if (t.expect) {
        check(r, {
          [`${t.desc}: status 200`]: (res) => res.status === 200,
          [`${t.desc}: parseable`]: (res) => { try { JSON.parse(res.body); return true; } catch { return false; } },
          [`${t.desc}: contains country`]: (res) => {
            try {
              const arr = JSON.parse(res.body);
              return arr.some(x => x.name && x.name.common === t.expect);
            } catch { return false; }
          },
          [`${t.desc}: schema ok`]: (res) => {
            try {
              const arr = JSON.parse(res.body);
              const c = arr.find(x => x.name && x.name.common === t.expect) || arr[0];
              return hasCountryShape(c);
            } catch { return false; }
          },
        });
      } else {
        check(r, {
          [`${t.desc}: handled (not 500)`]: (res) => res.status < 500,
        });
      }
      sleep(0.5);
    }
  });

  group('GET /capital/{capital}', () => {
    const r = http.get(`${BASE}/capital/ankara`);
    check(r, {
      'capital/ankara: status 200': (res) => res.status === 200,
      'capital/ankara: contains Turkey': (res) => {
        try { const arr = JSON.parse(res.body); return arr.some(x => x.name && x.name.common === 'Turkey'); } catch { return false; }
      },
    });

    const rb = http.get(`${BASE}/capital/asdasdasdasd`);
    check(rb, { 'capital/bogus: handled': (res) => res.status < 500 });
    sleep(0.5);
  });

  group('GET /lang/{code}', () => {
    const r = http.get(`${BASE}/lang/tr`);
    check(r, {
      'lang/tr: status 200': (res) => res.status === 200,
      'lang/tr: non-empty array': (res) => {
        try { const arr = JSON.parse(res.body); return Array.isArray(arr) && arr.length > 0; } catch { return false; }
      },
    });
    sleep(0.5);
  });

  group('GET /alpha/{code}', () => {
    const r = http.get(`${BASE}/alpha/TR`);
    check(r, {
      'alpha/TR: status 200': (res) => res.status === 200,
      'alpha/TR: contains Turkey': (res) => {
        try { const obj = JSON.parse(res.body); return (obj.name && obj.name.common === 'Turkey') || (Array.isArray(obj) && obj.some(x => x.name && x.name.common === 'Turkey')); } catch { return false; }
      },
    });

    const rn = http.get(`${BASE}/alpha/XXX`);
    check(rn, { 'alpha/XXX: handled': (res) => res.status !== 200 });
    sleep(0.5);
  });

  group('GET /region & /currency', () => {
    const r1 = http.get(`${BASE}/region/europe`);
    check(r1, { 'region/europe: status 200': (res) => res.status === 200 });

    const r2 = http.get(`${BASE}/currency/TRY`);
    check(r2, { 'currency/TRY: status 200/404': (res) => res.status === 200 || res.status === 404 });
    sleep(0.5);
  });

  sleep(1);
}
