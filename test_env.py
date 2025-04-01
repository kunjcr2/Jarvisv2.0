import os
from dotenv import load_dotenv
import openai

def test_env_variables():
    """
    Test if environment variables from .env file are loading correctly
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # List of environment variables to check
    env_vars = {
        'OPENAI_API_KEY': 'OpenAI API Key',
        'EMAIL_ADDRESS': 'Email Address',
        'EMAIL_PASSWORD': 'Email Password'
    }
    
    print("Testing environment variables from .env file:")
    print("="*50)
    
    all_vars_loaded = True
    
    for var, description in env_vars.items():
        value = os.getenv(var)
        if value:
            # Only show first and last few characters of sensitive data
            if var == 'OPENAI_API_KEY' and len(value) > 10:
                masked_value = value[:5] + '...' + value[-5:]
                print(f"✅ {description} ({var}): {masked_value}")
            elif var == 'EMAIL_PASSWORD' and len(value) > 4:
                masked_value = '*' * len(value)
                print(f"✅ {description} ({var}): {masked_value}")
            else:
                print(f"✅ {description} ({var}): {value}")
        else:
            print(f"❌ {description} ({var}): Not found")
            all_vars_loaded = False
    
    print("="*50)
    if all_vars_loaded:
        print("All environment variables are loaded successfully!")
    else:
        print("Some environment variables are missing!")
    
    # Return the API key for further inspection if needed
    return os.getenv('OPENAI_API_KEY')

def test_openai_api(api_key):
    """
    Test if OpenAI API key works by making a simple API call
    """
    if not api_key:
        print("\n❌ Error: Cannot test OpenAI API - API key not found")
        return False
    
    print("\n" + "="*50)
    print("Testing OpenAI API with the provided key:")
    print("="*50)
    
    # Set up OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    try:
        print("Testing API key with a simple completion request...")
        
        # Make a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a widely available model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API key is working!' in one short sentence."}
            ],
            max_tokens=20
        )
        
        # Extract and print the response
        response_text = response.choices[0].message.content.strip()
        print(f"\n✅ Success! API response: \"{response_text}\"")
        
        # Now try with the gpt-4o-mini model if specified
        print("\nTesting with gpt-4o-mini model...")
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'gpt-4o-mini is working!' in one short sentence."}
                ],
                max_tokens=20
            )
            
            response_text = response.choices[0].message.content.strip()
            print(f"\n✅ Success with gpt-4o-mini! Response: \"{response_text}\"")
        except Exception as e:
            print(f"\n❌ Error with gpt-4o-mini model: {str(e)}")
            print("This might indicate your API key doesn't have access to this model.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        
        if "auth" in str(e).lower() or "api key" in str(e).lower():
            print("\nThis looks like an authentication error. Your API key might be invalid.")
            if api_key.startswith('sk-proj-'):
                print("Notice: You're using a project-specific key (starts with 'sk-proj-').")
                print("These keys might not work with all OpenAI endpoints. Try a standard API key instead.")
        
        return False

if __name__ == "__main__":
    # First test if environment variables are loaded
    api_key = test_env_variables()
    
    # Extra check for the API key format
    if api_key:
        if api_key.startswith('sk-'):
            print("\nAPI Key format appears correct (starts with 'sk-')")
        elif api_key.startswith('sk-proj-'):
            print("\nWarning: Your API key appears to be a project-specific key (starts with 'sk-proj-').")
            print("This may not work with certain OpenAI endpoints. Consider using a standard API key.")
        else:
            print("\nWarning: Your API key doesn't start with the expected prefix 'sk-'")
    else:
        print("\nNo API key found")
    
    # Then test if the API key works with OpenAI
    success = test_openai_api(api_key)
    
    print("\n" + "="*50)
    if success:
        print("✅ OpenAI API key is working correctly!")
    else:
        print("❌ OpenAI API key test failed. Please check the errors above.")
    print("="*50) 