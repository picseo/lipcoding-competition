import { useState } from "react";
import { signup } from "../api/api";

export default function SignupPage() {
  const [form, setForm] = useState({ email: "", password: "", name: "", role: "mentor" });
  const handleChange = e => setForm({ ...form, [e.target.id]: e.target.value });
  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await signup(form);
      alert("회원가입 성공! 로그인 해주세요.");
      window.location.href = "/";
    } catch (err) {
      alert(err.error || "회원가입 실패");
    }
  };
  return (
    <form onSubmit={handleSubmit}>
      <input id="email" value={form.email} onChange={handleChange} placeholder="이메일" />
      <input id="password" type="password" value={form.password} onChange={handleChange} placeholder="비밀번호" />
      <input id="name" value={form.name} onChange={handleChange} placeholder="이름" />
      <select id="role" value={form.role} onChange={handleChange}>
        <option value="mentor">멘토</option>
        <option value="mentee">멘티</option>
      </select>
      <button id="signup" type="submit">회원가입</button>
    </form>
  );
}
