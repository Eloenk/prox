import fs from 'fs';
import axios from 'axios';

const proxyFile = 'proxies.txt';
const fastProxiesFile = 'fast_proxies.txt';
const workingProxiesFile = 'working_proxies.txt';
const testUrl = 'https://www.google.com';
const timeoutThreshold = 960;

async function testProxy(proxy) {
    const url = `http://${proxy.trim()}`;
    const start = Date.now();
    try {
        await axios.get(testUrl, {
            proxy: {
                host: url.split('://')[1].split(':')[0],
                port: url.split(':')[2],
            },
            timeout: timeoutThreshold,
        });
        const duration = Date.now() - start;
        return { proxy: url, duration };
    } catch (error) {
        return null;
    }
}

async function processProxies() {
    const proxies = fs.readFileSync(proxyFile, 'utf8').split('\n').map(p => p.trim()).filter(p => p);
    const fastProxies = [];
    const workingProxies = [];

    for (const proxy of proxies) {
        const result = await testProxy(proxy);
        if (result) {
            if (result.duration <= timeoutThreshold) {
                fastProxies.push(result.proxy);
            } else {
                workingProxies.push(result.proxy);
            }
            console.log(`Proxy ${result.proxy} responded in ${result.duration}ms`);
        } else {
            console.log(`Proxy ${proxy} failed.`);
        }
    }

    fs.writeFileSync(fastProxiesFile, fastProxies.join('\n'));
    fs.writeFileSync(workingProxiesFile, workingProxies.join('\n'));
    console.log(`Fast proxies saved to ${fastProxiesFile}`);
    console.log(`Working proxies saved to ${workingProxiesFile}`);
}

processProxies();
