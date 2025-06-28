import React from 'react';

const Login = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <form className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">로그인</h2>
        <div className="mb-4">
          <label htmlFor="email" className="block mb-1">이메일</label>
          <input id="email" type="email" className="w-full border rounded px-3 py-2" required />
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block mb-1">비밀번호</label>
          <input id="password" type="password" className="w-full border rounded px-3 py-2" required />
        </div>
        <button id="login" type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">로그인</button>
      </form>
    </div>
  );
};

export default Login;
