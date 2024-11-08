import { writable } from 'svelte/store';

export const loadedFiles = writable([]);
export const pdfContents = writable({});
export const statusMessage = writable('');
