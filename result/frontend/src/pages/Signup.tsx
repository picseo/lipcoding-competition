import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('mentor');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    try {
      const res = await fetch('/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, name: email.split('@')[0], role }),
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || '회원가입 실패');
        return;
      }
      navigate('/login');
    } catch (err) {
      setError('네트워크 오류');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <form className="bg-white p-8 rounded shadow-md w-full max-w-md" onSubmit={handleSubmit}>
        <h2 className="text-2xl font-bold mb-6 text-center">회원가입</h2>
        <div className="mb-4">
          <label htmlFor="email" className="block mb-1">이메일</label>
          <input id="email" type="email" className="w-full border rounded px-3 py-2" required value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block mb-1">비밀번호</label>
          <input id="password" type="password" className="w-full border rounded px-3 py-2" required value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        <div className="mb-4">
          <label htmlFor="role" className="block mb-1">역할</label>
          <select id="role" className="w-full border rounded px-3 py-2" required value={role} onChange={e => setRole(e.target.value)}>
            <option value="mentor">멘토</option>
            <option value="mentee">멘티</option>
          </select>
        </div>
        {error && <div className="text-red-500 mb-2 text-center">{error}</div>}
        <button id="signup" type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">회원가입</button>
      </form>
    </div>
  );
};

export default Signup;
