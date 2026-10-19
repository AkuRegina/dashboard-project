"use strict";
const el = (id) => document.getElementById(id);
let token = null;
let expiresAt = null;

function message(text, error = false) {
  el("message").textContent = text;
  el("message").classList.toggle("error", error);
  el("message").hidden = !text;
}

function tab(mode) {
  for (const name of ["login", "register"]) {
    const active = name === mode;
    el(`${name}-tab`).classList.toggle("active", active);
    el(`${name}-tab`).setAttribute("aria-selected", String(active));
    el(`${name}-tab`).tabIndex = active ? 0 : -1;
    el(`${name}-panel`).hidden = !active;
  }
}

function signedOut() {
  token = null;
  expiresAt = null;
  el("guest-panel").hidden = false;
  el("user-panel").hidden = true;
  el("password-form").reset();
  tab("login");
}

function showUser(user) {
  el("guest-panel").hidden = true;
  el("user-panel").hidden = false;
  el("welcome").textContent = `Hello, ${user.f_name}.`;
  el("user-email").textContent = user.email;
  el("user-role").textContent = user.role;
  el("session-expiry").textContent = new Date(expiresAt).toLocaleString();
}

async function api(path, body, method = "POST") {
  const headers = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(path, {method, headers, body: body === undefined ? undefined : JSON.stringify(body)});
  const data = response.status === 204 ? {} : await response.json();
  if (!response.ok) {
    if (response.status === 401 && token) signedOut();
    throw new Error(data.error || "Request failed. Please try again.");
  }
  return data;
}

async function busy(button, action) {
  button.disabled = true;
  message("");
  try { await action(); }
  catch (error) { message(error.message || "Could not connect to the server.", true); }
  finally { button.disabled = false; }
}

for (const mode of ["login", "register"]) {
  el(`${mode}-tab`).addEventListener("click", () => {tab(mode); message("");});
  el(`${mode}-tab`).addEventListener("keydown", (event) => {
    if (["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) {
      event.preventDefault();
      const next = event.key === "Home" ? "login" : event.key === "End" ? "register" : mode === "login" ? "register" : "login";
      tab(next); el(`${next}-tab`).focus();
    }
  });
}

el("register-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const body = Object.fromEntries(new FormData(event.target));
  if (body.password !== body.confirm_password) {message("Passwords do not match.", true); return;}
  delete body.confirm_password;
  busy(event.submitter, async () => {
    await api("/demo/register", body);
    event.target.reset();
    el("login-email").value = body.email;
    tab("login");
    el("login-password").focus();
    message("Account created. Log in with your email and password.");
  });
});

el("login-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    const data = await api("/auth/login", Object.fromEntries(new FormData(event.target)));
    token = data.token;
    expiresAt = data.expires_at;
    event.target.reset();
    showUser(data.user);
    message("You’re logged in.");
  });
});

el("logout").addEventListener("click", (event) => busy(event.currentTarget, async () => {
  await api("/auth/logout");
  signedOut();
  message("You’re logged out.");
}));

el("check-session").addEventListener("click", (event) => busy(event.currentTarget, async () => {
  const data = await api("/auth/me", undefined, "GET");
  showUser(data.user);
  message("Session checked. You’re still logged in.");
}));

el("password-form").addEventListener("submit", (event) => {
  event.preventDefault();
  busy(event.submitter, async () => {
    const data = await api("/auth/change-password", Object.fromEntries(new FormData(event.target)));
    signedOut();
    message(data.message);
  });
});
