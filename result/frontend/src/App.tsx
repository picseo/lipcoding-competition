import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Signup from './pages/Signup';
import Login from './pages/Login';
import Profile from './pages/Profile';
import Mentors from './pages/Mentors';
import Requests from './pages/Requests';
import Navbar from './components/Navbar';

function App() {
  // TODO: 인증 상태 및 역할에 따라 라우팅/네비게이션 제어
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <Routes>
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/mentors" element={<Mentors />} />
        <Route path="/requests" element={<Requests />} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </div>
  );
}

export default App;
