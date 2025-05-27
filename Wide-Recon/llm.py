import os
import json
from groq import Groq

def get_asn_for_domain(domain, file_data, client):
    """
    Use Groq API to find ASN numbers associated with the domain
    """
    # Construct prompt to extract ASN numbers
    prompt = f"""
    Given the following ASN data and the domains {domain}, 
    identify the Prefix CIDR associated with these domains.
    
    ASN Data:
    {file_data}
    
    Domains: {domain}
    
    Respond ONLY with a JSON array of Prefix CIDR. 
    If no CIDRs associated with the domains provided (the simillar name of the domains should be in the "Name" field of the table )are found, return an empty array.

   Example:
   ["192.168.1.0/24"]
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert at analyzing network and ASN data."},
                {"role": "user", "content": prompt}
            ],
            model="deepseek-r1-distill-llama-70b"
        )
        
        # Extract and parse the response
        response = chat_completion.choices[0].message.content
        response = response.split("</think>", 1)[1].strip()
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
    domain = file.readlines()
    
    # Get ASN numbers
    asn_numbers = get_asn_for_domain(domain, file_data, client)
    
    # Output results
    print(json.dumps(asn_numbers, indent=2))

if __name__ == "__main__":
    main()
