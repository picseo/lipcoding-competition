import { useEffect, useState } from "react";
import { getMe } from "../api/api";

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return (window.location.href = "/login");
    getMe(token).then(setProfile).catch(() => window.location.href = "/login");
  }, []);
  if (!profile) return <div>Loading...</div>;
  return (
    <div>
      <h2>내 정보</h2>
      <div>이메일: {profile.email}</div>
      <div>이름: {profile.profile.name}</div>
      <div>역할: {profile.role}</div>
      {/* ... */}
    </div>
  );
}
