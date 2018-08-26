import client from './http';

function apiGet(url, params) {
  return client.get(url, params);
}

function apiPost(url, params) {
  return client.post(url, params);
}

function apiDelete(url, params) {
  return client.delete(url, params);
}

export {
  apiGet,
  apiPost,
  apiDelete,
};
