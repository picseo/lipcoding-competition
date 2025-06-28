import { useState } from "react";
import { login } from "../api/api";

export default function LoginPage() {
  const [form, setForm] = useState({ email: "", password: "" });
  const handleChange = e => setForm({ ...form, [e.target.id]: e.target.value });
  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const { token } = await login(form);
      localStorage.setItem("token", token);
      window.location.href = "/profile";
    } catch (err) {
      alert(err.error || "로그인 실패");
    }
  };
  return (
    <form onSubmit={handleSubmit}>
      <input id="email" value={form.email} onChange={handleChange} placeholder="이메일" />
      <input id="password" type="password" value={form.password} onChange={handleChange} placeholder="비밀번호" />
      <button id="login" type="submit">로그인</button>
    </form>
  );
}
