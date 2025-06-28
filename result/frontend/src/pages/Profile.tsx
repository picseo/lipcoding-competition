import React from 'react';

const Profile = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <form className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">프로필</h2>
        <div className="mb-4">
          <label htmlFor="name" className="block mb-1">이름</label>
          <input id="name" type="text" className="w-full border rounded px-3 py-2" required />
        </div>
        <div className="mb-4">
          <label htmlFor="bio" className="block mb-1">소개</label>
          <textarea id="bio" className="w-full border rounded px-3 py-2" rows={3} />
        </div>
        <div className="mb-4">
          <label htmlFor="skillsets" className="block mb-1">기술 스택</label>
          <input id="skillsets" type="text" className="w-full border rounded px-3 py-2" />
        </div>
        <div className="mb-4 flex flex-col items-center">
          <img id="profile-photo" src="https://placehold.co/500x500.jpg?text=PROFILE" alt="프로필" className="w-32 h-32 rounded-full object-cover mb-2" />
          <input id="profile" type="file" accept=".png,.jpg" className="w-full" />
        </div>
        <button id="save" type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">저장</button>
      </form>
    </div>
  );
};

export default Profile;
