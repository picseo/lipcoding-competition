import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  // TODO: 인증 및 역할에 따라 메뉴 변경
  return (
    <nav className="bg-blue-600 text-white px-4 py-3 flex gap-4">
      <Link to="/profile">프로필</Link>
      <Link to="/mentors">멘토목록</Link>
      <Link to="/requests">매칭요청</Link>
      <Link to="/login">로그아웃</Link>
    </nav>
  );
};

export default Navbar;
