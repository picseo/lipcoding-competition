import React from 'react';

const Mentors = () => {
  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-4">멘토 목록</h2>
      <div className="flex gap-4 mb-4">
        <input id="search" type="text" placeholder="기술 스택 검색" className="border rounded px-3 py-2" />
        <select id="name" className="border rounded px-3 py-2">
          <option value="">이름순</option>
        </select>
        <select id="skill" className="border rounded px-3 py-2">
          <option value="">스킬셋순</option>
        </select>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {/* 예시 멘토 카드 */}
        <div className="mentor bg-white p-4 rounded shadow flex flex-col items-center">
          <img src="https://placehold.co/500x500.jpg?text=MENTOR" alt="멘토" className="w-24 h-24 rounded-full mb-2" />
          <div className="font-bold">홍길동</div>
          <div>React, Node.js</div>
        </div>
      </div>
    </div>
  );
};

export default Mentors;
