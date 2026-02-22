const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('recorderAPI', {
  start: (options) => ipcRenderer.invoke('recorder:start', options),
  stop: (exportFormats) => ipcRenderer.invoke('recorder:stop', exportFormats),
  addComment: (text) => ipcRenderer.invoke('recorder:addComment', text),
  getState: () => ipcRenderer.invoke('recorder:getState'),
  openReport: (filePath) => ipcRenderer.invoke('recorder:openReport', filePath),
});
