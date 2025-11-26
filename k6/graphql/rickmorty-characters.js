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

const URL = 'https://rickandmortyapi.com/graphql';

export default function () {
  group('GraphQL: characters list', () => {
    const query = JSON.stringify({ query: '{ characters(page:1) { results { id name status species } } }' });
    const r = http.post(URL, query, { headers: { 'Content-Type': 'application/json' } });
    check(r, {
      'chars: status 200': (res) => res.status === 200,
      'chars: parseable': (res) => { try { JSON.parse(res.body); return true; } catch { return false; } },
      'chars: has results array': (res) => {
        try { const data = JSON.parse(res.body); return !!(data.data && data.data.characters && Array.isArray(data.data.characters.results)); } catch { return false; }
      },
    });
    sleep(0.5);
  });

  // functional: get a specific character by name (rick)
  group('GraphQL: character by name', () => {
    const q = JSON.stringify({ query: '{ characters(filter:{name:"Rick"}) { results { id name } } }' });
    const r = http.post(URL, q, { headers: { 'Content-Type': 'application/json' } });
    check(r, {
      'name: status 200': (res) => res.status === 200,
      'name: contains Rick': (res) => {
        try { const data = JSON.parse(res.body); return data.data.characters.results.some(c => c.name.includes('Rick')); } catch { return false; }
      },
    });
    sleep(0.5);
  });

  group('GraphQL: malformed query', () => {
    const bad = JSON.stringify({ query: '{ unknownField }' });
    const r = http.post(URL, bad, { headers: { 'Content-Type': 'application/json' } });
    check(r, {
      'malformed: handled (not 200 w/o errors)': (res) => res.status === 400 || (res.status === 200 && JSON.parse(res.body).errors),
    });
    sleep(0.5);
  });

  sleep(1);
}
