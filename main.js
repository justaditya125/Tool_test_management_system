const { app, BrowserWindow, dialog, ipcMain } = require('electron');
const fs = require('fs');
const path = require('path');

const url = require('url');
const { ipcMain } = require('electron');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadURL(
        url.format({
            pathname: path.join(__dirname, 'index.html'),
            protocol: 'file:',
            slashes: true
        })
    );

    mainWindow.webContents.openDevTools(); 

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

app.on('ready', createWindow);

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', function () {
    if (mainWindow === null) {
        createWindow();
    }
});

ipcMain.on('save-csv', async (event, csvData) => {
    const { filePath } = await dialog.showSaveDialog({
        buttonLabel: 'Save CSV',
        defaultPath: path.join(app.getPath('downloads'), 'test_cases.csv'),
        filters: [
            { name: 'CSV Files', extensions: ['csv'] }
        ]
    });

    if (filePath) {
        fs.writeFileSync(filePath, csvData);
        event.reply('csv-saved', 'CSV file saved successfully');
    }
});
