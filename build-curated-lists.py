#!/usr/bin/env python3
import os

def create_curated_lists():
    """Create curated lists of IP blocks for specific country groups"""
    
    # Ensure Curated-Lists directory exists
    os.makedirs('Curated-Lists', exist_ok=True)
    
    # State Sponsors of Terrorism list
    state_sponsors = []
    countries_state = {
        'IR': 'Iran',
        'CU': 'Cuba', 
        'KP': 'North Korea',
        'SY': 'Syria'
    }
    
    for country_code, country_name in countries_state.items():
        # IPv4
        ipv4_file = f'TXT/IPV4/{country_code}.txt'
        if os.path.exists(ipv4_file):
            with open(ipv4_file, 'r') as f:
                state_sponsors.extend(f.read().strip().split('\n'))
        
        # IPv6
        ipv6_file = f'TXT/IPV6/{country_code}.txt'
        if os.path.exists(ipv6_file):
            with open(ipv6_file, 'r') as f:
                state_sponsors.extend(f.read().strip().split('\n'))
    
    # Write State Sponsors list
    with open('Curated-Lists/StateSponsorsOfTerrorism.txt', 'w') as f:
        f.write('\n'.join(state_sponsors))
    
    print(f'Created StateSponsorsOfTerrorism.txt with {len(state_sponsors)} IP blocks')
    
    # OFAC Sanctioned Countries list
    ofac_sanctioned = []
    countries_ofac = {
        'IR': 'Iran',
        'CU': 'Cuba',
        'KP': 'North Korea',
        'SY': 'Syria',
        'RU': 'Russia',
        'BY': 'Belarus',
        'YE': 'Yemen',
        'IQ': 'Iraq',
        'MM': 'Myanmar',
        'CF': 'Central African Republic',
        'CD': 'Congo, Dem. Rep.',
        'ET': 'Ethiopia',
        'HK': 'Hong Kong',
        'LB': 'Lebanon',
        'LY': 'Libya',
        'SD': 'Sudan',
        'VE': 'Venezuela',
        'ZW': 'Zimbabwe'
    }
    
    for country_code, country_name in countries_ofac.items():
        # IPv4
        ipv4_file = f'TXT/IPV4/{country_code}.txt'
        if os.path.exists(ipv4_file):
            with open(ipv4_file, 'r') as f:
                content = f.read().strip()
                if content:
                    ofac_sanctioned.extend(content.split('\n'))
        
        # IPv6
        ipv6_file = f'TXT/IPV6/{country_code}.txt'
        if os.path.exists(ipv6_file):
            with open(ipv6_file, 'r') as f:
                content = f.read().strip()
                if content:
                    ofac_sanctioned.extend(content.split('\n'))
    
    # Write OFAC Sanctioned list
    with open('Curated-Lists/OFACSanctioned.txt', 'w') as f:
        f.write('\n'.join(ofac_sanctioned))
    
    print(f'Created OFACSanctioned.txt with {len(ofac_sanctioned)} IP blocks')

if __name__ == '__main__':
    create_curated_lists()