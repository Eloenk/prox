import requests
import time

# Read proxies from file
proxy_file = "list.txt"
with open(proxy_file, "r") as f:
    proxies = [p.strip() for p in f if p.strip()]  # Remove empty lines

# Ensure all proxies have "http://"
proxies = [p if p.startswith("http://") else f"http://{p}" for p in proxies]
print(proxies)
# URL to test connectivity
test_url = "http://ipinfo.io/json"
fast_proxies = []
slow_proxies = []

def test_proxy(proxy):
    try:
        start_time = time.time()
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=5)
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms

        if response.status_code == 200:
            print(f"✅ Proxy {proxy} is working. Response Time: {elapsed_time:.2f}ms")
            if elapsed_time <= 960:
                fast_proxies.append(proxy)
            else:
                slow_proxies.append(proxy)
        else:
            print(f"❌ Proxy {proxy} returned status code {response.status_code}.")
    except requests.RequestException as e:
        print(f"❌ Proxy {proxy} failed: {e}")

# Test each proxy
for proxy in proxies:
    test_proxy(proxy)

# Save categorized proxies to files
with open("fast_proxies.txt", "w") as f:
    f.writelines(f"{p}\n" for p in fast_proxies)

with open("slow_proxies.txt", "w") as f:
    f.writelines(f"{p}\n" for p in slow_proxies)

print(f"\n✅ {len(fast_proxies)} fast proxies saved to fast_proxies.txt")
print(f"✅ {len(slow_proxies)} slow proxies saved to slow_proxies.txt")
