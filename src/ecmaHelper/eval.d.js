// WaifuBot - UserBot
// All Rights @TeamUltroid < https://github.com/TeamUltroid/Ultroid/ >
//
// Editado por @fnixdev

const { exec } = require('child_process');
const { appendFileSync, truncate } = require('fs');

(async () => {
    truncate('./src/ecmaHelper/evalJs.result.d.txt', 0, function() {
        console.log('Result File Truncated')
        const evalJs = exec('node ./src/ecmaHelper/evalJs.run.js');

        evalJs.stdout.on('data', (data) => {
            appendFileSync('./src/ecmaHelper/evalJs.result.d.txt', `${data.toString()}\n`, () => {});
        });

        evalJs.stderr.on('data', (error) => {
            appendFileSync('./src/ecmaHelper/evalJs.result.d.txt', `${error}\n`, () => {});
        });
    });
})();
