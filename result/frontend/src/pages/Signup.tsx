import React from 'react';

const Signup = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <form className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">회원가입</h2>
        <div className="mb-4">
          <label htmlFor="email" className="block mb-1">이메일</label>
          <input id="email" type="email" className="w-full border rounded px-3 py-2" required />
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block mb-1">비밀번호</label>
          <input id="password" type="password" className="w-full border rounded px-3 py-2" required />
        </div>
        <div className="mb-4">
          <label htmlFor="role" className="block mb-1">역할</label>
          <select id="role" className="w-full border rounded px-3 py-2" required>
            <option value="mentor">멘토</option>
            <option value="mentee">멘티</option>
          </select>
        </div>
        <button id="signup" type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">회원가입</button>
      </form>
    </div>
  );
};

export default Signup;
