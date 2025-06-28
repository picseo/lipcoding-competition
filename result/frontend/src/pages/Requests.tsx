import React from 'react';

const Requests = () => {
  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-4">매칭 요청</h2>
      {/* 예시 요청 목록 */}
      <div className="bg-white p-4 rounded shadow mb-4">
        <div className="request-message" mentee="mentee-1">멘티1의 요청 메시지</div>
        <div className="flex gap-2 mt-2">
          <button id="accept" className="bg-green-500 text-white px-4 py-1 rounded">수락</button>
          <button id="reject" className="bg-red-500 text-white px-4 py-1 rounded">거절</button>
        </div>
      </div>
      <div id="request-status" className="mt-4">상태: 대기중</div>
    </div>
  );
};

export default Requests;
