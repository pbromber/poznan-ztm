#!/usr/bin/env python3
"""Simple test script for Poznań Transport API."""

import asyncio
import aiohttp
import sys

API_URL = "https://www.peka.poznan.pl/vm/method.vm"

async def test_api(stop_symbol):
    """Test the API with a given stop symbol."""
    headers = {
        "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    data = f'method=getTimes&p0={{"symbol":"{stop_symbol}"}}'

    print(f"Testing API for stop: {stop_symbol}")
    print("-" * 50)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(API_URL, headers=headers, data=data, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                result = await response.json()

                if "success" not in result:
                    print(f"❌ Error: Invalid response")
                    print(result)
                    return False

                success = result["success"]
                
                # Display stop info
                bollard = success.get("bollard", {})
                print(f"✅ Stop found: {bollard.get('name')} ({bollard.get('symbol')})")
                print()

                # Display departures
                times = success.get("times", [])
                if not times:
                    print("No departures scheduled")
                    return True

                print(f"Next {len(times)} departures:")
                print()

                for i, time in enumerate(times[:5], 1):
                    line = time.get("line", "?")
                    direction = time.get("direction", "Unknown")
                    minutes = time.get("minutes", 0)
                    real_time = "🟢 Real-time" if time.get("realTime") else "🟡 Scheduled"
                    
                    features = []
                    if time.get("bike"):
                        features.append("🚲")
                    if time.get("airCnd"):
                        features.append("❄️")
                    if time.get("lowFloorBus") or time.get("lfRamp"):
                        features.append("♿")
                    
                    features_str = " ".join(features) if features else ""
                    
                    print(f"{i}. Line {line} → {direction}")
                    print(f"   Time: {minutes} min | {real_time} {features_str}")
                    print()

                return True

        except aiohttp.ClientError as err:
            print(f"❌ Connection error: {err}")
            return False
        except Exception as err:
            print(f"❌ Error: {err}")
            return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        stop = sys.argv[1].upper()
    else:
        stop = "NIED01"  # Default test stop
    
    success = asyncio.run(test_api(stop))
    sys.exit(0 if success else 1)

