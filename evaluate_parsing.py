
import httpx, os
import json
import logging
import random

async def run(task: str):
    async with httpx.AsyncClient(timeout=30) as client:
        logging.warning(f"🟡 Running task: {task.strip()}")
        data = {
                "question": task
            }
        files = {}
        response = await client.post("http://localhost:8000/api/parse", data=data, files=files)
        try:
            response_text = response.json()
        except json.JSONDecodeError:
            response_text = response.text
        if response.status_code < 400:
            logging.info(f"🟢 HTTP {response.status_code} {response_text}")
        else:
            logging.error(f"🔴 HTTP {response.status_code} {response_text}")
        return response.status_code, response_text
    
async def evaluate(use_case: str):
    # file exists under test_data directory
    file_path = f"test_data/{use_case}.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            task = file.read()
        status_code, response_text = await run(task)
        if status_code != 200:
            return False
        
        # check the returned json matches the use case
        if "GA_No" in response_text and response_text["GA_No"] == use_case:
            return True
        else:
            return False
    else:
        #print("File does not exist.")
        return False
    

async def main():
    use_cases = [
        "GA1.1", "GA1.2", "GA1.3", "GA1.4", "GA1.5", "GA1.6", "GA1.7", "GA1.8", "GA1.9", "GA1.10", "GA1.11", "GA1.12", "GA1.13", "GA1.14", "GA1.15", "GA1.16", "GA1.17", "GA1.18",
        "GA2.1", "GA2.2", "GA2.3", "GA2.4", "GA2.5", "GA2.6", "GA2.7", "GA2.8", "GA2.9", "GA2.10",
        "GA3.1", "GA3.2", "GA3.3", "GA3.4", "GA3.5", "GA3.6", "GA3.7", "GA3.8", "GA3.9",
        "GA4.1", "GA4.2", "GA4.3", "GA4.4", "GA4.5", "GA4.6", "GA4.7", "GA4.8", "GA4.9", "GA4.10",
        "GA5.1", "GA5.2", "GA5.3", "GA5.4", "GA5.5", "GA5.6", "GA5.7", "GA5.8", "GA5.9", "GA5.10"
    ]
    use_cases = random.sample(use_cases, 5)
    a_score, a_total = 0, 0
    for use_case in use_cases:
        a_total += 1
        try:
            success = await evaluate(use_case)
        except Exception as e:
            logging.error(f"🔴 {use_case} failed: {e}")
            success = False
        if success:
            logging.info(f"✅ {use_case} PASSED")
        else:
            logging.error(f"❌ {use_case} FAILED")
        a_score += 1 if success else 0
        
    logging.info(f"🎯 Parsed: {a_score} / {a_total}")
    


if __name__ == "__main__":
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate GA No with configurable logging")
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    parser.add_argument("--log-level", default="INFO", choices=levels, help="Set logging level")
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level, format="%(message)s\n")
    
    asyncio.run(main())