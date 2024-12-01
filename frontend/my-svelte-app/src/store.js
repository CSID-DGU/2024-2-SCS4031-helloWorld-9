import { writable } from 'svelte/store';

// 파일 매니저의 기본 구조
const initialFileStructure = [
  {
    id: "/",
    type: "folder",
    date: new Date(),
  }
];

// 파일 매니저의 상태를 저장하는 store
export const fileManagerState = writable({
  structure: initialFileStructure,
  activePanel: 0,
  mode: 'cards',
  currentPath: '/'
});

// PDF 파일의 내용을 저장하는 store
export const pdfContents = writable({});

// 파일 매니저의 drive 정보를 저장하는 store
export const driveInfo = writable({
  used: 0,
  total: 1000000000 // 1GB 기본 할당
});

// 상태 메시지를 저장하는 store
export const statusMessage = writable('');

export const chatMessages = writable([]);