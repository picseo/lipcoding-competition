import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  const isLoggedIn = Boolean(localStorage.getItem('token'));

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="bg-blue-600 text-white px-4 py-3 flex gap-4">
      {isLoggedIn ? (
        <>
          <Link to="/profile">프로필</Link>
          <Link to="/mentors">멘토목록</Link>
          <Link to="/requests">매칭요청</Link>
          <button onClick={handleLogout} className="bg-blue-700 px-2 rounded">로그아웃</button>
        </>
      ) : (
        <>
          <Link to="/login">로그인</Link>
          <Link to="/signup">회원가입</Link>
        </>
      )}
    </nav>
  );
};

export default Navbar;
