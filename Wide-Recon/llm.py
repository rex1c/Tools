import os
import json
from groq import Groq

def get_asn_for_domain(domain, file_data, client):
    """
    Use Groq API to find ASN numbers associated with the domain
    """
    # Construct prompt to extract ASN numbers
    prompt = f"""
    Given the following ASN data and the domain {domain}, 
    identify the ASN numbers associated with this domain.
    
    ASN Data:
    {file_data}
    
    Domain: {domain}
    
    Respond ONLY with a JSON array of ASN numbers. 
    If no ASNs are found, return an empty array.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert at analyzing network and ASN data."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        
        # Extract and parse the response
        response = chat_completion.choices[0].message.content
        return json.loads(response)
    
    except Exception as e:
        print(f"Error in Groq API call: {e}")
        return []

def main():
    # Groq API setup
    client = Groq(api_key="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")

    
    # ASN data as a string
    file = open("ASN.res" , "r")
    file_data = file.read()
    file.close()
    # Domain to lookup
    file = open("domains" , "r")
    domain = file.readlines()[0][:-1]
    
    # Get ASN numbers
    asn_numbers = get_asn_for_domain(domain, file_data, client)
    
    # Output results
    print(json.dumps(asn_numbers, indent=2))

if __name__ == "__main__":
    main()
