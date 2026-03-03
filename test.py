import google.generativeai as genai

# Load env file to get API key
api_key = "AIzaSyDjjPoSpVo4ys3Jg6QE2rHtie7MJcvbfBA"

if not api_key:
    print("API KEY not found in stix&vulnerability/.env")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

print("Testing Gemini API...")
try:
    response = model.generate_content("Hello, this is a test. Reply with 'OK' if you receive this.")
    print("Success! Response from model:")
    print(response.text)
except Exception as e:
    print("Error during API call:")
    print(e)
